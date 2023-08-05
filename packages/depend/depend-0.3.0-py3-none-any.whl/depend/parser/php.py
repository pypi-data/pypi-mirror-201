"""Functions to handle PHP files"""
from __future__ import annotations

import json

from depend.dep import Dep


def handle_composer_json(req_file_data: str) -> list[Dep]:
    """
    Parse composer json files required by php
    :param req_file_data: Content of package.json
    Return:
          list of requirement and specs
    """
    package_data = json.loads(req_file_data)
    dep_data = package_data.get("require", {})
    return [
        Dep("php", package, version)
        for (package, version) in dep_data.items()
        if package != "php"
    ]
