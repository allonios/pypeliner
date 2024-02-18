from typing import Any

import pytest

from pypeliner.processors.base import BaseProcessor, CallbackProcessor


# using a dummy processor since BaseProcessor is an abstract class.
class DummyProcessor(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state


@pytest.fixture
def processor():
    return DummyProcessor()


@pytest.fixture
def callback_processor():
    return CallbackProcessor(callback=lambda state: "callback_test")


def test_call_process_method_init_state(processor):
    assert processor.process("test1") == "test1"


def test_callback_processor(callback_processor):
    assert callback_processor.process("callback_test") == "callback_test"
