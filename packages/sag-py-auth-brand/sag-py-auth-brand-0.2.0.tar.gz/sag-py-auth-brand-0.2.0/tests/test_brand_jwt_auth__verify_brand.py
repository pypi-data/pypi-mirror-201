from typing import Any, Dict, Optional

import pytest
from fastapi import HTTPException
from sag_py_auth.models import Token

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.models import BrandAuthConfig

from .helpers import get_token


def test__verify_brand__where_user_has_brand() -> None:
    # Arrange
    auth_config = BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
    )
    brand_jwt_auth = BrandJwtAuth(auth_config, ["myRequiredRole"])

    resource_access: Optional[Dict[str, Any]] = {"role-brand": {"roles": ["mybrandone", "mybrandtwo"]}}

    token: Token = get_token(None, resource_access)

    # Act
    try:
        brand_jwt_auth._verify_brand(token, "mybrandone")
    except Exception:
        pytest.fail("No exception expected if the brand is present in the token")


def test__verify_brand__where_brand_is_missing() -> None:
    with pytest.raises(HTTPException) as exception:
        # Arrange
        auth_config = BrandAuthConfig(
            "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
        )
        brand_jwt_auth = BrandJwtAuth(auth_config, ["myRequiredRole"])

        resource_access: Optional[Dict[str, Any]] = {"role-brand": {"roles": ["mybrandone", "mybrandtwo"]}}

        token: Token = get_token(None, resource_access)

        # Act
        brand_jwt_auth._verify_brand(token, "mybrandthree")

    # Assert
    assert exception.value.status_code == 403
    assert exception.value.detail == "Missing brand."
