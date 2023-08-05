"""Test depend cli"""
from __future__ import annotations

import json

from typer.testing import CliRunner

from depend.cli import app


def test_cli():
    """Normal invocation of the CLI"""
    runner = CliRunner()
    result = runner.invoke(app, ["--lang", "python", "--packages", "zxpy"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data["zxpy"]) == 1
    version, _ = data["zxpy"].popitem()
    assert version >= "1.6"


def test_file():
    """Normal invocation but with dependency file"""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--lang",
            "cs",
            "--dep-file",
            "tests/data/example_package_small.nuspec",
            "--depth",
            "0",
        ],
    )
    assert result.exit_code == 0


def test_err():
    """File based invocation but invalid type passed"""
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        [
            "--lang",
            "cs",
            "--dep-file",
            "data/example_file.unknown",
        ],
    )
    assert result.exit_code == -1
