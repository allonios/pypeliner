# Pipeliner

`pipeliner` is a simple python framework for building data processing pipelines.

you can checkout the documentation [here](https://simple-pipeliner.readthedocs.io/en/latest/).

and checkout some examples [here](https://github.com/allonios/pipeliner/tree/master/pipeliner/examples).

## Installation
it can be simply installing using `pip`:

```shell
pip install pipeliner
```

## Getting Started

Let's say we want to build a pipeline for processing textual data coming from a file.
we will need 3 main components to achieve this using pipeliner.

### Reader
first we will need a reader for reading the file, and it can be defined like the following:

```python
from pipeliner.readers.base import BaseReader

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

if `input_state` is passed the that processor will use the `input_state` instead of the state passed by the runner,
this is achieved using the `super` call for `process` method and passing `input_state` there.
it is recommended to always call `super` for the `process` method as a best practice.

`PROCESSOR_NAME` is a verbose name for a processor.

#### 1- Lower Case Processor
```python
class LowerCaseProcessor(BaseProcessor):
    PROCESSOR_NAME = "Lower Case Processor"

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        return self.state.lower()
```

#### 2- Remove Stop Words Processor
```python
class RemoveStopWordsProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Stop Words Processor"

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        stop_words = [
            "the", "to", "and", "a",
            "in", "it", "is", "am,
            "I", "that", "had", "on",
            "for", "be", "were", "was",
            "of", "or", "it", "an",
        ]
        self.state = super().process(input_state)

        for stop_word in stop_words:
            self.state = re.sub(rf"\W+{stop_word}\W+", " ", self.state)
            self.state = re.sub(rf"\W+{stop_word.title()}\W+", " ", self.state)

        return self.state
```

### 3- Remove Numbers Processor

```python
class RemoveNumbersProcessor(BaseProcessor):
    PROCESSOR_NAME = "Remove Numbers Processor"

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        return re.sub(r"\d+", "", self.state)
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
    verbose=True,
    run_timers=True
)

print(runner.run())
```


`processors` parameter will set the processors of the pipeline and also its order.

`reader` parameter will set the reader of the pipeline to be the file reader we defined earlier.

`verbose` parameter will print the current processor that is running.

`run_timers` parameter will print the time consumed by each processor to run.

for more information visit the documentation at [simple-pipeliner](https://simple-pipeliner.readthedocs.io/en/latest/)
