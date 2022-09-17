"""
Base runners module, contains base runner and base stream runner.
"""
from typing import Any, List

from pipeliner.processors.base import BaseProcessor
from pipeliner.readers.base import BaseReader
from pipeliner.utils.decorators import exec_timer


class BaseRunner:
    """
    Base class for runners, can be used with bulk readers to run processors in
    a linear pipeline.

    Args:
        processors: processors objects to be run by this runner.
        reader: reader object to read the data.
        verbose: output running status on terminal.
        run_timers: print the timing for each processor.
        timers_decimal_places: when run_timers is True,
            it will specify the number of decimal points for the measured time,
            if run_timers is False and this parameter is specified
            it will have no effect.
    """

    def __init__(
        self,
        processors: List[BaseProcessor],
        reader: BaseReader,
        verbose: bool = False,
        run_timers: bool = False,
        timers_decimal_places: int = 3,
    ) -> None:
        self.processors = processors
        self.reader = reader
        self.verbose = verbose
        self.run_timers = run_timers
        self.timers_decimal_places = timers_decimal_places

    def run_processors_loop(self) -> None:
        """
        A method defines the loop for running the processors in a linear
        manner.

        Returns:
            None.
        """
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
        """
        A method used to read the state and start the processing loop.

        Returns:
            processed state.
        """
        self.current_state = self.reader.read()
        self.run_processors_loop()
        return self.current_state


class BaseStreamRunner(BaseRunner):
    """
    Base for runners that uses stream readers.
    """

    def run(self) -> Any:
        """
        A method that uses the stream reader to update the state,
        run the processors loop and yield the result. ths method keeps reading
        until the reader stops providing any new updated state.

        Returns:
            processed state.
        """
        for updated_state in self.reader.read():
            self.current_state = updated_state
            self.run_processors_loop()
            yield self.current_state
