from typing import Literal, Tuple

import pytest
from fastapi import Request
from pytest import MonkeyPatch
from sag_py_auth.models import Token
from starlette.datastructures import Headers

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.models import BrandAuthConfig
from tests.helpers import get_token

pytest_plugins: Tuple[Literal["pytest_asyncio"]] = ("pytest_asyncio",)


async def jwt_auth_call_mock(self: BrandJwtAuth, request: Request) -> Token:
    return get_token(None, None)


def _verify_brand_mock(self: BrandJwtAuth, token: Token, brand: str) -> None:
    if token:
        token.token_dict["_verify_brand"] = "True"


was_brand_set_to_context = False


def set_brand_to_context_mock(brand_to_set: str) -> None:
    global was_brand_set_to_context
    was_brand_set_to_context = True


@pytest.mark.asyncio
async def test__call__correctly_processes_request(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    auth_config = BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName", "audienceOne", "myInstance", "myStage"
    )

    monkeypatch.setattr("sag_py_auth.JwtAuth.__call__", jwt_auth_call_mock)
    monkeypatch.setattr("sag_py_auth_brand.brand_jwt_auth.BrandJwtAuth._verify_brand", _verify_brand_mock)
    monkeypatch.setattr("sag_py_auth_brand.brand_jwt_auth.set_brand_to_context", set_brand_to_context_mock)

    jwt = BrandJwtAuth(auth_config, None)

    request: Request = Request(scope={"type": "http"})
    request._headers = Headers({"Authorization": "Bearer validToken"})

    # Act
    actual: Token = await jwt.__call__(request)

    # Assert - Verify that all steps have been executed
    assert actual.get_field_value("typ") == "Bearer"
    assert actual.get_field_value("azp") == "public-project-swagger"
    assert actual.get_field_value("_verify_brand") == "True"
    assert was_brand_set_to_context
