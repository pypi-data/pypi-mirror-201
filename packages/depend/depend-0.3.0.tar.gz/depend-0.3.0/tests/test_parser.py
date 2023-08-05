"""Tests for all functions in depend parser."""
from __future__ import annotations

import pytest

import depend.api_handler


@pytest.fixture
def dependency_payload():
    """Generates a fixed payload to test the script"""
    return {"javascript": ["react:0.12.0"], "python": ["pygithub:1.55"]}


def test_make_url_with_version():
    """Check if version specific url is generated for all languages"""
    assert (
        depend.api_handler.make_url("python", "aiohttp", "3.7.2")
        == "https://pypi.org/pypi/aiohttp/3.7.2/json"
    )
    assert (
        depend.api_handler.make_url("javascript", "diff", "5.0.0")
        == "https://registry.npmjs.org/diff/5.0.0"
    )
    assert (
        depend.api_handler.make_url("go", "bufio", "go1.17.6")
        == "https://proxy.golang.org/bufio/@v/go1.17.6.mod"
    )


def test_make_url_without_version():
    """Check if correct url is generated for all languages"""
    assert (
        depend.api_handler.make_url("python", "aiohttp")
        == "https://pypi.org/pypi/aiohttp/json"
    )
    assert (
        depend.api_handler.make_url("javascript", "diff")
        == "https://registry.npmjs.org/diff"
    )
    assert (
        depend.api_handler.make_url("go", "bufio")
        == "https://proxy.golang.org/bufio/@v/list"
    )


# @pytest.mark.asyncio
# async def test_make_vcs_request(result_payload):
#     """Test VCS handler"""
#     depend.api_handler.handle_vcs(
#         "go", "github.com/getsentry/sentry-go", result_payload
#     )
#     assert result_payload["pkg_lic"] == ['BSD 2-Clause "Simplified" License']


# @pytest.mark.asyncio
# async def test_make_vcs_clone_request(result_payload):
#     """Test VCS handler"""
#     depend.api_handler.handle_vcs(
#         "go", "github.com/getsentry/sentry-go", result_payload, True
#     )
#     assert result_payload["pkg_dep"]


# @pytest.mark.asyncio
# async def test_unsupported_vcs_fails(result_payload):
#     """Checks if exception is raised for unsupported pattern"""
#     with pytest.raises(VCSNotSupportedError, match="gitlab"):
#         depend.api_handler.handle_vcs(
#             "go", "gitlab.com/secmask/awserver", result_payload
#         )
