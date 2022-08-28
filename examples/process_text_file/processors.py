import re
from typing import Any

from processors.base import BaseProcessor


class TitleWordsProcessor(BaseProcessor):
    def process_state(self, input_state: Any = None) -> Any:
        self.state = super().process_state(input_state)
        return self.state.title()


class RemoveStopWordsProcessor(BaseProcessor):
    def process_state(self, input_state: Any = None) -> Any:
        stop_words = [
            "the",
            "to",
            "and",
            "a",
            "in",
            "it",
            "is",
            "I",
            "that",
            "had",
            "on",
            "for",
            "be",
            "were",
            "was",
            "of",
            "or",
            "it",
            "an",
        ]
        self.state = super().process_state(input_state)

        for stop_word in stop_words:
            self.state = re.sub(rf"\W+{stop_word}\W+", " ", self.state)

        return self.state


class RemoveNumbersProcessor(BaseProcessor):
    def process_state(self, input_state: Any = None) -> Any:
        self.state = super().process_state(input_state)
        return re.sub(r"\d+", "", self.state)
