"""
Base module for processors that contains base processors class and a
callback based processors base class.
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Callable


class BaseProcessor(metaclass=ABCMeta):
    """
    Base class for processors.

    Attributes:
        PROCESSOR_NAME: verbose name for processor.

    Args:
        init_state: initial state used by the processor,
            usually used when using the processor on its own without a runner.
    """

    PROCESSOR_NAME = ""

    def __init__(self, init_state: Any = None) -> None:
        self.state = init_state

    def __call__(self, input_state: Any) -> Any:
        result = self.process(input_state)
        # if a value is provided by the `process` method we use that as the new
        # processed state.
        # the user might forget to store his latest processing results in
        # self.state and just returns it directly,
        # so this should cover that case.
        if result is not None:
            self.state = result
        return self.state

    def __str__(self) -> str:
        if self.PROCESSOR_NAME:
            return self.PROCESSOR_NAME
        else:
            return super().__str__()

    @abstractmethod
    def process(self, input_state: Any = None) -> Any:
        """
        process method defines the processing operations for the current
        processor.

        Args:
            input_state: processor input state.

        Returns:
            processed state.
        """
        if input_state is not None:
            self.state = input_state
        return self.state


class CallbackProcessor(BaseProcessor):
    """
    Base class for processors that holds their logic in a parameterized
    callback.

    Args:
        callback: a callback with processing logic.
        init_state: processor initial state.
    """

    def __init__(self, callback: Callable, init_state: Any = None) -> None:
        super().__init__(init_state)
        self.callback = callback

    def process(self, input_state: Any = None) -> Any:
        self.state = self.callback(super().process(input_state))
        return self.state

    def __str__(self) -> str:
        if self.PROCESSOR_NAME:
            return self.PROCESSOR_NAME
        else:
            return self.callback.__name__
