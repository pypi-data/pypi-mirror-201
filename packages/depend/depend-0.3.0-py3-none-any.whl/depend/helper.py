"""Helper Functions for Inspector."""
from __future__ import annotations

import re
from typing import Optional

from loguru import logger
from packaging.specifiers import SpecifierSet

from depend.errors import LanguageNotSupportedError


def prefix_equals(constraint: str) -> str:
    """If the input is a version with no range specifier, prepend it with `==`."""
    constraint = constraint.strip()
    specifier_characters = (">", "=", "<", "^", "~")

    if not constraint.startswith(specifier_characters):
        return f"=={constraint}"

    return constraint


def fix_constraint_rust(constraint: str) -> str:
    """Rust version constrains to Python"""
    # Ref: https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
    if constraint.startswith("="):
        return f"={constraint}"

    # Default works like caret
    if "*" not in constraint:
        if constraint.startswith("~"):
            constraint = handle_tilde(constraint)
        elif constraint[:1].isalnum():
            constraint = "^" + constraint

        if constraint.startswith("^"):
            constraint = handle_caret(constraint)

    return prefix_equals(constraint)


def fix_constraint_php(constraint: str) -> str:
    """PHP version constrains to Python"""
    constraint = constraint.strip()
    # range constraints alternative
    if constraint.startswith("^"):
        constraint = handle_caret(constraint)
    elif constraint.startswith("~"):
        constraint = handle_tilde(constraint, True)
    elif " - " in constraint:
        constraint = constraint.split(" - ", 1)
        constraint = f">={constraint[0]}, <={constraint[1]}"
    # handle remaining logical ands
    constraint = re.sub(r"(\s)+(?!\w)", ",", constraint)
    return prefix_equals(constraint)


def fix_constraint_cs(constraint: str) -> str:
    """C# version constrains to Python"""
    if constraint[0] == "(":
        ver_spec = constraint[1:-1].split(",")
        if constraint[-1] == ")":
            if ver_spec[0] and not ver_spec[1]:
                constraint = ">" + ver_spec[0]
            elif not ver_spec[0] and ver_spec[1]:
                constraint = "<" + ver_spec[1]
            else:
                constraint = ">" + ver_spec[0] + ",<" + ver_spec[1]
        else:
            if ver_spec[0] and not ver_spec[1]:
                constraint = ">" + ver_spec[0]
            elif not ver_spec[0] and ver_spec[1]:
                constraint = "<=" + ver_spec[1]
            else:
                constraint = ">" + ver_spec[0] + ",<=" + ver_spec[1]
    elif constraint[0] == "[":
        ver_spec = constraint[1:-1].split(",")
        if len(ver_spec) == 1:
            constraint = "==" + ver_spec[0]
        elif constraint[-1] == ")":
            if ver_spec[0] and not ver_spec[1]:
                constraint = ">=" + ver_spec[0]
            elif not ver_spec[0] and ver_spec[1]:
                constraint = "<" + ver_spec[1]
            else:
                constraint = ">=" + ver_spec[0] + ",<" + ver_spec[1]
        else:
            if ver_spec[0] and not ver_spec[1]:
                constraint = ">=" + ver_spec[0]
            elif not ver_spec[0] and ver_spec[1]:
                constraint = "<=" + ver_spec[1]
            else:
                constraint = ">=" + ver_spec[0] + ",<=" + ver_spec[1]
    else:
        constraint = ">=" + constraint
    return constraint


def fix_constraint_js(constraint: str) -> str:
    """JavaScript version constrains to Python"""
    # JS supports * or x as a direct major ver wildcard
    # Replacing '.x' with '.*' should be fine, as `package=x` isn't valid
    # (use `package=*` for that), and for cases like `1.2.3-pre.x`, i think
    # it's fine to have it replaced with `1.2.3-pre.*`.
    # https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies
    constraint = constraint.strip().replace(".x", ".*")

    if constraint.startswith("^"):
        constraint = handle_caret(constraint)
    elif constraint.startswith("~"):
        constraint = handle_tilde(constraint)
    # range constraints alternative
    elif " - " in constraint:
        constraint = constraint.split(" - ", 1)
        constraint = f">={constraint[0]}, <={constraint[1]}"
    # handle remaining logical ands
    constraint = re.sub(r"(\s)+(?!\w)", ",", constraint)

    return prefix_equals(constraint)


def fix_constraint_py(constraint: str) -> str:
    """Python non standard version constrains handling"""
    # handle poetry spec of tilde requirements
    # constraint = re.sub(r"=*~(?!=)", "~=", constraint)
    # caret requirements
    if "^" in constraint:
        constraint = handle_caret(constraint)
    if "~" in constraint and "~=" not in constraint:
        constraint = handle_tilde(constraint)

    return prefix_equals(constraint)


def handle_caret(req: str) -> str:
    """Handle caret based requirement constraints"""
    original_version = req.lstrip("^")
    version, _, _ = original_version.partition("-")
    major, minor, patch, *_ = (version + "...").split(".")
    if patch:
        if minor == "0" and major == "0":
            limit = f"0.0.{int(patch) + 1}"
        elif major == "0":
            limit = f"0.{int(minor) + 1}.0"
        else:
            limit = f"{int(major) + 1}.0.0"
    elif minor:
        if major == "0":
            limit = f"0.{int(minor) + 1}.0"
        else:
            limit = f"{int(major) + 1}.0.0"
    else:
        limit = f"{int(major) + 1}.0.0"
    return f">={version},<{limit}"


def handle_tilde(req: str, is_php: bool = False) -> str:
    """Handle tilde based requirement constraints"""
    original_version = req.lstrip("~")
    version, _, _ = original_version.partition("-")
    major, minor, patch, *_ = (version + "...").split(".")
    if patch:
        limit = f"{major}.{int(minor) + 1}.0"
    elif minor and not is_php:
        # if major.minor is given php wont lock the minor version
        limit = f"{major}.{int(minor) + 1}.0"
    else:
        limit = f"{int(major) + 1}.0.0"
    return f">={original_version},<{limit}"


def fix_constraint(language, package, reqs: str) -> tuple[SpecifierSet]:
    """
    Fixes requirement string to be parsed by python requirements
    Parameters:
        language: language to decide conversion criterion
        package: name of package
        reqs: requirement info associated with package
    """
    constraint = reqs.strip()
    if constraint == "*" or not constraint:
        return (SpecifierSet(),)

    if language == "python":
        constraints = [
            ",".join(
                [
                    fix_constraint_py(sub_constraint)
                    for sub_constraint in constraint.split(",")
                ]
            )
        ]
    elif language == "javascript":
        constraints = []
        # handle logical or
        for sub_constraint in constraint.split("||"):
            sub_constraint = ",".join(
                [
                    fix_constraint_js(constraint)
                    for constraint in sub_constraint.split(",")
                ]
            )
            constraints.append(sub_constraint)
    elif language == "go":
        # https://go.dev/ref/mod#go-mod-file-require
        constraints = ["==" + constraint]
    elif language == "cs":
        # https://docs.microsoft.com/en-us/nuget/concepts/package-versioning#version-ranges
        constraints = [fix_constraint_cs(constraint)]
    elif language == "php":
        # https://getcomposer.org/doc/articles/versions.md#writing-version-constraints
        constraints = []
        # handle logical or
        for sub_constraint in constraint.replace("||", "|").split("|"):
            sub_constraint = ",".join(
                [
                    fix_constraint_php(constraint)
                    for constraint in sub_constraint.split(",")
                ]
            )
            constraints.append(sub_constraint)
    elif language == "rust":
        # https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
        constraints = [
            ",".join(
                [
                    fix_constraint_rust(sub_constraint)
                    for sub_constraint in constraint.split(",")
                ]
            )
        ]

    version_constraints = tuple(SpecifierSet(constraint) for constraint in constraints)
    logger.debug(
        "(Analysing {}|{}) Converted {} to pythonic version constraints: {}",
        language,
        package,
        reqs,
        list(map(str, version_constraints)),
    )
    return version_constraints


def constraints_to_string(constraints: tuple[SpecifierSet]) -> str:
    """Converts the specifier set to string"""
    return "||".join(
        ",".join(str(spec) for spec in specifier._specs) or "*"
        for specifier in constraints
    )


def make_url(language: str, package: str, version: Optional[str] = None) -> str:
    """
    Construct the API JSON request URL or web URL to scrape
    Parameters:
        language: lowercase: python, javascript or go
        package: as imported in source
        version: optional version specification
    Return:
          url to fetch
    """
    suffix = ""
    url_elements: tuple[str, ...]
    if language == "python":
        if version:
            url_elements = (
                "https://pypi.org/pypi",
                package,
                version,
                "json",
            )
        else:
            url_elements = ("https://pypi.org/pypi", package, "json")
    elif language == "javascript":
        if version:
            url_elements = ("https://registry.npmjs.org", package, version)
        else:
            url_elements = ("https://registry.npmjs.org", package)
    elif language == "go":
        if version:
            url_elements = ("https://proxy.golang.org", package, "@v", version + ".mod")
        else:
            url_elements = ("https://proxy.golang.org", package, "@v", "list")
    elif language == "cs":
        # Repository expects package name to be lower for it to work reliably
        package = package.lower()
        if version:
            url_elements = (
                "https://api.nuget.org/v3-flatcontainer",
                package,
                version,
                package + ".nuspec",
            )
        else:
            url_elements = (
                "https://api.nuget.org/v3-flatcontainer",
                package,
                "index.json",
            )
    elif language == "php":
        url_elements = ("https://packagist.org/packages", package)
        suffix = ".json"
    elif language == "rust":
        if version:
            url_elements = ("https://crates.io/api/v1/crates", package, version)
        else:
            url_elements = ("https://crates.io/api/v1/crates", package, "versions")
    else:
        raise LanguageNotSupportedError(language)

    return "/".join(url_elements).rstrip("/") + suffix
