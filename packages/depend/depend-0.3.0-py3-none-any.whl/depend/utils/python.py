"""Helper functions for Python Dependencies"""
from __future__ import annotations

from packaging.requirements import InvalidRequirement, Requirement

from depend.dep import Dep


def handle_requirements_txt(req_file_data: str) -> list[Dep]:
    """
    Parse requirements file
    :param req_file_data: Content of requirements.txt
    Return:
          list of requirement and specs
    """
    requirement_lines = req_file_data.splitlines()
    return parse_requirements([line.partition("#")[0] for line in requirement_lines])


def parse_requirements(requirement_lines: list[str]) -> list[Dep]:
    if not requirement_lines:
        return []

    requirements = []
    for req_line in requirement_lines:
        try:
            requirements.append(Requirement(req_line))
        except InvalidRequirement:
            pass

    pkg_dep = []
    for ir in requirements:
        if "extra" in str(ir.marker):
            continue
        elif not ir.specifier._specs:
            pkg_dep.append(Dep("python", str(ir.name), "*"))
        else:
            pkg_dep.append(Dep("python", str(ir.name), str(ir.specifier).lstrip("=")))
    return pkg_dep
