from abc import ABCMeta, abstractmethod
from typing import Any


class BaseReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Any:
        ...


class DefaultReader(BaseReader):
    def __init__(self, default_value: Any) -> None:
        self.default_value = default_value

    def read(self) -> Any:
        return self.default_value
