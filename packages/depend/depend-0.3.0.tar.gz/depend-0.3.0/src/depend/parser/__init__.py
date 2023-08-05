"""File parsing logic"""
from __future__ import annotations

import os
from pathlib import Path

from depend.dep import Dep
from depend.errors import FileNotSupportedError
from depend.parser.go import handle_go_mod
from depend.parser.js import handle_package_json, handle_yarn_lock
from depend.parser.php import handle_composer_json
from depend.parser.py import (
    handle_otherpy,
    handle_setup_cfg,
    handle_setup_py,
    handle_toml,
)
from depend.parser.rust import handle_cargo_lock, handle_cargo_toml
from depend.utils.nuspec_parser import parse_nuspec
from depend.utils.python import handle_requirements_txt


def handle_dep_file(file_location: Path) -> list[Dep]:
    """
    Parses contents of requirement file and returns useful insights
    Parameters:
        file_location: location of requirement file
    Return:
          key features for depend
    """
    file_name = os.path.basename(file_location)
    file_content = file_location.read_text()
    return handle_dep_file_content(file_name, file_content)


def handle_dep_file_content(
    file_name: str,
    file_content: str,
) -> list[Dep]:
    """
    Parses contents of requirement file and returns useful insights
    Parameters:
        file_name: name of requirement file
        file_content: content of the file
    Return:
          key features for depend
    """
    file_extension = file_name.split(".")[-1]
    if file_name in ["conda.yml", "tox.ini", "Pipfile", "Pipfile.lock"]:
        return handle_otherpy(file_content, file_name)
    if file_extension == "mod":
        return handle_go_mod(file_content)
    elif file_extension == "json":
        if file_name == "composer.json":
            return handle_composer_json(file_content)
        return handle_package_json(file_content)
    elif file_extension == "lock":
        if file_name == "Cargo.lock":
            return handle_cargo_lock(file_content)
        return handle_yarn_lock(file_content)
    elif file_extension == "txt":
        return handle_requirements_txt(file_content)
    elif file_extension == "toml":
        if file_name == "Cargo.toml":
            return handle_cargo_toml(file_content)
        return handle_toml(file_content)
    elif file_extension == "py":
        return handle_setup_py(file_content)
    elif file_extension == "cfg":
        return handle_setup_cfg(file_content)
    elif file_extension == "nuspec":
        return parse_nuspec(file_content)
    else:
        raise FileNotSupportedError(file_name)
