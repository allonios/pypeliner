from typing import Any

import pytest

from pypeliner.processors.base import BaseProcessor
from pypeliner.readers.base import DefaultReader
from pypeliner.runner_configuration import RunnerConfiguration
from pypeliner.runners.base import BaseRunner


class Processor1(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state


class Processor2(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state * 2


class Processor3(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state


class DummyPreProcessHook(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state


class DummyPostProcessHook(BaseProcessor):
    def process(self, state: Any) -> Any:
        return state


@pytest.fixture
def pipeline():
    return BaseRunner(
        processors=[
            Processor1(),
            Processor2(),
            Processor3(),
        ],
        reader=DefaultReader("test_runner"),
    )


@pytest.fixture
def pipeline_with_hooks():
    return BaseRunner(
        processors=[
            Processor1(),
            Processor2(),
            Processor3(),
        ],
        reader=DefaultReader("test_runner"),
        configuration=RunnerConfiguration(
            pre_processors=[DummyPreProcessHook()],
            post_processors=[DummyPostProcessHook()],
        ),
    )


def test_run_pipeline_runner(pipeline):
    assert pipeline.run() == "test_runnertest_runner"


def test_processors_hooks_call(mocker, pipeline_with_hooks):
    mocked_reader = mocker.patch.object(
        pipeline_with_hooks.reader, "read", return_value="test_runner"
    )

    mocked_processor1 = mocker.patch.object(
        pipeline_with_hooks.processors[0],
        "process",
        return_value="test_runner",
    )
    mocked_processor3 = mocker.patch.object(
        pipeline_with_hooks.processors[2],
        "process",
        return_value="test_runner",
    )

    mocked_preprocessor = mocker.patch.object(
        pipeline_with_hooks.configuration.pre_processors[0],
        "process",
        return_value="test_runner",
    )

    mocked_postprocessor = mocker.patch.object(
        pipeline_with_hooks.configuration.post_processors[0],
        "process",
        return_value="test_runner",
    )

    pipeline_with_hooks.run()

    mocked_reader.assert_called_once()
    mocked_processor1.assert_called_once_with("test_runner")
    mocked_processor3.assert_called_once_with("test_runner")

    mocked_preprocessor.assert_any_call("test_runner")
    mocked_postprocessor.assert_any_call("test_runner")
