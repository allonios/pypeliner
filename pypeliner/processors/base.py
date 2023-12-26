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
    """

    PROCESSOR_NAME = ""

    def __call__(self, state: Any) -> Any:
        return self.process(state)

    def __str__(self) -> str:
        if self.PROCESSOR_NAME:
            return self.PROCESSOR_NAME
        else:
            return super().__str__()

    @abstractmethod
    def process(self, state: Any) -> Any:
        """
        process method defines the processing operations for the current
        processor.
        it is not recommended to be called directly unless the processor is
        used a standalone unit.

        Args:
            state: processor input state.

        Returns:
            processed state.
        """
        return state


class CallbackProcessor(BaseProcessor):
    """
    Base class for processors that holds their logic in a parameterized
    callback.

    Args:
        callback: a callback with processing logic, it is mandatory for the
        callback to have 1 required positional arguments, for any further
        required positional arguments consider using a partial.
        init_state: processor initial state.
    """

    def __init__(self, callback: Callable[[Any], Any]) -> None:
        super().__init__()
        self.callback = callback

    def process(self, state: Any) -> Any:
        return self.callback(state)
