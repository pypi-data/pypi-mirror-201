"""Tests output obtained by parsing version info across languages"""
from __future__ import annotations

import pytest
from packaging.specifiers import SpecifierSet

from depend.dep import Dep
from depend.resolver import Resolver


@pytest.mark.parametrize(
    ("language", "constraints", "expected"),
    [
        # Caret requirements
        ("python", "^1.2.3", ">=1.2.3,<2.0.0"),
        ("python", "^1.2", ">=1.2.0,<2.0.0"),
        ("python", "^1", ">=1.0.0,<2.0.0"),
        ("python", "^0.2.3", ">=0.2.3,<0.3.0"),
        ("python", "^0.0.3", ">=0.0.3,<0.0.4"),
        ("python", "^0.0", ">=0.0.0,<0.1.0"),
        ("python", "^0", ">=0.0.0,<1.0.0"),
        # Tilde requirements
        ("python", "~1.2.3", ">=1.2.3,<1.3.0"),
        ("python", "~1.2", ">=1.2.0,<1.3.0"),
        ("python", "~1", ">=1.0.0,<2.0.0"),
        ("python", "~0.3.2", ">=0.3.2,<0.4.0"),
        ("python", "~0.0.5", ">=0.0.5,<0.1.0"),
        # exact same logic for JavaScript
        ("javascript", "^1.2.3", ">=1.2.3,<2.0.0"),
        ("javascript", "^1.2", ">=1.2.0,<2.0.0"),
        ("javascript", "^1", ">=1.0.0,<2.0.0"),
        ("javascript", "^0.2.3", ">=0.2.3,<0.3.0"),
        ("javascript", "^0.0.3", ">=0.0.3,<0.0.4"),
        ("javascript", "^0.0", ">=0.0.0,<0.1.0"),
        ("javascript", "^0", ">=0.0.0,<1.0.0"),
        ("javascript", "~1.2.3", ">=1.2.3,<1.3.0"),
        ("javascript", "~0.3.2", ">=0.3.2,<0.4.0"),
        # exact requirements
        ("javascript", "1.2.3", "==1.2.3"),
        # wildcard requirements
        ("javascript", "1.2.x", "==1.2.*"),
        ("javascript", "*", ""),
        ("javascript", "", ""),
        ("javascript", "1.2.3 - 1.2.5", ">=1.2.3,<=1.2.5"),
        (
            "javascript",
            "1.2 <1.2.1||2.x < 2.3 < 2.2",
            "==1.2,<1.2.1||==2.*,<2.3.0,<2.2.0",
        ),
        # Go Minimum version specification
        ("go", "v1.2.3", "==v1.2.3"),
        # C# set bassed notation
        ("cs", "1.0", ">=1.0"),
        ("cs", "(1.0,)", ">1.0"),
        ("cs", "[1.0]", "==1.0"),
        ("cs", "(,1.0]", "<=1.0"),
        ("cs", "(,1.0)", "<1.0"),
        ("cs", "[1.0,2.0]", ">=1.0,<=2.0"),
        ("cs", "(1.0,2.0)", ">1.0,<2.0"),
        ("cs", "[1.0,2.0)", ">=1.0,<2.0"),
        ("php", "^1.2.3", ">=1.2.3,<2.0.0"),
        ("php", "^0.3", ">=0.3.0,<0.4.0"),
        ("php", "^0.0.3", ">=0.0.3,<0.0.4"),
        ("php", "1.0.0 - 2.1.0", ">=1.0.0,<=2.1.0"),
        ("php", "~1.2", ">=1.2,<2.0.0"),
        ("php", "~1.2.3", ">=1.2.3,<1.3.0"),
        ("rust", "1.2.3", ">=1.2.3,<2.0.0"),
        ("rust", "1.2", ">=1.2.0,<2.0.0"),
        ("rust", "1", ">=1.0.0,<2.0.0"),
        ("rust", "0.2.3", ">=0.2.3,<0.3.0"),
        ("rust", "0.2", ">=0.2.0,<0.3.0"),
        ("rust", "0.0.3", ">=0.0.3,<0.0.4"),
        ("rust", "0.0", ">=0.0.0,<0.1.0"),
        ("rust", "0", ">=0.0.0,<1.0.0"),
        # alt syntax for carets
        ("rust", "^0.2.3", ">=0.2.3,<0.3.0"),
        ("rust", "~1.2.3", ">=1.2.3,<1.3.0"),
        ("rust", "~1.2", ">=1.2.0,<1.3.0"),
        ("rust", "~1", ">=1.0.0,<2.0.0"),
        # TODO: ~ in Python[poetry], JavaScript
        # TODO: Ignores git and URL dependencies
        # TODO: Ignores directives other than require in Go
        # TODO: Ignores stability constraints in PHP
    ],
)
def test_simple_dependency_parsing(language, constraints, expected, async_client):
    """Test direct single entry logical conversion of requirement constraints"""
    resolver = Resolver(Dep(language, "test", constraints), async_client)
    assert resolver.version_constraints == tuple(
        SpecifierSet(cons) for cons in expected.split("||")
    )


@pytest.mark.parametrize(
    ("language", "constraints", "expected"),
    [
        # logical ORs
        ("javascript", "<1.2.3 || <1.2.2", "<1.2.3"),
        ("php", "1.0.*", ">=1.0,<1.1"),
        ("php", ">=1.0 <1.1 || <=1.0", "1.0.*"),
        ("rust", "*", ">=0.0.0"),
        ("rust", "1.*", ">=1.0.0,<2.0.0"),
        ("rust", "1.2.*", ">=1.2.0,<1.3.0"),
    ],
)
def test_equivalent_dependency_parsing(language, constraints, expected, async_client):
    """Tests equivalent version resolutions when latest compatible ver is to be considered"""
    resolver = Resolver(Dep(language, "test", constraints), async_client)
    req_resolver = Resolver(Dep(language, "test", expected), async_client)
    vers = [".".join(list(str(ver).rjust(3, "0"))) for ver in range(0, 1000)]
    assert resolver.resolve_version(vers) == req_resolver.resolve_version(vers)
