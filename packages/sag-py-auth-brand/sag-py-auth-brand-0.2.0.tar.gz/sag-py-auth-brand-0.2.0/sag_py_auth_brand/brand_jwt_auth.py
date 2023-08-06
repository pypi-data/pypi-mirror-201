import logging
from logging import Logger
from typing import List, Optional

from fastapi import Header
from sag_py_auth.jwt_auth import JwtAuth
from sag_py_auth.models import Token, TokenRole
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from .models import BrandAuthConfig
from .request_brand_context import set_brand as set_brand_to_context
from .request_brand_context import set_brand_alias as set_brand_alias_to_context

logger: Logger = logging.getLogger(__name__)


class BrandJwtAuth(JwtAuth):
    def __init__(self, auth_config: BrandAuthConfig, required_roles: Optional[List[str]]) -> None:
        super().__init__(
            auth_config,
            required_roles=self._build_required_token_roles(auth_config, required_roles),
            required_realm_roles=self._build_required_realm_roles(auth_config),
        )

    def _build_required_token_roles(
        self, auth_config: BrandAuthConfig, required_roles: Optional[List[str]]
    ) -> List[TokenRole]:
        token_roles: List[TokenRole] = [TokenRole("role-instance", auth_config.instance)]

        if required_roles is not None:
            token_roles.extend(TokenRole("role-endpoint", item) for item in required_roles)

        return token_roles

    def _build_required_realm_roles(self, auth_config: BrandAuthConfig) -> List[str]:
        return [auth_config.stage]

    async def __call__(self, request: Request, brand: str = Header(...)) -> Token:  # type: ignore
        token: Token = await super(BrandJwtAuth, self).__call__(request)
        self._verify_brand(token, brand)
        set_brand_to_context(brand)
        return token

    def _verify_brand(self, token: Token, brand: str) -> None:
        if not token.has_role("role-brand", brand) and not self._brand_has_accessible_alias(token, brand):
            self._raise_auth_error(HTTP_403_FORBIDDEN, "Missing brand.")

    def _brand_has_accessible_alias(self, token: Token, brand: str) -> bool:
        brand_aliases: List[str] = token.get_roles("role-brand-alias")

        # Check if the given brand is defined as alias for the brand it should be replaced by.
        if not brand_aliases:
            logger.debug("Brand %s is not in list of accessible brand aliases.", brand)
            return False

        # Find indices of all detected brand aliases accessible for the current client or user
        # (i.e. compare accessible brands with brand aliases in token because
        # user access is configured via brands (not via brand alias)):
        accessible_brand_alias_ids: List[int] = [
            id
            for id, val in enumerate(brand_alias in token.get_roles("role-brand") for brand_alias in brand_aliases)
            if val
        ]

        # Set alias only if there is exactly one match
        # (one user must have access to 0 or 1 brand that corresponds to a brand alias):
        if len(accessible_brand_alias_ids) > 1:
            logger.warning("Unambiguous role association: user has access to more than one brand alias.")
            return False
        if not accessible_brand_alias_ids:
            logger.warning("Unambiguous role association: brand is not associated with any brand aliases.")
            return False

        brand_alias: str = brand_aliases[0]
        set_brand_alias_to_context(brand_alias)
        return True
