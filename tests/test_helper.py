import pytest

from depinspect.validator import is_valid_package_name


@pytest.mark.parametrize(
    "package_name, expected_result",
    [
        ("lib1", True),
        ("1l", True),
        ("!not_a_lib", False),
        ("a_super_lib", False),
        ("a:superlib", False),
        ("!", False),
        ("a", False),
        ("MY-LIB+123.ubuntu", True),
    ],
)
def test_is_valid_package(package_name: str, expected_result: bool) -> None:
    result = is_valid_package_name(package_name)
    assert result == expected_result
