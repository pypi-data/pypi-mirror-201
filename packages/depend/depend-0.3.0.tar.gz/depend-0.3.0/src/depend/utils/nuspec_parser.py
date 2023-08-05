"""Functions to handle C# dependency files."""
from __future__ import annotations

from typing import OrderedDict

import xmltodict

from depend.dep import Dep


def handle_nuspec(req_file_data: str) -> list[Dep]:
    """
    Parse required info from .nuspec
    Parameters:
        req_file_data: Content of pom.xml
    """
    return parse_nuspec(req_file_data)


def parse_nuspec(req_file_data: str) -> list[Dep]:
    """
    Get data frim .nuspec files
    https://docs.microsoft.com/en-us/nuget/reference/nuspec#dependencies-element
    """
    root = xmltodict.parse(req_file_data).get("package", {}).get("metadata", {})
    dep_info = root.get("dependencies")
    dep_set = set()

    if dep_info and "group" in dep_info:
        # Dependencies Group
        if isinstance(dep_info["group"], OrderedDict):  # TODO: why is this ordereddict?
            group = dep_info["group"]
            if group and "dependency" in group:
                dep_set = dep_set.union(handle_nuspec_dep(group["dependency"]))
        else:
            for group in dep_info["group"]:
                if group and "dependency" in group:
                    dep_set = dep_set.union(handle_nuspec_dep(group["dependency"]))
    elif dep_info and "dependency" in dep_info:
        # Dependencies element
        dep_set = handle_nuspec_dep(dep_info["dependency"])
    return list(dep_set)


def handle_nuspec_dep(dep_list_obj) -> set[Dep]:
    """Convert dependency specification in nuspec to parsable string"""
    pkg_dep = set()
    if isinstance(dep_list_obj, list):
        for dep in dep_list_obj:
            dep_entry = Dep("cs", dep.get("@id"), dep.get("@version"))
            pkg_dep.add(dep_entry)
    else:
        dep_entry = Dep("cs", dep_list_obj.get("@id"), dep_list_obj.get("@version"))
        pkg_dep.add(dep_entry)
    return pkg_dep
