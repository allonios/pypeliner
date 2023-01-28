"""
String utils module contains utility functions to manipulate strings.
"""
from typing import Union


def convert_string_to_number(string: str) -> Union[int, float, str]:
    """
    A function to convert an str typed number to a number, if the passed string
    is a text and not a number, then the same string is returned.
    Args:
        string: the number in a string form

    Returns:
        A number (int or a float).
    """
    if string.strip().isdigit():
        return int(string)
    else:
        try:
            return float(string)
        except ValueError:
            return string
