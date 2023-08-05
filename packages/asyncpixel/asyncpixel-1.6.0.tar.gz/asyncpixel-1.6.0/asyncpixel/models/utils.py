"""Utils for pydantic models."""
from typing import Union


def safe_divide(dividend: Union[int, float], divisor: Union[int, float]) -> float:
    """Return dividend / divisor without raising ZeroDivisionError.

    Args:
        dividend (int, float): the dividend (a in a/b)
        divisor (int, float): the divisor (b in a/b)

    Returns:
        float: dividend / divisor, or floating point infinity if divisor == 0
    """
    if divisor == 0:
        return float("inf") * (1 if dividend >= 0 else -1)
    return dividend / divisor


def to_camel(string: str) -> str:
    """Convert str to camel case.

    Args:
        string (str): input.

    Returns:
        str: camelCase version of str.
    """
    out = string.split("_")[0]
    for word in string.split("_")[1:]:
        out += word.capitalize()
    return out


def to_upper(string: str) -> str:
    """Convert str to upper case.

    Args:
        string (str): input.

    Returns:
        str: upperCase version of str.
    """
    return string.upper()
