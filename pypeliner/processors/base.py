"""
Base module for processors that contains base processors class and a
callback based processors base class.
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from pypeliner.exceptions import StateIntegrityError


class BaseProcessor(metaclass=ABCMeta):
    """
    Base class for processors.

    Attributes:
        PROCESSOR_NAME: verbose name for processor.

    Args:
    """

    PROCESSOR_NAME = ""

    def __init__(self) -> None:
        self.__state = None

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state: Any) -> None:
        """
        state setter, implemented to prevent setting/registering a None state.
        Args:
            new_state:
                The new state.
        Returns:
            None
        """
        if new_state is None:
            raise StateIntegrityError
        self.__state = new_state

    def register_state(self, new_state: Any) -> Any:
        """
        register_state method is implemented and used just for the sake of
        explicitly saying "this state is not registered", the setter for state
        is the one actually being used, the only difference is that
        register_state will return the new state.

        Args:
            new_state:
                The new state.

        Returns:
            The new state.
        """
        self.state = new_state
        return self.state

    def __call__(self, state: Any) -> Any:
        # registering the input state.
        self.register_state(state)

        result = self.process(state)

        # registering the output state.
        self.register_state(result)

        return self.state

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
        return self.callback(self.state)
