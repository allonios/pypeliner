"""
Bulk readers module, defines readers for reading bulk data all at once,
contains a file reader
"""

from pipeliner.readers.base import BaseReader


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
