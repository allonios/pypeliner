from abc import ABCMeta, abstractmethod
from types import NoneType
from typing import Any, Callable


class BaseProcessor(metaclass=ABCMeta):
    PROCESSOR_NAME = ""

    def __init__(self, init_state: Any = None) -> None:
        self.state = init_state

    def __call__(self, input_state: Any) -> Any:
        result = self.process(input_state)
        # if a value is provided by process_state we use that as the new
        # processed state.
        # the user might forget to store his latest processing results in
        # self.state and just returns it directly,
        # so this should cover that case.
        if not isinstance(result, NoneType):
            self.state = result
        return self.state

    def __str__(self) -> str:
        if self.PROCESSOR_NAME:
            return self.PROCESSOR_NAME
        else:
            return super().__str__()

    @abstractmethod
    def process(self, input_state: Any = None) -> Any:
        if not isinstance(input_state, NoneType):
            self.state = input_state
        return self.state


class CallbackProcessor(BaseProcessor):
    def __init__(self, callback: Callable, init_state: Any = None) -> None:
        super().__init__(init_state)
        self.callback = callback

    def process(self, input_state: Any = None) -> Any:
        return self.callback(super().process(input_state))

    def __str__(self) -> str:
        if self.PROCESSOR_NAME:
            return self.PROCESSOR_NAME
        else:
            return self.callback.__name__
