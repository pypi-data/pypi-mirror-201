"""Tests output obtained by parsing dependency files"""
from __future__ import annotations

from depend.dep import Dep, RustDep
from depend.parser.go import handle_go_mod
from depend.parser.js import handle_package_json, handle_yarn_lock
from depend.parser.php import handle_composer_json
from depend.parser.py import handle_otherpy, handle_setup_cfg, handle_toml
from depend.parser.rust import handle_cargo_lock, handle_cargo_toml
from depend.utils import nuspec_parser
from depend.utils.python import handle_requirements_txt


def test_go_mod():
    """Check go.mod file output"""
    with open("tests/data/example_go.mod") as f:
        mod_content = f.read()
    result = handle_go_mod(mod_content)
    assert set(result) == {
        Dep(
            "go", "github.com/alecthomas/template", "v0.0.0-20160405071501-a0175ee3bccc"
        ),
        Dep("go", "github.com/alecthomas/units", "v0.0.0-20151022065526-2efee857e7cf"),
        Dep("go", "github.com/gorilla/mux", "v1.6.2"),
        Dep("go", "github.com/sirupsen/logrus", "v1.2.0"),
        Dep("go", "gopkg.in/alecthomas/kingpin.v2", "v2.2.6"),
    }


def test_package_json():
    """Check package.json file output"""
    with open("tests/data/example_package.json") as f:
        json_content = f.read()
    result = handle_package_json(json_content)
    assert set(result) == {
        Dep("javascript", "jshint", "*"),
        Dep("javascript", "imagemin", "*"),
        Dep("javascript", "browser-sync", "*"),
        Dep("javascript", "uglifyjs", "*"),
        Dep("javascript", "watch", "*"),
        Dep("javascript", "cssmin", "*"),
        Dep("javascript", "jscs", "*"),
        Dep("javascript", "uglify-js", "*"),
        Dep("javascript", "browserify", "*"),
        Dep("javascript", "expect.js", "*"),
        Dep("javascript", "should", "*"),
        Dep("javascript", "mocha", "*"),
        Dep("javascript", "istanbul", "*"),
    }


def test_npm_shrinkwrap_json():
    """Check package.json file output"""
    with open("tests/data/example_npm_shrinkwrap.json") as f:
        json_content = f.read()
    result = handle_package_json(json_content)

    assert set(result) == {
        Dep("javascript", "grunt-ember-handlebars", "0.7.0"),
        Dep("javascript", "grunt", "0.4.1"),
        Dep("javascript", "async", "0.1.22"),
        Dep("javascript", "coffee-script", "1.3.3"),
        Dep("javascript", "colors", "0.6.2"),
        Dep("javascript", "dateformat", "1.0.2-1.2.3"),
        Dep("javascript", "eventemitter2", "0.4.13"),
        Dep("javascript", "findup-sync", "0.1.2"),
        Dep("javascript", "lodash", "1.0.1"),
        Dep("javascript", "glob", "3.1.21"),
        Dep("javascript", "graceful-fs", "1.2.3"),
        Dep("javascript", "inherits", "1.0.0"),
        Dep("javascript", "hooker", "0.2.3"),
        Dep("javascript", "iconv-lite", "0.2.11"),
        Dep("javascript", "minimatch", "0.2.12"),
        Dep("javascript", "lru-cache", "2.3.1"),
        Dep("javascript", "sigmund", "1.0.0"),
        Dep("javascript", "nopt", "1.0.10"),
        Dep("javascript", "abbrev", "1.0.4"),
        Dep("javascript", "rimraf", "2.0.3"),
        Dep("javascript", "graceful-fs", "1.1.14"),
        Dep("javascript", "lodash", "0.9.2"),
        Dep("javascript", "underscore.string", "2.2.1"),
        Dep("javascript", "which", "1.0.5"),
        Dep("javascript", "js-yaml", "2.0.5"),
        Dep("javascript", "argparse", "0.1.15"),
        Dep("javascript", "underscore", "1.4.4"),
        Dep("javascript", "underscore.string", "2.3.3"),
        Dep("javascript", "esprima", "1.0.4"),
        Dep("javascript", "grunt-lib-contrib", "0.5.3"),
        Dep("javascript", "zlib-browserify", "0.0.1"),
        Dep("javascript", "lineman", "0.15.0"),
        Dep("javascript", "grunt-contrib-clean", "0.5.0"),
        Dep("javascript", "rimraf", "2.2.2"),
        Dep("javascript", "graceful-fs", "2.0.1"),
        Dep("javascript", "grunt-contrib-coffee", "0.7.0"),
        Dep("javascript", "grunt-contrib-concat", "0.3.0"),
        Dep("javascript", "grunt-contrib-copy", "0.4.1"),
        Dep("javascript", "grunt-contrib-handlebars", "0.5.10"),
        Dep("javascript", "handlebars", "1.0.12"),
        Dep("javascript", "optimist", "0.3.7"),
        Dep("javascript", "wordwrap", "0.0.2"),
        Dep("javascript", "uglify-js", "2.3.6"),
        Dep("javascript", "async", "0.2.9"),
        Dep("javascript", "source-map", "0.1.31"),
        Dep("javascript", "amdefine", "0.1.0"),
        Dep("javascript", "grunt-contrib-jshint", "0.6.4"),
        Dep("javascript", "jshint", "2.1.11"),
        Dep("javascript", "shelljs", "0.1.4"),
        Dep("javascript", "cli", "0.4.5"),
        Dep("javascript", "glob", "3.2.6"),
        Dep("javascript", "inherits", "2.0.1"),
        Dep("javascript", "console-browserify", "0.1.6"),
        Dep("javascript", "grunt-contrib-jst", "0.5.1"),
        Dep("javascript", "grunt-contrib-less", "0.7.0"),
        Dep("javascript", "less", "1.4.2"),
        Dep("javascript", "mime", "1.2.11"),
        Dep("javascript", "request", "2.27.0"),
        Dep("javascript", "qs", "0.6.5"),
        Dep("javascript", "json-stringify-safe", "5.0.0"),
        Dep("javascript", "forever-agent", "0.5.0"),
        Dep("javascript", "tunnel-agent", "0.3.0"),
        Dep("javascript", "http-signature", "0.10.0"),
        Dep("javascript", "assert-plus", "0.1.2"),
        Dep("javascript", "asn1", "0.1.11"),
        Dep("javascript", "ctype", "0.5.2"),
        Dep("javascript", "hawk", "1.0.0"),
        Dep("javascript", "hoek", "0.9.1"),
        Dep("javascript", "boom", "0.4.2"),
        Dep("javascript", "cryptiles", "0.2.2"),
        Dep("javascript", "sntp", "0.2.4"),
        Dep("javascript", "aws-sign", "0.3.0"),
        Dep("javascript", "oauth-sign", "0.3.0"),
        Dep("javascript", "cookie-jar", "0.3.0"),
        Dep("javascript", "node-uuid", "1.4.1"),
        Dep("javascript", "form-data", "0.1.2"),
        Dep("javascript", "combined-stream", "0.0.4"),
        Dep("javascript", "delayed-stream", "0.0.5"),
        Dep("javascript", "mkdirp", "0.3.5"),
        Dep("javascript", "ycssmin", "1.0.1"),
        Dep("javascript", "grunt-lib-contrib", "0.6.1"),
        Dep("javascript", "grunt-contrib-sass", "0.5.0"),
        Dep("javascript", "dargs", "0.1.0"),
        Dep("javascript", "grunt-contrib-cssmin", "0.6.1"),
        Dep("javascript", "clean-css", "1.0.12"),
        Dep("javascript", "grunt-contrib-uglify", "0.2.4"),
        Dep("javascript", "uglify-js", "2.4.1"),
        Dep("javascript", "uglify-to-browserify", "1.0.1"),
        Dep("javascript", "grunt-watch-nospawn", "0.0.3"),
        Dep("javascript", "gaze", "0.3.3"),
        Dep("javascript", "fileset", "0.1.5"),
        Dep("javascript", "config-extend", "0.0.6"),
        Dep("javascript", "testem", "0.5.3"),
        Dep("javascript", "express", "3.1.0"),
        Dep("javascript", "connect", "2.7.2"),
        Dep("javascript", "qs", "0.5.1"),
        Dep("javascript", "formidable", "1.0.11"),
        Dep("javascript", "bytes", "0.1.0"),
        Dep("javascript", "pause", "0.0.1"),
        Dep("javascript", "commander", "0.6.1"),
        Dep("javascript", "range-parser", "0.0.4"),
        Dep("javascript", "mkdirp", "0.3.3"),
        Dep("javascript", "cookie", "0.0.5"),
        Dep("javascript", "buffer-crc32", "0.1.1"),
        Dep("javascript", "fresh", "0.1.0"),
        Dep("javascript", "methods", "0.0.1"),
        Dep("javascript", "send", "0.1.0"),
        Dep("javascript", "mime", "1.2.6"),
        Dep("javascript", "cookie-signature", "0.0.1"),
        Dep("javascript", "debug", "0.7.2"),
        Dep("javascript", "mustache", "0.4.0"),
        Dep("javascript", "socket.io", "0.9.16"),
        Dep("javascript", "socket.io-client", "0.9.16"),
        Dep("javascript", "uglify-js", "1.2.5"),
        Dep("javascript", "ws", "0.4.31"),
        Dep("javascript", "nan", "0.3.2"),
        Dep("javascript", "tinycolor", "0.0.1"),
        Dep("javascript", "options", "0.0.5"),
        Dep("javascript", "xmlhttprequest", "1.4.2"),
        Dep("javascript", "active-x-obfuscator", "0.0.1"),
        Dep("javascript", "zeparser", "0.0.5"),
        Dep("javascript", "policyfile", "0.0.4"),
        Dep("javascript", "base64id", "0.1.0"),
        Dep("javascript", "redis", "0.7.3"),
        Dep("javascript", "winston", "0.7.2"),
        Dep("javascript", "cycle", "1.0.2"),
        Dep("javascript", "eyes", "0.1.8"),
        Dep("javascript", "pkginfo", "0.3.0"),
        Dep("javascript", "request", "2.16.6"),
        Dep("javascript", "form-data", "0.0.10"),
        Dep("javascript", "hawk", "0.10.2"),
        Dep("javascript", "hoek", "0.7.6"),
        Dep("javascript", "boom", "0.3.8"),
        Dep("javascript", "cryptiles", "0.1.3"),
        Dep("javascript", "sntp", "0.1.4"),
        Dep("javascript", "cookie-jar", "0.2.0"),
        Dep("javascript", "aws-sign", "0.2.0"),
        Dep("javascript", "oauth-sign", "0.2.0"),
        Dep("javascript", "forever-agent", "0.2.0"),
        Dep("javascript", "tunnel-agent", "0.2.0"),
        Dep("javascript", "json-stringify-safe", "3.0.0"),
        Dep("javascript", "qs", "0.5.6"),
        Dep("javascript", "stack-trace", "0.0.7"),
        Dep("javascript", "charm", "0.0.8"),
        Dep("javascript", "js-yaml", "2.1.3"),
        Dep("javascript", "tap", "0.4.4"),
        Dep("javascript", "inherits", "2.0.0"),
        Dep("javascript", "yamlish", "0.0.5"),
        Dep("javascript", "slide", "1.1.5"),
        Dep("javascript", "runforcover", "0.0.2"),
        Dep("javascript", "bunker", "0.1.2"),
        Dep("javascript", "burrito", "0.2.12"),
        Dep("javascript", "traverse", "0.5.2"),
        Dep("javascript", "uglify-js", "1.1.1"),
        Dep("javascript", "nopt", "2.1.2"),
        Dep("javascript", "difflet", "0.2.6"),
        Dep("javascript", "traverse", "0.6.6"),
        Dep("javascript", "charm", "0.1.2"),
        Dep("javascript", "deep-is", "0.1.2"),
        Dep("javascript", "deep-equal", "0.0.0"),
        Dep("javascript", "buffer-equal", "0.0.0"),
        Dep("javascript", "backbone", "1.0.0"),
        Dep("javascript", "underscore", "1.5.2"),
        Dep("javascript", "styled_string", "0.0.1"),
        Dep("javascript", "growl", "1.7.0"),
        Dep("javascript", "consolidate", "0.8.0"),
        Dep("javascript", "did_it_work", "0.0.6"),
        Dep("javascript", "fireworm", "0.4.4"),
        Dep("javascript", "commander", "1.3.2"),
        Dep("javascript", "keypress", "0.1.0"),
        Dep("javascript", "express", "3.4.0"),
        Dep("javascript", "connect", "2.9.0"),
        Dep("javascript", "bytes", "0.2.0"),
        Dep("javascript", "uid2", "0.0.2"),
        Dep("javascript", "multiparty", "2.1.8"),
        Dep("javascript", "readable-stream", "1.0.17"),
        Dep("javascript", "stream-counter", "0.1.0"),
        Dep("javascript", "commander", "1.2.0"),
        Dep("javascript", "cookie", "0.1.0"),
        Dep("javascript", "buffer-crc32", "0.2.1"),
        Dep("javascript", "fresh", "0.2.0"),
        Dep("javascript", "send", "0.1.4"),
        Dep("javascript", "cookie-signature", "1.0.1"),
        Dep("javascript", "debug", "0.7.3"),
        Dep("javascript", "http-proxy", "0.10.3"),
        Dep("javascript", "pkginfo", "0.2.3"),
        Dep("javascript", "utile", "0.1.7"),
        Dep("javascript", "deep-equal", "0.1.0"),
        Dep("javascript", "i", "0.3.2"),
        Dep("javascript", "ncp", "0.2.7"),
        Dep("javascript", "rimraf", "1.0.9"),
        Dep("javascript", "coffee-script", "1.6.3"),
        Dep("javascript", "watch_r", "0.0.14"),
        Dep("javascript", "structr", "0.3.2"),
        Dep("javascript", "ejs", "0.8.4"),
        Dep("javascript", "commander", "1.1.1"),
        Dep("javascript", "tq", "0.2.5"),
        Dep("javascript", "hurryup", "0.0.2"),
        Dep("javascript", "comerr", "0.0.6"),
        Dep("javascript", "semver", "2.1.0"),
    }


def test_package_lock_json():
    """Check package.json file output"""
    with open("tests/data/example_package_lock.json") as f:
        json_content = f.read()
    result = handle_package_json(json_content)
    assert set(result) == {
        Dep("javascript", "@f/zip-obj", "1.1.1"),
        # TODO: enable these as GithubDeps
        # Dep(
        #     "javascript",
        #     "@paulcbetts/cld",
        #     "*",
        #     "github:ssbc/paulcbetts-cld-prebuilt#63609a21577c9c44229f16c0f42cf13322035718",
        # ),
        Dep("javascript", "glob", "5.0.15"),
        # TODO: enable these as GithubDeps
        # Dep(
        #     "javascript",
        #     "@paulcbetts/spellchecker",
        #     "*",
        #     "github:ssbc/paulcbetts-spellchecker-prebuilt#8e28e43d81073b354e7811792b9a39132db52221",
        # ),
        Dep("javascript", "@types/node", "8.10.39"),
        Dep("javascript", "abbrev", "1.1.1"),
        Dep("javascript", "abstract-leveldown", "4.0.3"),
        Dep("javascript", "acorn", "5.7.3"),
        Dep("javascript", "acorn-dynamic-import", "4.0.0"),
        Dep("javascript", "acorn-jsx", "3.0.1"),
        Dep("javascript", "acorn", "3.3.0"),
    }


def test_yarn_v1_lock():
    """Check yarn.lock v1 file output"""
    with open("tests/data/example_v1_yarn.lock") as f:
        yarn_content = f.read()
    result = handle_yarn_lock(yarn_content)
    assert set(result) == {
        Dep("javascript", "@babel/code-frame", "7.0.0-beta.55"),
        Dep("javascript", "@babel/highlight", "7.0.0-beta.55"),
        Dep("javascript", "@gulp-sourcemaps/identity-map", "1.0.2"),
        Dep("javascript", "@gulp-sourcemaps/map-sources", "1.0.0"),
        Dep("javascript", "@zkochan/cmd-shim", "3.1.0"),
        Dep("javascript", "abab", "1.0.4"),
        Dep("javascript", "abab", "2.0.0"),
        Dep("javascript", "abbrev", "1.1.1"),
        Dep("javascript", "acorn-dynamic-import", "2.0.2"),
        Dep("javascript", "acorn-globals", "4.1.0"),
        Dep("javascript", "acorn-jsx", "3.0.1"),
        Dep("javascript", "acorn", "5.7.1"),
        Dep("javascript", "yargs", "3.10.0"),
        Dep("javascript", "yn", "2.0.0"),
    }


def test_yarn_v2_lock():
    """Check yarn.lock v2 file output"""
    with open("tests/data/example_v2_yarn.lock") as f:
        yarn_content = f.read()
    result = handle_yarn_lock(yarn_content)
    assert set(result) == {
        Dep("javascript", "@babel/code-frame", "7.5.5"),
        Dep("javascript", "@babel/core", "7.6.0"),
        Dep("javascript", "@babel/core", "7.7.4"),
        Dep("javascript", "@babel/generator", "7.7.4"),
        Dep("javascript", "@babel/helper-annotate-as-pure", "7.7.4"),
        Dep(
            "javascript",
            "@babel/helper-builder-binary-assignment-operator-visitor",
            "7.7.4",
        ),
        Dep("javascript", "@babel/helper-builder-react-jsx", "7.7.4"),
        Dep("javascript", "@babel/helper-call-delegate", "7.7.4"),
        Dep("javascript", "@babel/helper-create-class-features-plugin", "7.7.4"),
        Dep("javascript", "@babel/helper-create-regexp-features-plugin", "7.7.4"),
        Dep("javascript", "@babel/helper-define-map", "7.7.4"),
        Dep("javascript", "@babel/helper-explode-assignable-expression", "7.7.4"),
        Dep("javascript", "@babel/helper-function-name", "7.7.4"),
        Dep("javascript", "@babel/helper-get-function-arity", "7.7.4"),
        Dep("javascript", "@babel/helper-hoist-variables", "7.7.4"),
        Dep("javascript", "@babel/helper-member-expression-to-functions", "7.7.4"),
        Dep("javascript", "@babel/helper-module-imports", "7.7.4"),
        Dep("javascript", "@babel/helper-module-transforms", "7.7.4"),
        Dep("javascript", "@babel/helper-optimise-call-expression", "7.7.4"),
        Dep("javascript", "@babel/helper-plugin-utils", "7.0.0"),
        Dep("javascript", "@babel/helper-regex", "7.5.5"),
        Dep("javascript", "@babel/helper-remap-async-to-generator", "7.7.4"),
        Dep("javascript", "@babel/helper-replace-supers", "7.7.4"),
        Dep("javascript", "yarnv2-storybook", "0.0.0-use.local"),
        Dep("javascript", "@yarnpkg/parsers", "0.0.0-use.local"),
    }


def test_requirements_txt():
    """Check requirements.txt file output"""
    with open("tests/data/example_requirements.txt") as f:
        txt_content = f.read()
    result = handle_requirements_txt(txt_content)
    assert set(result) == {
        Dep("python", "cycler", ">=0.10.0"),
        Dep("python", "kiwisolver", ">1.2.0"),
        Dep("python", "matplotlib", "<3.2.1"),
        Dep("python", "numpy", "!=1.18.5"),
        Dep("python", "pandas", "1.*"),
        Dep("python", "pyparsing", "2.*"),
        Dep("python", "python-dateutil", "2.8.*"),
        Dep("python", "pytz", "~2020"),
        Dep("python", "scipy", "~1.4"),
        Dep("python", "seaborn", "~0.10.1"),
        Dep("python", "six", "^1.15.0"),
        Dep("python", "beautifulsoup4", "^4.6"),
        Dep("python", "certifi", "^2018"),
        Dep("python", "lxml", "<5.7,>4"),
    }


def test_setup_cfg():
    """Check setup.cfg file output"""
    with open("tests/data/example_setup.cfg") as f:
        cfg_content = f.read()
    result = handle_setup_cfg(cfg_content)
    assert set(result) == {Dep("python", "setuptools", ">=30.3.0")}


def test_pyproject_toml():
    """Check toml file output"""
    with open("tests/data/example_pyproject.toml") as f:
        pyproject = f.read()
    result = handle_toml(pyproject)
    assert set(result) == {Dep("python", "numpy", ">=1.18.5")}


def test_poetry_toml():
    """Check poetry toml file output"""
    with open("tests/data/example_pyproject_poetry.toml") as f:
        pyproject = f.read()
    result = handle_toml(pyproject)
    assert set(result) == {
        Dep("python", "gunicorn", "^20.0.4"),
        Dep("python", "flask", "^1.1.1"),
        Dep("python", "flask_restful", "^0.3.8"),
        Dep("python", "spacy", "^2.2.3"),
        Dep("python", "thulac", "^0.2.1"),
        Dep("python", "wiktionaryparser", "^0.0.97"),
    }


def test_other_py():
    """
    Parses conda.yml tox.ini and Pipfiles
    """
    with open("tests/data/example_pipfile") as f:
        pyproject = f.read()
    result = handle_otherpy(pyproject, "Pipfile")
    assert set(result) == {
        Dep("python", "records", ">0.5.0"),
        Dep("python", "nose", "*"),
    }


def test_cs_xml():
    """Parses nuspec files"""
    with open("tests/data/example_package.nuspec") as f:
        nuspec = f.read()
    result = nuspec_parser.handle_nuspec(nuspec)
    assert set(result) == {
        Dep("cs", "Walter.BOM", "2020.8.25.1"),
        Dep("cs", "Microsoft.Extensions.Logging.Abstractions", "3.1.7"),
        Dep("cs", "Microsoft.AspNetCore.Mvc.Core", "2.2.5"),
        Dep("cs", "Microsoft.Extensions.Configuration.Binder", "3.1.7"),
        Dep("cs", "Microsoft.Extensions.FileProviders.Physical", "3.1.7"),
        Dep("cs", "Walter.Cypher", "2020.8.23.1"),
        Dep("cs", "Microsoft.AspNetCore.Http.Features", "3.1.7"),
        Dep("cs", "Microsoft.AspNetCore.Mvc.RazorPages", "2.2.5"),
        Dep("cs", "Microsoft.Extensions.DependencyInjection.Abstractions", "3.1.7"),
        Dep("cs", "Walter", "2020.8.23.1"),
        Dep("cs", "Walter.Net.Networking", "2020.8.25.1"),
        Dep("cs", "Walter.Web.FireWall.SqlDataTools", "2020.8.25.1"),
        Dep("cs", "Newtonsoft.Json", "12.0.3"),
        Dep("cs", "Microsoft.Extensions.Identity.Core", "3.1.7"),
        Dep("cs", "Microsoft.AspNetCore.Routing", "2.2.2"),
        Dep("cs", "Walter.Net.LookWhosTalking", "2020.8.25.1"),
        Dep("cs", "Microsoft.Extensions.Caching.Abstractions", "3.1.7"),
        Dep("cs", "System.Configuration.ConfigurationManager", "4.7.0"),
    }


def test_composer_json():
    """Check composer json file output"""
    with open("tests/data/example_composer.json") as f:
        php_project = f.read()
    result = handle_composer_json(php_project)
    assert set(result) == {
        Dep("php", "filament/filament", "^2.10"),
        Dep("php", "illuminate/contracts", "^9.0"),
        Dep("php", "spatie/laravel-package-tools", "^1.9.2"),
    }


def test_cargo_toml():
    """Check cargo toml file output"""
    with open("tests/data/example_cargo.toml") as f:
        rust_project = f.read()
    result = handle_cargo_toml(rust_project)
    assert set(result) == {
        RustDep("rust", "whoami", "=1.2"),
        RustDep("rust", "sys-locale", "0.2"),
        RustDep("rust", "serde_derive", "1.0"),
        RustDep("rust", "serde", "1.0"),
        RustDep("rust", "serde_json", "1.0"),
        RustDep("rust", "cfg-if", "1.0"),
        RustDep("rust", "lazy_static", "1.4"),
        RustDep("rust", "sha2", "0.10"),
        RustDep("rust", "repng", "0.2"),
        RustDep("rust", "libc", "0.2"),
        # TODO: enable these as GithubDeps
        # Dep(
        #     "rust",
        #     "parity-tokio-ipc",
        #     "*",
        #     "https://github.com/open-trade/parity-tokio-ipc||",
        # ),
        RustDep("rust", "flexi_logger", "0.22"),
        RustDep("rust", "runas", "0.2"),
        # TODO: enable these as GithubDeps
        # Dep("rust", "magnum-opus", "*", "https://github.com/open-trade/magnum-opus||"),
        RustDep("rust", "async-trait", "0.1"),
        RustDep("rust", "crc32fast", "1.3"),
        RustDep("rust", "clap", "3.0"),
        RustDep("rust", "rpassword", "6.0"),
        RustDep("rust", "base64", "0.13"),
        RustDep("rust", "sysinfo", "0.23"),
        RustDep("rust", "num_cpus", "1.13"),
        RustDep("rust", "samplerate", "0.2"),
        RustDep("rust", "uuid", "0.8", features=["v4"]),
        RustDep("rust", "rubato", "0.12"),
        RustDep(
            "rust",
            "dasp",
            "0.11",
            features=["signal", "interpolate-linear", "interpolate"],
        ),
    }


def test_cargo_lock():
    """Check poetry toml file output"""
    with open("tests/data/example_cargo.lock") as f:
        rust_project = f.read()
    result = handle_cargo_lock(rust_project)
    assert set(result) == {
        RustDep("rust", "addr2line", "0.17.0"),
        RustDep("rust", "adler", "1.0.2"),
        RustDep("rust", "adler32", "1.2.0"),
        RustDep("rust", "aho-corasick", "0.7.18"),
        RustDep("rust", "alsa", "0.6.0"),
        RustDep("rust", "alsa-sys", "0.3.1"),
        RustDep("rust", "android_log-sys", "0.2.0"),
        RustDep("rust", "android_logger", "0.11.0"),
        RustDep("rust", "ansi_term", "0.12.1"),
        RustDep("rust", "anyhow", "1.0.56"),
        RustDep("rust", "arboard", "2.0.1"),
        RustDep("rust", "async-trait", "0.1.52"),
        RustDep("rust", "atk", "0.9.0"),
        RustDep("rust", "atk-sys", "0.10.0"),
    }
