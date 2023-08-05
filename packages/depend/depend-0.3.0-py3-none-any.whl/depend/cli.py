"""CLI for depend."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from loguru import logger
from rich import print as rprint

from depend import Depend
from depend.errors import (
    FileNotSupportedError,
    LanguageNotSupportedError,
    VCSNotSupportedError,
)

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    lang: str = typer.Option(..., help="python, javascript, go, cs, php, rust"),
    packages: Optional[str] = typer.Option(None, help="rich:latest,pygit2:~=1.9.2,..."),
    dep_file: Optional[Path] = typer.Option(None, help="Absolute or Relative Path"),
    depth: Optional[int] = typer.Option(None, help="Recursive resolution by default"),
    debug: bool = typer.Option(False, help="Enables debug logs"),
):
    """
    Dependency Inspector

    Retrieves licenses and dependencies of Python, JavaScript, C#, PHP, Rust and Go packages.
    Uses Package Indexes for Python and Javascript.

    Go is temporarily handled by scraping pkg.go.dev and VCS.

    VCS support is currently limited to GitHub only.

    Parameters such as auth tokens and passwords can be defined in config.ini,
    rather than specifying as an argument.
    """
    if debug or any(x in os.environ for x in ("PYCHARM_HOSTED", "GITHUB_ACTIONS")):
        level = "DEBUG"
    else:
        level = "WARNING"

    config = {
        "handlers": [{"sink": sys.stderr, "level": level}],
    }
    logger.configure(**config)

    try:
        if packages:
            result = Depend(packages, lang, depth, debug).resolve()
        else:
            result = Depend.from_dep_file(dep_file, lang, depth, debug).resolve()
        rprint(json.dumps(result, indent=3))
    except (
        LanguageNotSupportedError,
        VCSNotSupportedError,
        FileNotSupportedError,
    ) as e:
        logger.error(e.msg)
        sys.exit(-1)
