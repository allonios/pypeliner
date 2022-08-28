from abc import ABCMeta
from typing import Any, Callable


class BaseProcessor(metaclass=ABCMeta):
    def __init__(self, init_state: Any = None) -> None:
        self.state = init_state

    def __call__(self, input_state: Any) -> Any:
        result = self.process_state(input_state)
        # if a value is provided by process_state we use that as the new
        # processed state.
        # the user might forget to store his latest processing results in
        # self.state and just returns it directly,
        # so this should cover that case.
        if result:
            self.state = result
        return self.state

    def process_state(self, input_state: Any = None) -> Any:
        if input_state:
            self.state = input_state
        return self.state


class CallbackProcessor(BaseProcessor):
    def __init__(self, callback: Callable, init_state: Any = None) -> None:
        super().__init__(init_state)
        self.callback = callback

    def process_state(self, input_state: Any = None) -> Any:
        return self.callback(super().process_state(input_state))
