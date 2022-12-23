"""
CSV utils contains utilities to read csv files
"""
from typing import List, Union

from pipeliner.utils.string_utils import convert_string_to_number


def convert_row_values_to_numbers(
    row: List[str],
) -> List[Union[int, float, str]]:
    """
    A function to convert a csv file row string values to numbers if possible.

    e.g:
        input: ["1", "2", "a", "b"]
        output: [1, 2, "a", "b"]

    Args:
        row: a row from a csv file.

    Returns:
        the row with number values instead of strings
    """
    return list(map(lambda element: convert_string_to_number(element), row))
