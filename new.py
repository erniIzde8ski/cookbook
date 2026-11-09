#!/usr/bin/env python3

import os
import subprocess
import sys
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Literal
from typing import LiteralString
from typing import Never

from cyclopts import App
from cyclopts import CycloptsError
from rich import print

eprint = partial(print, file=sys.stderr)


def abort(msg: str | None = None, /) -> Never:
    raise CycloptsError(msg)


ROOT = Path(__file__).parent
RECIPE_DIR = ROOT / "src" / "Pages" / "41-recipes"
assert RECIPE_DIR.is_dir()

SECTIONS = {path.name[3:].lower(): path for path in RECIPE_DIR.iterdir() if path.is_dir()}

if TYPE_CHECKING:
    SectionKey = LiteralString
else:
    SectionKey = Literal[*SECTIONS.keys()]


def template(title: str) -> str:
    return f"""#import "/prelude.typ": *

#Recipe(title: "{title}")
"""


app = App()


@app.default
def main(section: SectionKey, title: str, /):
    target_directory = SECTIONS[section]

    target = target_directory / (title.strip() + ".typ")
    if target.exists():
        abort("Target already exists.")

    _ = target.write_text(template(title))
    print("Wrote to path:", target)

    os.chdir(ROOT)
    _ = subprocess.run(("git", "add", "-N", target.as_posix()), check=True)
    print("Began tracking new path in git.")
    _ = subprocess.run(("doit", "compile:letter"), check=True)
    print("Regenerated index file.")


if __name__ == "__main__":
    app()
