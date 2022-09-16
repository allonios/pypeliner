"""
Text Processors
"""

import re
from typing import Any

from pipeliner.processors.base import BaseProcessor


class TitleWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Title Words Processor"

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        return self.state.title()


class RemoveStopWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Stop Words Processor"

    def process(self, input_state: Any = None) -> Any:
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
        self.state = super().process(input_state)

        for stop_word in stop_words:
            self.state = re.sub(rf"\W+{stop_word}\W+", " ", self.state)
            self.state = re.sub(rf"\W+{stop_word.title()}\W+", " ", self.state)

        return self.state


class RemoveNumbersProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Numbers Processor"

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        return re.sub(r"\d+", "", self.state)
