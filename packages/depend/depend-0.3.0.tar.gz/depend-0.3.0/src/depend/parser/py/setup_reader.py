"""
Modification of Setup Reader as implemented by Poetry
https://github.com/python-poetry/poetry/blob/master/src/poetry/utils/setup_reader.py
"""
from __future__ import annotations

import ast
from configparser import ConfigParser
from typing import Any, Iterable, List, Optional, Union

import github
from github.ContentFile import ContentFile
from loguru import logger
from poetry.utils.setup_reader import SetupReader

from depend.dep import Dep
from depend.utils.github import find_github_details_from_url
from depend.utils.python import parse_requirements
from depend.vcs.vcs_helper import get_github

# TODO: there are no logs in this file. What are the changes? Why are they needed?


class LaxSetupReader(SetupReader):
    """
    Read the setup.py file without executing it.
    """

    def auth_read_setup_py(self, content: str) -> list[Dep]:
        """
        Directly read setup.py content
        :param content: content of setup.py
        Return:
          {
            "name": package name,
            "version": package version,
            "install_requires": list of packages required
                or a string with file to be read from repo
            "python_requires": python versions,
            "classifiers": data provided for indexing,
            "license": list of licenses found
        }
        """
        body = ast.parse(content).body
        owner_name, repo_name, branch = find_github_details_from_url(content)
        setup_call, body = self._find_setup_call(body)
        if not setup_call:
            return []

        # Inspecting keyword arguments
        pkg_dep = self._find_install_requires(setup_call, body)
        if isinstance(pkg_dep, str) and repo_name is not None:
            g = get_github()
            logger.info("Repo: {}/{}", owner_name, repo_name)
            # TODO: make this take two args instead
            repo = g.get_repo(f"{owner_name}/{repo_name}")
            commit_branch_tag = branch or repo.default_branch
            try:
                repo_file_content = repo.get_contents(pkg_dep, ref=commit_branch_tag)
                if isinstance(repo_file_content, ContentFile):
                    dep_file = repo_file_content.decoded_content.decode()
                    return parse_requirements(dep_file.splitlines())
            except github.GithubException as e:
                logger.error(e)
        else:
            return parse_requirements(
                pkg_dep.splitlines() if isinstance(pkg_dep, str) else pkg_dep
            )

    def _find_in_dict(self, dict_: ast.Dict, name: str) -> Optional[Any]:
        for key, val in zip(dict_.keys, dict_.values):
            if isinstance(key, ast.Str) and key.s == name:
                return val
        return None

    def _find_single_string(self, call: ast.Call, body: List[Any], name: str) -> str:
        value = self._find_in_call(call, name)
        if value is None:
            # Trying to find in kwargs
            kwargs = self._find_call_kwargs(call)

            if kwargs is None or not isinstance(kwargs, ast.Name):
                return ""

            variable = self._find_variable_in_body(body, kwargs.id)
            if not isinstance(variable, (ast.Dict, ast.Call)):
                return ""

            if isinstance(variable, ast.Call):
                if not isinstance(variable.func, ast.Name):
                    return ""

                if variable.func.id != "dict":
                    return ""

                value = self._find_in_call(variable, name)
            else:
                value = self._find_in_dict(variable, name)

        if value is None:
            return ""

        if isinstance(value, ast.Str):
            return value.s or ""
        if isinstance(value, ast.List):
            out = ""
            for subnode in value.elts:
                if isinstance(subnode, ast.Str):
                    out = out + subnode.s + "\n"
            return out or ""
        elif isinstance(value, ast.Name):
            variable = self._find_variable_in_body(body, value.id)

            if variable is not None and isinstance(variable, ast.Str):
                return variable.s or ""
        return ""

    def _find_install_requires(
        self, call: ast.Call, body: Iterable[Any]
    ) -> Union[List[str], str]:
        """
        Analyze setup.py and find dependencies
        :param call: setup function in setup.py
        :param body: body for variable definitions
        Return:
          package dependencies list or file to query
        """
        install_requires: List[str] = []
        value = self._find_in_call(call, "install_requires")
        if value is None:
            # Trying to find in kwargs
            kwargs = self._find_call_kwargs(call)

            if kwargs is None or not isinstance(kwargs, ast.Name):
                return install_requires

            variable = self._find_variable_in_body(body, kwargs.id)
            if not isinstance(variable, (ast.Dict, ast.Call)):
                return install_requires

            if isinstance(variable, ast.Call):
                if not isinstance(variable.func, ast.Name):
                    return install_requires

                if variable.func.id != "dict":
                    return install_requires

                value = self._find_in_call(variable, "install_requires")
            else:
                value = self._find_in_dict(variable, "install_requires")

        if value is None:
            return install_requires

        elif isinstance(value, ast.List):
            for el_n in value.elts:
                if isinstance(el_n, ast.Name):
                    variable = self.find_variable_in_body(body, el_n.id)

                    if variable is not None and isinstance(variable, ast.List):
                        for el in variable.elts:
                            if isinstance(el, ast.Constant):
                                install_requires.append(el.s)

                    elif variable is not None and isinstance(variable, ast.Constant):
                        install_requires.append(variable.s)

                    # ignores other instances possible
        elif isinstance(value, ast.Name):
            variable = self.find_variable_in_body(body, value.id)

            if variable is not None and isinstance(variable, ast.List):
                for el in variable.elts:
                    if isinstance(el, ast.Constant):
                        install_requires.append(el.s)

            elif variable is not None and isinstance(variable, str):
                return variable

        return install_requires

    def find_variable_in_body(self, body: Iterable[Any], name: str) -> Optional[Any]:
        """
        Considers with body as well
        :param body: ast body to search in
        :param name: variable being searched for
        Return:
          variable value
        """
        for elem in body:
            # checks if filename is found in with
            if (
                isinstance(elem, ast.With)
                and self.find_variable_in_body(elem.body, name) is not None
            ):
                for item in elem.items:
                    if not isinstance(item, ast.withitem):
                        continue
                    cont = item.context_expr
                    if not isinstance(cont, ast.Call):
                        continue
                    func = cont.func
                    if not (isinstance(func, ast.Name) and func.id == "open"):
                        continue
                    for arg in cont.args:
                        if not (isinstance(arg, ast.Constant)):
                            return "check_all_paths"
                        return arg.value

            if not isinstance(elem, ast.Assign):
                continue

            for target in elem.targets:
                if not isinstance(target, ast.Name):
                    continue

                if target.id == name:
                    return elem.value
        return None

    def read_setup_cfg(self, content: str) -> list[Dep]:
        """
        Analyzes content of setup.cfg
        :param content: file content
        Return:
          filtered metadata
        """
        parser = ConfigParser()
        parser.read_string(content)

        dep_info = parser.get("options", "install_requires", fallback="")
        if dep_info and not dep_info.startswith("\n"):
            dep_info = dep_info.split(";")
        else:
            dep_info = dep_info.splitlines()

        return parse_requirements(dep_info)
