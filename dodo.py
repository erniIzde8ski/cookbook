import os
import subprocess as sp
import sys
from collections import defaultdict
from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterator
from collections.abc import Sequence as seq
from functools import partial
from hashlib import sha256
from pathlib import Path
from shutil import copyfileobj
from shutil import which
from typing import ClassVar
from typing import Literal
from typing import NamedTuple
from typing import NewType
from typing import Required
from typing import Self
from typing import TypedDict
from typing import cast
from typing import override
from urllib.error import HTTPError
from urllib.request import urlopen

import yaml
from doit.tools import result_dep
from evilfunctools import cache
from evilfunctools import compose
from evilfunctools import immediate
from loguru import logger as log
from pydantic import BaseModel


class Version(NamedTuple):
    major: int
    minor: int
    patch: int = 0


ShortHash = NewType("ShortHash", str)

type StrPath = os.PathLike[str]


@cache
def short_hash_from_str(__s: str, /) -> ShortHash:
    hash = sha256(__s.encode()).digest()
    return cast(ShortHash, hash.hex()[:6])


# TODO: assert that the results from this function are being used in a
# cross-platform, cross-machine stable manner somehow
@cache
def task_name_from_target(target: str | Path):

    if isinstance(target, Path):
        path = target
        target = path.as_posix()
    else:
        path = Path(target)
    hash = short_hash_from_str(target)
    return f"{hash}_{path.parent.name}"


MINIMUM_TYPST_VERSION = Version(0, 15)


TYPST_ROOT = Path("src")
VARIANT_DIRECTORY = TYPST_ROOT / "variants"
TARGET = Path("target")
FONT_CACHE = Path(__file__).resolve().parent / ".cache" / "fonts"


TYPST_SOURCES = set(TYPST_ROOT.rglob("*.typ"))
YAML_SOURCES = set(TYPST_ROOT.rglob("*.yaml"))
ALL_SOURCES = TYPST_SOURCES | YAML_SOURCES
VARIANTS = {
    path for path in VARIANT_DIRECTORY.rglob("*.typ") if not path.name.startswith("_")
}
INDICES = set(TYPST_ROOT.rglob("index.yaml"))
LIBRARIES = ALL_SOURCES - VARIANTS


FONT_PATHS = list(map(Path, (os.environ.get("TYPST_FONT_PATHS") or "").split(os.pathsep)))
FONT_PATHS.append(Path("/usr/share/texmf-dist/fonts/opentype"))
os.environ["TYPST_FONT_PATHS"] = os.pathsep.join(
    path.as_posix() for path in FONT_PATHS if path.exists()
)


def ensure_file(path: Path, url: str) -> bool:
    """Ensures that a file at `path` exists, downloading it from `url` if necessary.

    Returns True if the file exists or was successfully downloaded."""
    if path.exists():
        return True

    try:
        log.info(f"Downloading {path.name} from {url}")
        with urlopen(url, timeout=30) as response, path.open("wb") as file:  # pyright: ignore[reportAny]
            copyfileobj(response, file)  # pyright: ignore[reportAny]
        return True
    except HTTPError as err:
        log.error(f"Failed to download {path.name}:\n>>> URL: {url}\n>>> {err}")
        return False


font_libs = frozendict[Path, seq[str]]


class _GoogleTypefaceCache(BaseModel):
    hash: str
    paths: frozendict[str, frozenset[Path]]

    path: ClassVar[Path] = FONT_CACHE.with_name("google.yaml")

    @classmethod
    def load(cls) -> Self:
        with open(cls.path) as file:
            data: object = yaml.safe_load(file)  # pyright: ignore[reportAny]
        return cls.model_validate(data)

    def save(self):
        with open(self.path, "w") as file:
            _ = yaml.safe_dump(self.model_dump(mode="json"), file)

    @override
    def __iter__(self) -> Generator[tuple[str, frozenset[Path]]]:
        yield from self.paths.items()


def _get_google_typefaces(*typeface_names: str):
    REPOSITORY = "google/fonts"
    BRANCH = "main"

    from github import Github

    client = Github()
    repo = client.get_repo(REPOSITORY)
    branch = repo.get_branch(BRANCH)
    sha = branch.commit.sha

    try:
        cache = _GoogleTypefaceCache.load()
        if cache.hash == sha and set(typeface_names) == set(cache.paths.keys()):
            return cache
        else:
            log.info("sha is out of date, redownloading Google typefaces")
    except FileNotFoundError:
        pass

    paths = defaultdict[str, set[Path]](set)

    for name in typeface_names:
        files = repo.get_contents(f"/ofl/{name}/", ref=branch.name)
        assert isinstance(files, list)

        for file in files:
            path = Path(file.name)
            if path.suffix.lower() in (".ttf", ".otf"):
                paths[name].add(path)

    cache = _GoogleTypefaceCache(hash=sha, paths=paths)  # pyright: ignore[reportArgumentType]
    cache.save()
    return cache


@immediate
def FONT_LIBS() -> font_libs:

    intermediate_libs = defaultdict[Path, list[str]]
    retval = intermediate_libs(list)

    def addpath(path: Path, /):
        nonlocal retval
        retval[path.parent].append(path.name)

    root = FONT_CACHE
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)

    gfontrepo = "google/fonts"
    gfontrev = "master"

    gfonturl = f"https://raw.githubusercontent.com/{gfontrepo}/{gfontrev}/ofl"

    for typeface, paths in _get_google_typefaces(
        "ysabeau", "libertinusserif", "sourcesans3"
    ):
        if not paths:
            continue
        type_path = root / typeface
        type_path.mkdir(parents=True, exist_ok=True)
        for path in paths:
            url = f"{gfonturl}/{typeface}/{path}"
            target = type_path / path
            if ensure_file(target, url):
                addpath(target)

    extra_dirs = (Path(p) for p in ("/usr/share/texmf-dist/fonts/opentype",))

    for dir in extra_dirs:
        if not dir.is_dir():
            continue
        for path in dir.rglob("*.ttf"):
            addpath(path)

    return font_libs((key, tuple(vals)) for key, vals in retval.items())  # pyright: ignore[reportCallIssue]


def _get_tinymist():
    # `tinymist` is normal, `tinymist-linux-x64` happens in GitHub Actions
    for command in ("tinymist", "tinymist-linux-x64"):
        full_path = which(command)
        if full_path is None:
            continue

        version_output = sp.check_output((command, "--version"), encoding="utf8")
        version = (
            next(
                line
                for line in version_output.splitlines()
                if line.startswith("Typst Version:")
            )
            .split(":")[1]
            .strip()
            .split(".")
        )
        version = Version(*(int(x) for x in version))

        if version < MINIMUM_TYPST_VERSION:
            log.warning(
                f"Skipping executable: discovered version ({version})"
                f" is lower than required minimum version ({MINIMUM_TYPST_VERSION})\n"
                f"  Command: {command}\n"
                f"  Full path: {full_path}"
            )
            continue

        return command

    print("No valid `tinymist` executable could be found :(")
    sys.exit(1)


TINYMIST = _get_tinymist()

type CmdAction = list[str]
type PyAction = Callable[[], bool | None | str | dict[object, object]]
type Action = CmdAction | PyAction


def cmdaction(*args: str | Path) -> CmdAction:
    result: list[str] = []
    for value in args:
        if isinstance(value, Path):
            value = value.as_posix()
        result.append(value)
    return result


def _generate_flat_index(root: Path) -> Iterator[str]:
    files: list[str] = []
    for path in sorted(root.iterdir()):
        if path.name.startswith(".") or path.name.startswith("_"):
            continue
        if path.is_dir():
            yield path.name + "/"
            for child in _generate_flat_index(path):
                yield f"{path.name}/{child}"
        elif path.is_file() and path.suffix == ".typ":
            files.append(path.name)
    yield from files


def _build_index(index: Path):
    paths = list(_generate_flat_index(index.parent))
    with open(index, "w") as file:
        yaml.dump(paths, file)


class _TaskInfo(TypedDict, total=False):
    actions: Required[list[Action]]
    targets: seq[StrPath]
    "Files generated by this subtask."
    file_dep: seq[StrPath]
    "Files required by this subtask."
    task_dep: seq[str]
    uptodate: list[bool | result_dep]
    clean: bool
    doc: str
    "Documentation for this task."
    basename: str
    verbosity: Literal[0, 1, 2]
    """Defines console output behavior:
    - 0: capture stdout/stderr
    - 1: capture stdout only (default)
    - 2: capture nothing
    """


class Subtask(_TaskInfo, total=True):
    name: str


class Task(_TaskInfo):
    pass


type TaskGenerator = Generator[Subtask]


@cache
@compose(tuple)
@compose(sorted)
def list_deps_of_index(index: Path):
    return index.parent.rglob("*.typ")


def task_check_index() -> TaskGenerator:
    for path in INDICES:
        action = compose(str, partial(list_deps_of_index, path))
        yield Subtask(name=task_name_from_target(path), actions=[action])


def task_build_indices() -> TaskGenerator:
    for path in INDICES:
        name = task_name_from_target(path)

        yield Subtask(
            name=name,
            actions=[partial(_build_index, path)],
            targets=(path,),
            uptodate=[result_dep(f"check_index:{name}")],
        )


def task_compile():
    libs = list(LIBRARIES)
    modes = ("debug", "release")
    for variant in VARIANTS:
        name = variant.name.removesuffix(variant.suffix)
        for mode in modes:
            target_file = TARGET / mode / (name + ".pdf")
            task = Subtask(
                name=f"{mode}/{name}",
                actions=[
                    cmdaction(
                        TINYMIST,
                        "compile",
                        "--save-lock",
                        "--root=src",
                        "--font-path",
                        FONT_CACHE,
                        "--input",
                        f"{mode=!s}",
                        "--",
                        variant,
                        target_file,
                    )
                ],
                file_dep=[variant] + libs,
                targets=[target_file],
            )
            if mode == "release":
                task["uptodate"] = [True]
            yield task


if __name__ == "__main__":
    print(f"{FONT_LIBS = }")
