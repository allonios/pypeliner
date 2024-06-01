# Pypeliner

`pypeliner` is a simple python framework for building data processing pipelines.

you can check out the documentation [here](https://simple-pypeliner.readthedocs.io/en/latest/).

and checkout some examples [here](https://github.com/allonios/pypeliner/tree/master/examples).

## Installation
it can be simply installing using `pip`:

```shell
pip install simple-pypeliner
```

## Getting Started

Let's say we want to build a pipeline for processing textual data coming from a file.
we will need 3 main components to achieve this using pypeliner.

### Reader
first we will need a reader for reading the file, and it can be defined like the following:

```python
from pypeliner.readers.base import BaseReader

class FileReader(BaseReader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> str:
        with open(self.file_path, "r") as file_handler:
            return file_handler.read()
```

inheriting from `BaseReader` makes sure that the `read` method is implemented to be used later within the [Reader](#reader).
the code basically is reading a file and returning its content as a string.

### Processors
next we will define our processing logic, lets say we want to make all letters in the text file lower case, then remove
stop words i.g: but, and, or, etc after that remove numbers.

to achieve that we will write a processor for each one of these tasks.

each processor should define its own `process` method. a processor will receive the `state` it needs to process from the [Runner](#runner).

if `state` is passed the that processor will use the `state` instead of the state passed by the runner,
this is achieved using the `super` call for `process` method and passing `state` there.
it is recommended to always call `super` for the `process` method as a best practice.

`PROCESSOR_NAME` is a verbose name for a processor.

#### 1- Lower Case Processor
```python
class LowerCaseProcessor(BaseProcessor):
    PROCESSOR_NAME = "Lower Case Processor"

    def process(self, state: Any = None) -> Any:
        return state.lower()
```

#### 2- Remove Stop Words Processor
```python
class RemoveStopWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Stop Words Processor"

    def process(self, state: Any = None) -> Any:
        stop_words = [
            "the", "to", "and", "a",
            "in", "it", "is", "am",
            "I", "that", "had", "on",
            "for", "be", "were", "was",
            "of", "or", "it", "an",
        ]

        result = state

        for stop_word in stop_words:
            result = re.sub(
                rf"\W+{stop_word.title()}\W+", " ",
                re.sub(
                    rf"\W+{stop_word}\W+", " ",
                    state
                )
            )

        return result
```

### 3- Remove Numbers Processor

```python
class RemoveNumbersProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Numbers Processor"

    def process(self, state: Any = None) -> Any:
        return re.sub(r"\d+", "", state)
```

### Runner

the runner is the place where everything comes together, it will use the [Reader](#reader) to load the file
and define the running loop for the [Processor](#processors)

we'll be using the built in `BaseRunner`

```python
from runners.base import BaseRunner

runner = BaseRunner(
    processors=[
        LowerCaseProcessor(),
        RemoveStopWordsProcessor(),
        RemoveNumbersProcessor(),
    ],
    reader=FileReader(
        file_path="test.txt"
    ),
    configuration=RunnerConfiguration(
        post_processors=[],
        post_processors=[],
        verbose=True,
        run_timers=True
    )
)

print(runner.run())
```


`processors` parameter will set the processors of the pipeline and also its order.

`reader` parameter will set the reader of the pipeline to be the file reader we defined earlier.

`configuration` parameter will set the configuration for the runner.

`verbose` will print the current processor that is running and `run_timers` will print the time consumed by each processor to run and you can also set `pre-processors` and `post-processors` that will run before and after each processor.

for more information visit the documentation at [pypeliner](https://pypeliner.readthedocs.io/en/latest/)
