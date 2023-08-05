"""Functions to handle Python dependency files."""
from __future__ import annotations

import dparse2
import toml

from depend.dep import Dep
from depend.parser.py.setup_reader import LaxSetupReader
from depend.utils.python import parse_requirements


def handle_setup_py(req_file_data: str) -> list[Dep]:
    """
    Parse setup.py
    :param req_file_data: Content of setup.py
    Return:dict containing dependency info and specs
    """
    parser = LaxSetupReader()
    return parser.auth_read_setup_py(req_file_data)


def handle_setup_cfg(req_file_data: str) -> list[Dep]:
    """
    Parse setup.py
    :param req_file_data: Content of setup.py
    Return:dict containing dependency info and specs
    """
    parser = LaxSetupReader()
    return parser.read_setup_cfg(req_file_data)


def handle_toml(file_data: str) -> list[Dep]:
    """
    Parse pyproject or poetry toml files and return required keys
    :param file_data: content of toml
    """
    toml_parsed = dict(toml.loads(file_data))
    package_data = toml_parsed.get("package")
    if package_data is None:
        package_data = toml_parsed.get("tool", {}).get("poetry", {})
        return [
            Dep("python", name, version)
            for (name, version) in package_data.get("dependencies", {}).items()
            if isinstance(version, str)
            if name != "python"
        ]

    package_dep = package_data.get("dependencies")
    if isinstance(package_dep, dict):
        # TODO: what is this case?
        pass
    elif package_dep:
        return parse_requirements(package_dep)


def handle_otherpy(file_data: str, file_name: str) -> list[Dep]:
    """
    Parses conda.yml tox.ini and Pipfiles
    this function returns only dependencies
    slated for removal once individual cases are handled
    """
    df = dparse2.parse(file_data, file_name=file_name)
    return [Dep("python", dep.name, str(dep.specs)) for dep in df.dependencies]
