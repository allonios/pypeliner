from typing import Any, List

from runners.base import BaseReaderRunner


class FileReaderRunner(BaseReaderRunner):
    def __init__(
        self, processors: List, file_path: str, initial_state: Any = None
    ) -> None:
        super().__init__(processors, initial_state)
        self.file_path = file_path

    def init_state(self, initial_state: Any = None) -> str:
        if initial_state:
            return initial_state
        with open(self.file_path, "r") as file_handler:
            return file_handler.read()
