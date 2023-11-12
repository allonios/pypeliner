from typing import Any

import pytest

from pypeliner.processors.base import BaseProcessor, CallbackProcessor


# using a dummy processor since BaseProcessor is an abstract class.
class DummyProcessor(BaseProcessor):
    def process(self, state: Any) -> Any:
        return super().process(state)


class DummyProcessorWithRegisterState(BaseProcessor):
    def process(self, state: Any) -> Any:
        result = super().process(state)
        self.register_state(result)
        return self.state


@pytest.fixture
def processor():
    return DummyProcessor()


@pytest.fixture
def processor_with_register_state():
    return DummyProcessorWithRegisterState()


@pytest.fixture
def callback_processor():
    return CallbackProcessor(callback=lambda state: "callback_test")


def test_call_process_method_init_state(processor):
    assert processor.process("test1") == "test1"


def test_call_process_method_register_state(processor_with_register_state):
    assert processor_with_register_state.process("test1") == "test1"
    assert processor_with_register_state.state == "test1"


def test_call_with_call_object_init_state(processor):
    assert processor("test1") == "test1"
    assert processor.state == "test1"


def test_callback_processor(callback_processor):
    assert callback_processor.process("callback_test") == "callback_test"


def test_callback_call_object_processor(callback_processor):
    assert callback_processor("callback_test") == "callback_test"
    assert callback_processor.state == "callback_test"
