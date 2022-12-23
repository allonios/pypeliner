"""
Bulk readers module, defines readers for reading bulk data all at once,
contains a file reader and csv file reader.
"""
from typing import Dict, List

from pipeliner.readers.base import BaseReader
from pipeliner.utils.csv_utils import convert_row_values_to_numbers


class FileReader(BaseReader):
    """
    A reader used to read an entire file.

    Args:
        file_path: file directory.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> str:
        with open(self.file_path, "r") as file_handler:
            return file_handler.read()


class CSVFileReader(BaseReader):
    """
    A reader to read a csv file.

    Args:
        file_path: file directory.
        load_titles_row: read the first line from the file to consider that
        as the columns names.
        columns_names: custom column names that will override the csv file
        existing columns names when load_titles_row is True.
        delimiter: rows delimiter.
        detect_numbers: convert string number values to int/float.
    """

    def __init__(
        self,
        file_path: str,
        load_titles_row: bool = True,
        columns_names: List = None,
        delimiter: str = ",",
        detect_numbers: bool = True,
    ) -> None:
        self.file_path = file_path
        self.load_titles_row = load_titles_row
        self.columns_names = []
        self.custom_columns_names = columns_names
        self.delimiter = delimiter
        self.detect_numbers = detect_numbers

    def read(self) -> Dict:
        data = {}

        with open(self.file_path, "r") as file_handler:
            rows = list(
                map(
                    lambda line: (
                        convert_row_values_to_numbers(
                            line.replace("\n", "").split(self.delimiter)
                        )
                        if self.detect_numbers
                        else line.replace("\n", "").split(self.delimiter)
                    ),
                    file_handler.readlines(),
                )
            )

        # user have passed custom column names.
        if self.custom_columns_names:
            self.columns_names = self.custom_columns_names
            # user asked to load title rows, but in the case of passing
            # custom column names they will override the title rows,
            # but still we need to drop the title row to apply the effect of
            # loading the title row, and then it was overridden by the
            # custom names.
            if self.load_titles_row:
                rows = rows[1:]
        # user asked to only load the columns titles rows.
        elif self.load_titles_row:
            self.columns_names = rows[0]
            rows = rows[1:]
        # user didn't ask to load the columns titles row nor passed a
        # custom names.
        else:
            columns_count = len(rows[0])
            self.columns_names = [
                f"column_{column_index}"
                for column_index in range(columns_count)
            ]

        for index, column in enumerate(self.columns_names):
            data[column] = list(map(lambda row: row[index], rows))

        return data
