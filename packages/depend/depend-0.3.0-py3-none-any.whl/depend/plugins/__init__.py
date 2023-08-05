from __future__ import annotations

import sys
from typing import ClassVar

from depend.plugins.license import LicensePlugin

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    Protocol = object


# TODO: make language a Literal union
class Plugin(Protocol):
    key: ClassVar[str]

    def resolve(self, language: str, package: str, version: str, context: dict) -> str:
        ...


def get_plugins(client):
    return [LicensePlugin(client)]
