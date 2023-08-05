"""Test overall pipeline for depend"""
from __future__ import annotations

import pytest
from jsonschema import validate

from depend import Depend
from depend.errors import LanguageNotSupportedError


class Helpers:
    """Helpers for test"""

    @staticmethod
    def is_valid(json_list):
        """Sets up schema check"""
        j_schema = {
            "type": "object",
            "patternProperties": {
                r"^$|^[\S]+$": {
                    "description": "pkg_name",
                    "type": "object",
                    "patternProperties": {
                        r"^$|^[\S]+$": {
                            "description": "pkg_ver",
                            "type": "object",
                            "properties": {
                                "import_name": {"type": "string"},
                                "lang_ver": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "pkg_lic": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "pkg_err": {"type": "object"},
                                "pkg_dep": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "timestamp": {"type": "string"},
                            },
                            "additionalProperties": False,
                        }
                    },
                },
            },
        }
        validate(instance=json_list, schema=j_schema)
        return True


@pytest.fixture
def json_schema():
    """Schema helper functions"""
    return Helpers


def test_cs(json_schema):
    """C# fetching test"""
    result = Depend(
        language="cs",
        packages="System.IO:4.3.0",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result.keys()) == {
        "Microsoft.NETCore.Platforms",
        "System.Runtime",
        "System.IO",
        "Microsoft.NETCore.Targets",
        "System.Text.Encoding",
        "System.Threading.Tasks",
    }


def test_go(json_schema):
    """Go fetching test"""
    result = Depend(
        language="go",
        packages="github.com/sirupsen/logrus",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result.keys()) == {
        "github.com/pmezard/go-difflib",
        "github.com/davecgh/go-spew",
        "github.com/stretchr/objx",
        "github.com/sirupsen/logrus",
        "github.com/stretchr/testify",
    }


def test_js(json_schema):
    """JavaScript fetching test"""
    result = Depend(
        language="javascript",
        packages="uri-js:<=4.4.1,ajv:8.11.0",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result.keys()) == {
        "json-schema-traverse",
        "uri-js",
        "require-from-string",
        "punycode",
        "fast-deep-equal",
        "ajv",
    }


def test_php(json_schema):
    """PHP fetching test"""
    result = Depend(
        language="php",
        packages="nunomaduro/collision:^5.0",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result.keys()) == {
        "symfony/polyfill-ctype",
        "symfony/service-contracts",
        "psr/log",
        "symfony/polyfill-intl-normalizer",
        "psr/container",
        "symfony/console",
        "symfony/polyfill-php80",
        "symfony/polyfill-php73",
        "nunomaduro/collision",
        "facade/ignition-contracts",
        "symfony/string",
        "symfony/polyfill-mbstring",
        "filp/whoops",
        "symfony/polyfill-intl-grapheme",
        "symfony/deprecation-contracts",
    }


def test_python(json_schema):
    """Python fetching test"""
    result = Depend(
        language="python",
        packages="pygit2:==1.9.2",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result.keys()) == {
        "cached-property",
        "pycparser",
        "pygit2",
        "cffi",
    }


def test_rust(json_schema):
    """Rust fetching test"""
    result = Depend(
        language="rust",
        packages="flate2:=1.0.25",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result) == {"flate2", "miniz_oxide", "crc32fast", "adler", "cfg-if"}
    assert len(result) == 5

    # With features
    result = Depend(
        language="rust",
        packages="flate2:=1.0.25|zlib",
    ).resolve()
    result.pop("_", None)
    assert json_schema.is_valid(result)
    assert set(result) == {
        "flate2",
        "miniz_oxide",
        "crc32fast",
        "adler",
        "cfg-if",
        "cc",
        "pkg-config",
        "libc",
        "libz-sys",
        "vcpkg",
    }
    assert len(result) == 10


def test_unsupported_language_fails():
    """Checks if exception is raised for unsupported language"""
    with pytest.raises(LanguageNotSupportedError, match="bhailang"):
        Depend(
            language="bhailang",
            packages="foo",
        ).resolve()
