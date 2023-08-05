"""Functions to handle Rust dependency files."""
from __future__ import annotations

import re

import toml

from depend.dep import Dep, RustDep


def handle_cargo_toml(file_data: str) -> list[Dep]:
    """
    Parse cargo toml files and return required keys
    :param file_data: content of toml
    """
    toml_parsed = dict(toml.loads(file_data))
    dependencies = []
    package_dep = toml_parsed.get("dependencies")
    for ir, spec in package_dep.items():
        if isinstance(spec, str):
            version = spec.split(",")[0]
            dependencies.append(RustDep("rust", ir, version))
        elif isinstance(spec, dict):
            version = spec.get("version")
            git_url = spec.get("git")
            features = spec.get("features", [])
            if version is not None:
                dep = RustDep("rust", ir, version, features)
                dependencies.append(dep)
            if git_url is not None:
                # TODO: create GithubRepo
                # git_branch = git_url + "||" + spec.get("branch", "")
                # dependencies.append(Dep("rust", ir, "*", git_branch))
                pass

    return dependencies


def handle_cargo_lock(file_data: str) -> list[Dep]:
    """
    Parses conda.yml tox.ini and Pipfiles
    this function returns only dependencies
    slated for removal once individual cases are handled
    """
    dependencies_regex = re.compile(
        r'name = \"([^"]+)\"[\n\r]version = \"([^"]+)\"', re.MULTILINE
    )
    matches = [(m[1], m[2]) for m in dependencies_regex.finditer(file_data)]
    return [RustDep("rust", name, str(version)) for name, version in matches]
