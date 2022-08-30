from abc import ABCMeta, abstractmethod
from typing import Any


class BaseReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Any:
        ...
