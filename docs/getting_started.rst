***************
Getting Started
***************

| Let's say we want to build a pipeline for processing textual data coming from a file.
| we will need 3 main components to achieve this using pypeliner.

.. _reader-reference-label:

######
Reader
######

First we will need a reader for reading the file, and it can be defined as the following:

.. code-block::

    from pypeliner.readers.base import BaseReader

    class FileReader(BaseReader):
        def __init__(self, file_path: str) -> None:
            self.file_path = file_path

        def read(self) -> str:
            with open(self.file_path, "r") as file_handler:
                return file_handler.read()


Inheriting from ``BaseReader`` makes sure that the ``read`` method is implemented to be used later within the :ref:`runner-reference-label`.
the code basically is reading a file and returning its content as a string.

.. _processors-reference-label:

##########
Processors
##########

Next we will define our processing logic, let's say we want to make all letters in the text file lower case, then remove
stop words e.g: but, and, or, etc after that remove numbers.


To achieve that we will write a processor for each one of these tasks.

Each processor should define its own ``process`` method. a processor will receive the ``state`` it needs to process from the :ref:`runner-reference-label`.

If ``state`` is passed the that processor will use the ``state`` instead of the state passed by the runner,
this is achieved using the ``super`` call for ``process`` method and passing ``state`` there.
it is recommended to always call ``super`` for the ``process`` method as a best practice.

``PROCESSOR_NAME`` is a verbose name for a processor.

-----------------------
1- Lower Case Processor
-----------------------

.. code-block::

    class LowerCaseProcessor(BaseProcessor):
        PROCESSOR_NAME = "Lower Case Processor"

        def process(self, state: Any = None) -> Any:
            return state.lower()



------------------------------
2- Remove Stop Words Processor
------------------------------

.. code-block::

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

            result = ""

            for stop_word in stop_words:
                result = re.sub(
                    rf"\W+{stop_word.title()}\W+", " ",
                    re.sub(
                        rf"\W+{stop_word}\W+", " ",
                        state
                    )
                )

            return result




---------------------------
3- Remove Numbers Processor
---------------------------

.. code-block::

    class RemoveNumbersProcessor(BaseProcessor):
        PROCESSOR_NAME = "Remove Numbers Processor"

        def process(self, state: Any = None) -> Any:
            return re.sub(r"\d+", "", state)


.. _runner-reference-label:

######
Runner
######

The runner is the place where everything comes together, it will use the :ref:`reader-reference-label` to load the file
and define the running loop for the :ref:`processors-reference-label`

We'll be using the built in :doc:`BaseRunner <_autosummary/pypeliner.runners.base.BaseRunner>`

.. code-block::

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

| ``processors`` parameter will set the processors of the pipeline and also its order.
| ``reader`` parameter will set the reader of the pipeline to be the file reader we defined earlier.
| ``configuration`` parameter will set the configuration for the runner.
| ``verbose`` will print the current processor that is running and ``run_timers`` will print the time consumed by each processor to run and you can also set ``pre-processors`` and ``post-processors`` that will run before and after each processor.
