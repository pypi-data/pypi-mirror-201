from typing import Optional

from sag_py_auth_brand.request_brand_context import get_brand as get_brand_from_context
from sag_py_auth_brand.request_brand_context import set_brand as set_brand_to_context
from sag_py_auth_brand.request_brand_context import set_brand_alias as set_brand_alias_to_context


def test__get_brand__not_set() -> None:
    # Arrange
    set_brand_to_context(None)
    set_brand_alias_to_context(None)

    # Act
    actual: str = get_brand_from_context()

    assert not actual


def test__get_brand__with_previously_set_brand() -> None:
    # Arrange
    set_brand_to_context("myBrand")
    set_brand_alias_to_context(None)

    # Act
    actual: Optional[str] = get_brand_from_context()

    assert actual == "myBrand"


def test__get_brand__with_previously_set_brand_alias() -> None:
    # Arrange
    set_brand_to_context(None)
    set_brand_alias_to_context("myBrandAlias")

    # Act
    actual: Optional[str] = get_brand_from_context()

    assert actual == "myBrandAlias"


def test__get_brand__with_previously_set_both() -> None:
    # Arrange
    set_brand_to_context("myBrand")
    set_brand_alias_to_context("myBrandAlias")

    # Act
    actual: Optional[str] = get_brand_from_context()

    assert actual == "myBrandAlias"
