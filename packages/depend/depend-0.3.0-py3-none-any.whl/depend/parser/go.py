"""Functions to handle Go files"""
import re

from depend.dep import Dep


def handle_go_mod(go_mod_text):
    require_regex = re.compile(r"^require\s+\(([^)]*)\)", re.MULTILINE)
    requires_all = require_regex.findall(go_mod_text)
    replace_regex = re.compile(r"^replace\s+\(([^)]*)\)", re.MULTILINE)
    replace_all = replace_regex.findall(go_mod_text)
    dependencies = {}
    for single_line in go_mod_text.split("\n"):
        single_line = single_line.strip()
        if "(" not in single_line:
            if single_line.startswith("require"):
                dep_info = single_line.split()
                if len(dep_info) >= 3:
                    dependencies[dep_info[1]] = dep_info[2]
                else:
                    dependencies[dep_info[1]] = None
            elif single_line.startswith("replace"):
                _, good = single_line.split("=>")
                dep_info = good.strip().split()
                if len(dep_info) >= 2:
                    dependencies[dep_info[0]] = dep_info[1]
                else:
                    dependencies[dep_info[0]] = None
    if requires_all:
        for requires in requires_all:
            for require_line in requires.strip().split("\n"):
                require_line = require_line.strip()
                if "//" in require_line:
                    require_line = require_line.split("//")[0]
                require = require_line.split()
                module_name = require[0]
                version = None
                if len(require) > 1:
                    version = require[1]
                dependencies[module_name] = version
    if replace_all:
        for replaces in replace_all:
            for replace_line in replaces.strip().split("\n"):
                replace_line = replace_line.strip()
                if "//" in replace_line:
                    replace_line = replace_line.split("//")[0]
                _, good = replace_line.split("=>")
                dep_info = good.strip().split()
                module_name = dep_info[0]
                version = None
                if len(dep_info) > 1:
                    version = dep_info[1]
                dependencies[module_name] = version
    return [
        Dep("go", dep_name, dep_version)
        for dep_name, dep_version in dependencies.items()
    ]
