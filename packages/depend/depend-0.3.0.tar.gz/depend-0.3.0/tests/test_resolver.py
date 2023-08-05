"""Tests for all functions in depend resolver."""
from __future__ import annotations

import asyncio

import httpx
import pytest
import pytest_asyncio

import depend.resolver
from depend.dep import Dep, RustDep


@pytest.fixture
def dependency_payload():
    """Generates a fixed payload to test the script"""
    return [Dep("javascript", "react", "0.12.0"), Dep("python", "pygithub", "1.55")]


@pytest_asyncio.fixture
async def async_client():
    """Generates a httpx client to test the script"""
    limits = httpx.Limits(
        max_keepalive_connections=None, max_connections=10, keepalive_expiry=None
    )
    async with httpx.AsyncClient(follow_redirects=True, limits=limits) as client:
        yield client


@pytest.mark.asyncio
async def test_make_single_request_py(async_client):
    """Test version and license for python"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("python", "aiohttp", "3.7.2"), client=async_client
    )
    assert resolved_dep.version == "3.7.2"


@pytest.mark.asyncio
async def test_make_single_request_js(async_client):
    """Test version and license for javascript"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("javascript", "react", "17.0.2"), client=async_client
    )
    assert resolved_dep.version == "17.0.2"


@pytest.mark.asyncio
async def test_make_single_request_go(async_client):
    """Test version and license for go"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("go", "github.com/getsentry/sentry-go", "v0.12.0"),
        client=async_client,
    )
    assert resolved_dep.version == "v0.12.0"


# @pytest.mark.asyncio
# async def test_make_single_request_go_github(async_client):
#     """Test version and license for go GitHub fallthrough"""
#     resolved_dep = await depend.resolver.resolve_package(
#         Dep("go", "gopkg.in/yaml.v3", "*", repo="https://github.com/go-yaml/yaml"),
#         client=async_client,
#     )
#     assert resolved_dep.repo


@pytest.mark.asyncio
async def test_make_single_request_rust(async_client):
    """Test version and license for javascript"""
    resolved_dep = await depend.resolver.resolve_package(
        RustDep("rust", "reqrnpdno", "*"), client=async_client
    )
    assert resolved_dep.version


@pytest.mark.asyncio
async def test_make_single_request_rust_ver(async_client):
    """Test version and license for javascript"""
    resolved_dep = await depend.resolver.resolve_package(
        RustDep("rust", "picnic-sys", ">=3.0.14, <3.0.15"), client=async_client
    )
    assert resolved_dep.version == "3.0.14"


# @pytest.mark.asyncio
# async def test_make_single_request_rust_git(async_client):
#     """Test version and license for javascript"""
#     resolved_dep = await depend.resolver.resolve_package(
#         Dep(
#             "rust",
#             "sciter-rs",
#             "*",
#             repo="https://github.com/open-trade/rust-sciter||dyn",
#         ),
#         client=async_client,
#     )
#     # TODO: this tet isn't doing anything
#     assert resolved_dep.repo


def test_make_multiple_requests(dependency_payload):
    """Multiple package requests for JavaScript NPM and Go"""
    result = asyncio.run(
        depend.resolver.make_multiple_requests(dependency_payload, depth=1)
    )
    assert set(result.keys()) == {
        "requests",
        "envify",
        "deprecated",
        "react",
        "pygithub",
        "pynacl",
        "pyjwt",
    }


@pytest.mark.asyncio
async def test_make_single_request_cs(async_client):
    """Test version and license for c#"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("cs", "Microsoft.Bcl.AsyncInterfaces", "*"), client=async_client
    )
    # TODO: make test better
    assert resolved_dep.version


@pytest.mark.asyncio
async def test_make_single_request_cs_ver(async_client):
    """Test version and license for c#"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("cs", "Walter.Web.Firewall.Core.3.x", "[2020.8.25.1]"),
        client=async_client,
    )
    assert resolved_dep.version == "2020.8.25.1"


@pytest.mark.asyncio
async def test_make_single_request_php(async_client):
    """Test version and license for php"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("php", "folospace/socketio", "*"), client=async_client
    )
    # TODO: make test better
    assert resolved_dep.version


@pytest.mark.asyncio
async def test_make_single_request_php_ver(async_client):
    """Test version and license for php"""
    resolved_dep = await depend.resolver.resolve_package(
        Dep("php", "ajgarlag/psr15-dispatcher", "0.4.1"), client=async_client
    )
    assert resolved_dep.version == "0.4.1"
