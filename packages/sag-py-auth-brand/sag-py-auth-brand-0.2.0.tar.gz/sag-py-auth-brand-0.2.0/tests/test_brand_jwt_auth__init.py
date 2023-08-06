from typing import List

from sag_py_auth.models import TokenRole

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.models import BrandAuthConfig


def test__jwt_auth__init__with_multiple_roles() -> None:
    # Arrange
    auth_config = BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName", "audienceOne", "myInstance", "myStage"
    )
    required_roles: List[str] = ["roleOne", "roleTwo"]

    # Act
    jwt = BrandJwtAuth(auth_config, required_roles)

    # Assert
    assert len(jwt.required_realm_roles) == 1
    assert "myStage" in jwt.required_realm_roles

    assert len(jwt.required_roles) == 3
    _verify_token_role(jwt, 0, "role-instance", "myInstance")
    _verify_token_role(jwt, 1, "role-endpoint", "roleOne")
    _verify_token_role(jwt, 2, "role-endpoint", "roleTwo")


def test__jwt_auth__init__without_roles() -> None:
    # Arrange
    auth_config = BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName", "audienceOne", "myInstance", "myStage"
    )

    # Act
    jwt = BrandJwtAuth(auth_config, None)

    # Assert
    assert len(jwt.required_realm_roles) == 1
    assert "myStage" in jwt.required_realm_roles

    assert len(jwt.required_roles) == 1
    _verify_token_role(jwt, 0, "role-instance", "myInstance")


def _verify_token_role(jwt: BrandJwtAuth, item_no: int, client: str, role: str) -> None:
    instance: TokenRole = jwt.required_roles[item_no]
    assert instance.client == client
    assert instance.role == role
