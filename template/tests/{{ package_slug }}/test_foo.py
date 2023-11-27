"""Example test file."""

import pytest


@pytest.mark.parametrize("foo", ["fu", "foo"])
def test_bar(foo: str) -> None:
    """Test foo bar does not fubar."""
    assert foo != "bar"
