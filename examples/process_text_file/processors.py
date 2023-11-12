"""
Text Processors
"""

import re
from typing import Any

from pypeliner.processors.base import BaseProcessor


class TitleWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Title Words Processor"

    def process(self, state: Any) -> Any:
        return state.title()


class RemoveStopWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Stop Words Processor"

    def process(self, state: Any) -> Any:
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

        for stop_word in stop_words:
            state = re.sub(rf"\W+{stop_word}\W+", " ", state)
            state = re.sub(rf"\W+{stop_word.title()}\W+", " ", state)

        return state


class RemoveNumbersProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Numbers Processor"

    def process(self, state: Any) -> Any:
        return re.sub(r"\d+", "", state)
