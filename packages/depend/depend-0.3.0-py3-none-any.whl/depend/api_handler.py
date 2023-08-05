from __future__ import annotations

from loguru import logger

from depend.dep import Dep, RustDep
from depend.errors import LanguageNotSupportedError
from depend.helper import make_url
from depend.parser.go import handle_go_mod
from depend.parser.js import handle_npm_json
from depend.utils.nuspec_parser import parse_nuspec
from depend.utils.python import parse_requirements

# from github import GithubException
# from depend.constants import DEP_FIELDS_MISSED, LICENSE_DICT, LICENSE_FILES, REQ_FILES
# from depend.parser import handle_dep_file_content
# from depend.utils.github import find_github_details_from_url
# from depend.vcs.github_worker import GithubRequestHandler


class APIHandler:
    def __init__(self, package, async_client):
        self.language = package.language
        self.package = package.name
        self.dependency = package
        self.version = package.version
        self.client = async_client
        self.api_url = make_url(self.language, self.package, self.version)
        self.api_response = None
        self.red_url = self.api_url

    async def get_direct_dependencies(self) -> list[Dep]:
        headers = {
            "User-Agent": "depend (https://github.com/deepsourcelabs/depend)",
        }
        self.api_response = await self.client.get(self.api_url, headers=headers)
        logger.debug("API: Queried {} for version list", self.red_url)
        # Collect repo if available to do vcs query if data incomplete
        if self.language == "python":
            return self.handle_pypi()
        elif self.language == "javascript":
            return self.handle_npmjs()
        elif self.language == "cs":
            return self.handle_cs()
        elif self.language == "php":
            return self.handle_php()
        elif self.language == "rust":
            return await self.handle_rust()
        elif self.language == "go":
            return await self.handle_go()

        raise LanguageNotSupportedError

    def handle_pypi(self) -> list[Dep]:
        """
        Take api response and return required results object
        """
        data = self.api_response.json()
        dependencies_list = data.get("info", {}).get("requires_dist")
        if dependencies_list:
            return parse_requirements(dependencies_list)

        return []

    def handle_cs(self) -> list[Dep]:
        """
        Take api response and return required results object
        """
        req_file_data = self.api_response.text
        return parse_nuspec(req_file_data)

    def handle_npmjs(self) -> list[Dep]:
        """
        Take api response and return required results object
        """

        return handle_npm_json(self.api_response.json())

    def handle_php(self):
        """
        Take api response and return required results object
        """
        data = self.api_response.json()
        versions = data.get("package", {}).get("versions")
        ver_data = versions.get(self.version, {})
        dep_data = ver_data.get("require", {})
        # remove php's version
        if "php" in dep_data:
            del dep_data["php"]

        dependencies = [Dep("php", dep, version) for (dep, version) in dep_data.items()]
        return dependencies

    async def handle_rust(self) -> list[RustDep]:
        """
        Take api response and return required results object
        """
        queried_data = self.api_response.json()
        features_or_deps = {"default", *self.dependency.dep.features}
        feature_deps_map = queried_data["version"].get("features", {})
        # These deps are the optional dependencies that have to be stored as well,
        # because the features we care about contain these.
        extra_deps = set()

        unprocessed_features_or_deps = features_or_deps.copy()
        # This will ensure that we don't recurse multiple times on a feature
        seen_features_or_deps = set()
        while unprocessed_features_or_deps:
            # This holds the nested features yet to be processed
            sub_deps = set()

            for feature in unprocessed_features_or_deps:
                if feature in feature_deps_map:
                    feature_deps = set(feature_deps_map[feature])
                    if not feature_deps:
                        logger.debug(
                            "({}:{}) {!r} is a feature with no deps",
                            self.package,
                            self.version,
                            feature,
                        )
                        continue

                    logger.debug(
                        "({}:{}) {!r} is a feature with deps: {}",
                        self.package,
                        self.version,
                        feature,
                        feature_deps,
                    )
                    for feature_dep in feature_deps:
                        if feature_dep in seen_features_or_deps:
                            logger.debug(
                                "({}:{}) feature {}'s sub-dep {!r} which we have already seen",
                                self.package,
                                self.version,
                                feature,
                                feature_dep,
                            )
                        else:
                            sub_deps.add(feature_dep)
                            seen_features_or_deps.add(feature_dep)
                            logger.debug(
                                "({}:{}) feature {}'s sub-dep {!r} will be queried",
                                self.package,
                                self.version,
                                feature,
                                feature_dep,
                            )

                else:
                    # Default might not be listed in features, assume default = []
                    if feature == "default":
                        continue

                    # If it isn't a sub-feature, it is a dependency
                    if feature.startswith("dep:"):
                        dep = feature[4:]
                    else:
                        dep = feature
                    extra_deps.add(dep)
                    logger.debug(
                        "({}:{}) Storing {!r} as an extra dependency",
                        self.package,
                        self.version,
                        dep,
                    )

            unprocessed_features_or_deps = sub_deps

        dependencies = []
        dep_url = self.api_url + "/dependencies"
        dep_res = await self.client.get(dep_url)
        data = dep_res.json()

        for dependency_data in data.get("dependencies", []):
            package = dependency_data["crate_id"]
            version = dependency_data["req"]
            features = dependency_data["features"]
            kind = dependency_data["kind"]
            is_optional = dependency_data["optional"]
            if kind == "dev":
                logger.debug(
                    "({}:{}) Skipping {}:{} as it is a dev dependency",
                    self.package,
                    self.version,
                    package,
                    version,
                )
                continue

            if is_optional and package not in extra_deps:
                # Optional dependency, but not part of the features we care about
                logger.debug(
                    "({}:{}) Skipping {}:{} as it is not part of current features",
                    self.package,
                    self.version,
                    package,
                    version,
                )
                continue

            dependencies.append(RustDep("rust", package, version, features))
            logger.debug(
                "({}:{}) Adding {}:{} as a dependency",
                self.package,
                self.version,
                package,
                version,
            )

        return dependencies

    async def handle_go(self) -> list[Dep]:
        """
        Take api response and return required results object
        """
        return handle_go_mod(self.api_response.text)
