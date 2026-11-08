import logging
import os
import subprocess as sp
import sys
from collections.abc import Iterator
from functools import partial
from hashlib import sha256
from pathlib import Path
from shutil import which
from typing import NamedTuple

import yaml

log = logging.getLogger(__name__)


class Version(NamedTuple):
    major: int
    minor: int
    patch: int = 0


MINIMUM_TYPST_VERSION = Version(0, 15)

LIBRARY_DIRECTORY = Path("src")
VARIANT_DIRECTORY = LIBRARY_DIRECTORY / "variants"
TARGET_DIRECTORY = Path("target")

TYPST_SOURCES = set(LIBRARY_DIRECTORY.rglob("*.typ"))
YAML_SOURCES = set(LIBRARY_DIRECTORY.rglob("*.yaml"))
ALL_SOURCES = TYPST_SOURCES | YAML_SOURCES
VARIANTS = {
    path for path in VARIANT_DIRECTORY.rglob("*.typ") if not path.name.startswith("_")
}
INDICES = set(LIBRARY_DIRECTORY.rglob("index.yaml"))
LIBRARIES = ALL_SOURCES - VARIANTS

FONT_PATHS = (os.environ.get("TYPST_FONT_PATHS") or "").split(os.pathsep)
FONT_PATHS.append("/usr/share/texmf-dist/fonts/opentype")
os.environ["TYPST_FONT_PATHS"] = os.pathsep.join(filter(bool, FONT_PATHS))


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


def Action(*args: str | Path) -> list[str]:
    result: list[str] = []
    for value in args:
        if isinstance(value, Path):
            value = value.as_posix()
        result.append(value)
    return result


def task_compile():
    libs = list(LIBRARIES)
    for variant in VARIANTS:
        name = variant.name.removesuffix(variant.suffix)
        target = TARGET_DIRECTORY / (name + ".pdf")
        yield {
            "name": name,
            "actions": [
                Action(
                    TINYMIST,
                    "compile",
                    "--save-lock",
                    "--root",
                    "src/",
                    "--",
                    variant,
                    target,
                )
            ],
            "file_dep": [variant] + libs,
            "targets": (target,),
        }


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


def task_build_index():
    for index_path in INDICES:
        path_bytes = index_path.as_posix().encode()
        hash = sha256(path_bytes).digest()
        short_hash = hash.hex()[:6]

        yield {
            "name": f"{short_hash}-{index_path.parent.name}",
            "actions": [partial(_build_index, index_path)],
            "file_dep": [*index_path.parent.rglob("*.typ")],
            "targets": (index_path,),
        }
