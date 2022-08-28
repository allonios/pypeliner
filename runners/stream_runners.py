from typing import Any, List

from runners.base import BaseStreamReaderRunner


class FileLinesReaderRunner(BaseStreamReaderRunner):
    def __init__(
        self, processors: List, file_path: str, initial_state: Any = None
    ) -> None:
        super().__init__(processors, initial_state)
        self.file_path = file_path

    def update_state(self) -> str:
        with open(self.file_path, "r") as file_handler:
            for line in file_handler.readlines():
                yield line
