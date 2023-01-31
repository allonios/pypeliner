from typing import Any

import pytest

from pypelines.processors.base import BaseProcessor, CallbackProcessor


# using a dummy processor since BaseProcessor is an abstract class.
class DummyProcessor(BaseProcessor):
    def process(self, input_state: Any = None) -> Any:
        return super().process(input_state)


@pytest.fixture
def processor():
    return DummyProcessor(init_state="test")


def test_call_with_init_state(processor):
    assert processor.process() == "test"


def test_call_with_process_method_init_state(processor):
    assert processor.process("test1") == "test1"


def test_call_with_call_object_init_state(processor):
    assert processor("test1") == "test1"


class DummyProcessorNoReturnValue(BaseProcessor):
    def process(self, input_state: Any = None) -> Any:
        super().process(input_state)
        self.state = "new_test_state"


@pytest.fixture
def processor_no_return():
    return DummyProcessorNoReturnValue(init_state="test")


def test_call_with_init_state_dummy_no_return(processor_no_return):
    assert processor_no_return.process() is None
    assert processor_no_return.state == "new_test_state"


def test_call_with_process_method_init_state_no_return(processor_no_return):
    assert processor_no_return.process("test1") is None
    assert processor_no_return.state == "new_test_state"


def test_call_with_call_object_init_state_no_return(processor_no_return):
    # __call__ should handle the user forgetting to return the processed state
    assert processor_no_return("") == "new_test_state"


@pytest.fixture
def callback_processor():
    return CallbackProcessor(callback=lambda state: "callback_test")


def test_callback_processor(callback_processor):
    assert callback_processor.process() == "callback_test"
