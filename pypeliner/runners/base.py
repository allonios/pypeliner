"""
Base runners module, contains base runner and base stream runner.
"""
from copy import deepcopy
from typing import Any, List

from pypeliner.processors.base import BaseProcessor
from pypeliner.readers.base import BaseReader
from pypeliner.runner_configuration import RunnerConfiguration
from pypeliner.utils.decorators import exec_timer


class BaseRunner:
    """
    Base class for runners, can be used with bulk readers to run processors in
    a linear pipeline.

    Args:
        processors: processors objects to be run by this runner.
        reader: reader object to read the data.
        configuration: configuration object to be used.
    """

    def __init__(
        self,
        processors: List[BaseProcessor],
        reader: BaseReader,
        configuration: RunnerConfiguration,
    ) -> None:
        self.processors = processors
        self.reader = reader
        self.configuration = configuration

    def decorate_processor(self, processor: BaseProcessor) -> BaseProcessor:
        if self.configuration.run_timers:
            named_timer_decorator = exec_timer(
                str(processor), self.configuration.timers_decimal_places
            )
            timed_processor_callback = named_timer_decorator(processor)
            return timed_processor_callback

        return processor

    def display_verbose_message(self, message: str) -> str:
        """
        Args method that will print a verbose message.
        Args:
            message: The verbose message to be displayed.

        Returns:
            None
        """
        if not self.configuration.verbose:
            return ""

        return message

    def run_hooks(self, state, processors: List[BaseProcessor]) -> Any:
        if not processors:
            return state

        for processor in processors:
            # print preprocess hook verbose message.
            self.display_verbose_message(f"Running hook: {processor}")

            decorated_processor = self.decorate_processor(processor)
            # run the decorated processor.
            state = decorated_processor(state)

            # print postprocess hook verbose message.
            self.display_verbose_message(f"Finished hook: {processor}")

        return state

    def run_processors_loop(self, initial_state: Any) -> None:
        """
        A method defines the loop for running the processors in a linear
        manner.

        Returns:
            Processed state.
        """

        # deepcopy the state if needed.
        if self.configuration.deep_copy_state:
            state = deepcopy(initial_state)
        else:
            state = initial_state

        for processor in self.processors:
            # run preprocessing hooks.
            state = self.run_hooks(state, self.configuration.pre_processors)

            # print preprocess verbose message.
            self.display_verbose_message(f"Running: {processor}")

            decorated_processor = self.decorate_processor(processor)
            # run the decorated processor.
            state = decorated_processor(state)

            # print postprocess verbose message.
            self.display_verbose_message(f"Finished: {processor}")

            # run postprocessing hooks.
            state = self.run_hooks(state, self.configuration.post_processors)

        return state

    def run(self):
        """
        A method used to read the state and start the processing loop.

        Returns:
            processed state.
        """
        initial_state = self.reader.read()
        # post process the initial state, we can't do any preprocessing since
        # we still don't have anything yet.
        initial_state = self.run_hooks(
            initial_state, self.configuration.post_processors
        )
        return self.run_processors_loop(initial_state)


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
            yield self.run_processors_loop(updated_state)
