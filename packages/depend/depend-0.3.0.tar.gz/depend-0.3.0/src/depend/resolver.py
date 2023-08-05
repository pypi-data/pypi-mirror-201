"""
Async Resolver
Takes Lang Package & Version Constraint
Returns dependencies with final constraints and obtained data
"""
from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Optional

import httpx
from httpx import AsyncClient
from loguru import logger
from packaging.version import InvalidVersion, Version

from depend.api_handler import APIHandler
from depend.caching_client import CachingClient
from depend.dep import Dep, ResolvedDep
from depend.helper import constraints_to_string, make_url
from depend.parser import handle_dep_file
from depend.plugins import Plugin, get_plugins


class Resolver:
    def __init__(self, dependency: Dep, client: AsyncClient) -> None:
        self.language = dependency.language
        self.package = dependency.name
        self.dependency = dependency
        self.client = client
        self.versions = []
        self.version_constraints = dependency.constraints
        self.versions_url = make_url(self.language, self.package)
        self.redirect_url = self.versions_url

    async def get_versions(self):
        response = await self.client.get(self.versions_url)
        if self.language in ("python", "rust", "javascript", "cs", "php"):
            self._default_versions(response)
        elif self.language == "go":
            self._go_versions(response)
        if response.status_code != 200:
            logger.error(
                "{}: Queried {} for version list",
                response.status_code,
                self.redirect_url,
            )
        return self.versions

    def _default_versions(self, api_response):
        """Default API query structure for obtaining versions"""
        if api_response.status_code == 404:
            return []
        data = api_response.json()

        if self.language == "python":
            self.versions = list(data.get("releases", {}))
        elif self.language == "rust":
            self.versions = [version["num"] for version in data.get("versions", {})]
        elif self.language == "javascript":
            self.versions = list(data.get("versions", {}))
        elif self.language == "cs":
            self.versions = data.get("versions", [])
        elif self.language == "php":
            self.versions = list(data.get("package", {}).get("versions", {}))

    def _go_versions(self, api_response):
        """
        Get list of all versions for go package
        Parameters:
            client: httpx client
        Return:
              list of versions
        """
        if api_response.status_code != 200:
            return []
        self.versions = api_response.text.split()

    def resolve_version(self, versions: list[str]) -> Optional[str]:
        """
        Returns latest suitable version from available metadata
        Return:
              specific version to query defaults to latest
        """
        if versions is None:
            return None
        compatible_vers = versions
        or_compatible = []
        for req in self.version_constraints:
            or_compatible.extend([ver for ver in compatible_vers if req.contains(ver)])
        if or_compatible:
            sorted_vers = sorted(
                or_compatible,
                key=try_version,
                reverse=True,
            )
            return sorted_vers[0]
        else:
            return None


async def resolve_package(dependency: Dep, client: AsyncClient) -> ResolvedDep | None:
    """
    Resolve vers
    Parameters:
        dependency: unresolved dependency
        client: httpx async client
        all_ver: all versions queried if version not supplied
    Return:
          result object with name version license and dependencies
    """
    resolver = Resolver(dependency, client)
    # Get all available versions for specified package
    versions = await resolver.get_versions()
    if not versions:
        logger.warning(
            "No versions found for package {} with constraints {}",
            dependency.name,
            dependency.constraints,
        )
        return None

    resolved_version = resolver.resolve_version(versions)
    if resolved_version is None:
        logger.warning(
            "No version could be resolved for package {} with constraints {}",
            dependency.name,
            dependency.constraints,
        )
        return None

    logger.debug(
        "(Analysing {}|{}) Resolved version {} from available versions: {} "
        "using constraints {}",
        dependency.language,
        dependency.name,
        resolved_version,
        versions,
        list(map(str, resolver.version_constraints)),
    )

    return ResolvedDep.from_dep(dependency, resolved_version)


async def work_with_vers(
    package: Dep,
    client: AsyncClient,
    plugins: list[Plugin],
) -> dict:
    """Obtain package dependency information, and information from other plugins."""
    rem_dep: set[Dep] = set()
    # Construct URL for version specific data
    api_handler = APIHandler(package, client)
    dependencies = await api_handler.get_direct_dependencies()
    rem_dep |= set(dependencies)
    # TODO: x are not queried part is redundant and most probably wrong
    logger.debug(
        "APIHandler ({}:{}): depends on {} of which {} are not queried",
        package.name,
        package.version,
        dependencies,
        rem_dep,
    )

    resolved_data = {
        "pkg_dep": [
            f"{dep.name}:{constraints_to_string(dep.constraints)}"
            for dep in dependencies
        ],
    }

    for plugin in plugins:
        resolved_data[plugin.key] = await plugin.resolve(
            package.language, package.name, package.version, resolved_data
        )

    return package.name, package.version, resolved_data, rem_dep


def resolve_dep_file(file):
    return handle_dep_file(file)


async def make_multiple_requests(packages: list[Dep], depth: int | None) -> dict:
    """
    Obtain license and dependency information for list of packages.
    Parameters:
        language: python, javascript or go
        package_list: a list of dependencies in each language
        depth: depth of recursion, None for no limit and 0 for input parsing alone
        result: optional result object to append to during recursion
    Return:
          result object with name version license and dependencies
    """
    return await _make_multiple_requests(
        packages,
        depth,
        result=defaultdict(dict),
        _already_queried=set(),
    )


async def _make_multiple_requests(
    packages: list[Dep],
    depth: int | None,
    result: defaultdict,
    _already_queried: set,
) -> dict:
    """
    Recursive implementation of make_multiple_requests, with caching.
    Parameters:
        _already_queried: set that keeps track of queried packages
    """
    deps = set()
    limits = httpx.Limits(
        max_keepalive_connections=None, max_connections=10, keepalive_expiry=None
    )
    async with CachingClient(follow_redirects=True, limits=limits) as client:
        futures = []
        for dependency in packages:
            futures.append(asyncio.ensure_future(resolve_package(dependency, client)))
            _already_queried.add(dependency)
        resolved_deps: list[ResolvedDep] = await asyncio.gather(*futures)

        plugins = get_plugins(client)
        tasks = []
        for resolved_dep in resolved_deps:
            if resolved_dep is None:
                continue

            fetched_versions = result.get(resolved_dep.name)
            if fetched_versions is None or resolved_dep.version not in fetched_versions:
                tasks.append(
                    asyncio.ensure_future(
                        work_with_vers(
                            resolved_dep,
                            client,
                            plugins,
                        )
                    )
                )
        final_results = await asyncio.gather(*tasks)
        for package, version, package_data, direct_deps in final_results:
            result[package][version] = package_data
            deps = deps.union(direct_deps)
        deps.difference_update(_already_queried)
        if len(deps) > 0 and depth is None:
            logger.debug("Invoking multiple requests for list: {}", list(deps))
            return await _make_multiple_requests(
                list(deps),
                depth,
                result,
                _already_queried,
            )
        elif len(deps) > 0 and isinstance(depth, int) and depth > 0:
            logger.debug(
                "({} Until Recursion Limit) Invoking multiple requests for list: {}",
                depth,
                list(deps),
            )
            logger.debug("Invoking multiple requests for {}", list(deps))
            return await _make_multiple_requests(
                list(deps),
                depth - 1,
                result,
                _already_queried=_already_queried,
            )

    if not (len(deps) == 0 or depth == 0):
        raise AssertionError
    return dict(result)


def try_version(value):
    """If version parsing fails defer the version"""
    try:
        return Version(value)
    except InvalidVersion:
        pass

    if "-" in value:
        ver, pre_release = value.split("-")
        pre_release_number = ""
        for i in pre_release:
            if str.isdigit(i):
                pre_release_number += i
            if i == "." and pre_release_number:
                break
        try:
            return Version(f"{ver}-rc.{pre_release_number}")
        except InvalidVersion:
            pass

    return Version("0.0.0")
