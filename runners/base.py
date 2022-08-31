from typing import Any, List

from readers.base import BaseReader


class BaseRunner:
    def __init__(
        self, processors: List, reader: BaseReader, initial_state: Any = None
    ) -> None:
        self.current_state = initial_state
        self.processors = processors
        self.reader = reader

    def run(self):
        self.current_state = self.reader.read()
        for processor in self.processors:
            self.current_state = processor(self.current_state)
        return self.current_state


class BaseStreamRunner(BaseRunner):
    def run(self) -> Any:
        for updated_state in self.reader.read():
            self.current_state = updated_state
            for processor in self.processors:
                self.current_state = processor(self.current_state)
            yield self.current_state
