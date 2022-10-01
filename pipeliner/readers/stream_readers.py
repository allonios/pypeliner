"""
Stream readers module, defines readers for reading data from streams, contains
file lines reader.
"""
from typing import List

from pipeliner.readers.base import BaseReader


class FileLinesReader(BaseReader):
    """
    A reader used to read a file line by line using a generator.
    Args:
        file_path: file directory.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> str:
        with open(self.file_path, "r") as file_handler:
            for line in file_handler.readlines():
                yield line


class CSVFileStreamReader(BaseReader):
    def __init__(
        self,
        file_path: str,
        load_titles_row: bool = True,
        delimiter: str = ",",
        detect_numbers: bool = True,
    ) -> None:
        self.file_path = file_path
        self.load_titles_row = load_titles_row
        self.delimiter = delimiter
        self.detect_numbers = detect_numbers

    def read(self) -> List[str]:
        with open(self.file_path, "r") as file_handler:
            if not self.load_titles_row:
                # just read the first line to through that away.
                file_handler.readline()

            for line in file_handler.readlines():
                yield line.replace("\n", "").split(self.delimiter)
