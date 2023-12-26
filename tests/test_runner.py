from typing import Any

import pytest

from pypeliner.processors.base import BaseProcessor
from pypeliner.readers.base import DefaultReader
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


def test_run_pipeline_runner(pipeline):
    assert pipeline.run() == "test_runnertest_runner"


def test_processors_call(mocker, pipeline):
    mocked_reader = mocker.patch.object(
        pipeline.reader, "read", return_value="test_runner"
    )

    mocked_processor1 = mocker.patch.object(
        pipeline.processors[0], "process", return_value="test_runner"
    )
    mocked_processor3 = mocker.patch.object(
        pipeline.processors[2], "process", return_value="test_runner"
    )

    pipeline.run()

    mocked_reader.assert_called_once()
    mocked_processor1.assert_called_once_with("test_runner")
    mocked_processor3.assert_called_once_with("test_runnertest_runner")
