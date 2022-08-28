from typing import Any, List


class BaseReaderRunner:
    def __init__(self, processors: List, initial_state: Any = None) -> None:
        self.current_state = self.init_state(initial_state)
        self.processors = processors

    def init_state(self, initial_state: Any = None) -> Any:
        if initial_state:
            return initial_state
        return None

    def run(self) -> Any:
        for processor in self.processors:
            self.current_state = processor(self.current_state)
        return self.current_state


class BaseStreamReaderRunner(BaseReaderRunner):
    def update_state(self) -> Any:
        yield self.current_state

    def run(self):
        for updated_state in self.update_state():
            self.current_state = updated_state
            self.current_state = super(BaseStreamReaderRunner, self).run()
            yield self.current_state
