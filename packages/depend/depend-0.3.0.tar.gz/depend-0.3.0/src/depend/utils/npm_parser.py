"""Functions to handle npm's json request/package.json files"""
from __future__ import annotations

from depend.dep import Dep


def nested_deps(json_input):
    for package, package_data in json_input.items():
        version = package_data.get("version", "*")
        if version.startswith("github"):
            # TODO: yield a GithubDep here
            pass
        else:
            yield Dep("javascript", package, version)
        deps = package_data.get("dependencies")
        if isinstance(deps, dict):
            yield from nested_deps(deps)


def handle_npm_json(package_data: dict) -> list[Dep]:
    dependencies = []
    dep_data = (
        package_data.get("dependencies") or package_data.get("__dependencies") or {}
    )
    if dep_data:
        if any(isinstance(i, dict) for i in dep_data.values()):
            dependencies = [*nested_deps(dep_data)]
        else:
            for package, version in dep_data.items():
                if version == "latest":
                    version = "*"
                # TODO: that github check from nested_deps might be needed here too
                dependencies.append(Dep("javascript", package, version))
    return dependencies

    # repo = repo_q.search(package_data) or ""
    # return repo
