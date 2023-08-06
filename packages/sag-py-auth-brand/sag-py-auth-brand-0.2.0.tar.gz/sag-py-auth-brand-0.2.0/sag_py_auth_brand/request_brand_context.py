from contextvars import ContextVar
from typing import Optional

brand: ContextVar[Optional[str]] = ContextVar("brand", default=None)
brand_alias: ContextVar[Optional[str]] = ContextVar("brand_alias", default=None)


def get_brand() -> str:
    """Gets the context local brand. See library contextvars for details.

    Returns: The brand
    """
    current_brand_alias: Optional[str] = brand_alias.get("")
    current_brand: Optional[str] = brand.get("")
    return current_brand_alias or current_brand or ""


def set_brand(brand_to_set: Optional[str]) -> None:
    """Sets the context local brand. See library contextvars for details."""
    brand.set(brand_to_set)


def set_brand_alias(brand_alias_to_set: Optional[str]) -> None:
    """Sets the context local brand. See library contextvars for details."""
    brand_alias.set(brand_alias_to_set)
