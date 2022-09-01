from typing import Any, List

from readers.base import BaseReader
from utils.decorators import exec_timer


class BaseRunner:
    def __init__(
        self,
        processors: List,
        reader: BaseReader,
        initial_state: Any = None,
        verbose: bool = False,
        run_timers: bool = False,
        timers_decimal_places: int = 3,
    ) -> None:
        self.current_state = initial_state
        self.processors = processors
        self.reader = reader
        self.verbose = verbose
        self.run_timers = run_timers
        self.timers_decimal_places = timers_decimal_places

    def run_processors_loop(self):
        for processor in self.processors:
            if self.verbose:
                print(f"Running: {processor}")
            if self.run_timers:
                named_timer_decorator = exec_timer(
                    str(processor), self.timers_decimal_places
                )
                timed_processor_callback = named_timer_decorator(processor)
                self.current_state = timed_processor_callback(
                    self.current_state
                )
            else:
                self.current_state = processor(self.current_state)

    def run(self):
        self.current_state = self.reader.read()
        self.run_processors_loop()
        return self.current_state


class BaseStreamRunner(BaseRunner):
    def run(self) -> Any:
        for updated_state in self.reader.read():
            self.current_state = updated_state
            self.run_processors_loop()
            yield self.current_state
