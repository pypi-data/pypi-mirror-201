from __future__ import annotations

import asyncio
import os
import pathlib
from typing import Optional

from loguru import logger

from depend.dep import Dep, RustDep
from depend.errors import FileNotSupportedError
from depend.resolver import make_multiple_requests, resolve_dep_file


class Depend:
    def __init__(
        self,
        packages: str | list[Dep],
        language: str,
        depth: Optional[int] = None,
        debug=False,
    ):
        self.language = language

        self.packages = []
        if isinstance(packages, list):
            self.packages = packages
        else:
            for package_str in packages.split(","):
                name, has_version, version = package_str.partition(":")
                if not has_version:
                    version = "*"
                if language == "rust":
                    if has_version:
                        version, *features = version.split("|")
                    else:
                        name, *features = name.split("|")
                    self.packages.append(RustDep(language, name, version, features))
                else:
                    self.packages.append(Dep(language, name, version))

        self.depth = depth
        self.result = {}
        if debug:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError as e:
                if str(e).startswith("There is no current event loop in thread"):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                else:
                    raise
            loop.set_debug = True

    @classmethod
    def from_dep_file(cls, file: pathlib.Path, *args, **kwargs):
        if not os.path.isfile(file):
            raise FileNotSupportedError(
                "Dependency information missing, please provide a valid dep_file or packages"
            )
        packages = resolve_dep_file(file)
        file_extension = os.path.basename(file).split(".")[-1]
        if file_extension == "lock" or "lock" in os.path.basename(file):
            raise ValueError("Lockfiles are not supported right now")
            # TODO: don't resolve lockfiles. They're already resolved.
            # Use their data directly.

            # logger.debug(
            #     "Using list of dependencies from lock file: {}",
            #     packages,
            # )
            # cls(packages, *args, depth=1, **kwargs)
        return cls(packages, *args, **kwargs)

    def resolve(self):
        logger.debug(
            "Recursively analysing list of {} dependencies: {}",
            self.language,
            self.packages,
        )
        self.result.update(
            asyncio.run(
                make_multiple_requests(self.packages, self.depth),
            )
        )
        return self.result
