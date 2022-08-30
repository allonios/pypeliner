from readers.base import BaseReader


class FileLinesReader(BaseReader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> str:
        with open(self.file_path, "r") as file_handler:
            for line in file_handler.readlines():
                yield line
