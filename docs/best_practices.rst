**************
Best Practices
**************


Here are some general tips when implementing anything using pypeliner:

#. When implementing a Reader, Processor or a Runner you are expected to inherit from the base class of these components.
#. When overriding a method of some base class make sure that you read the method and read its docstring to see if it is what you actually need, you are encouraged to always read the code of the base classes, eventually it is just simple code.
#. A complex type is welcomed and encouraged to be used as an input for a Processor, not just primitives.
#. A processor process method should only focus receiving the input/state, process it and return it (it shouldn't care about actions (registering the state and data flow related operations)).
#. Call a processor with the `__call__` method inside a Runner to enforce registering the state to make sure that the data will flow correctly through the processors.
#. :code:`CallbackProcessor` can be helpful for oneliner processors or making a processor on the run.
#. :code:`DefaultReader` can be helpful if you don't want pypeliner to handle the reading, you could just throw the value there and it will just flow.
#. Try to set :code:`PROCESSOR_NAME` it will be helpful when starting the Runner in verbose mode.
#. When implementing a multithreading/multiprocessing runner, override :code:`run` method to implement the threads/processes initialization and starting mechanism (you'd might run parallel processing loops or not run a loop at all).
#. In a Runner override :code:`run_processors_loop` if there are some conditions you'd like to enforce before running a certain processor.
#. For complex processing operations, you can break it into sub-pipelines by implementing each section in a pipeline with its own Runner and then create a parent Runner where its Processors are calling each sub-pipeline Runner.
#. Use Stream Readers for huge files that you'd want to avoid loading in fully to the memory.
#. Try to always use the appropriate Runner with the appropriate Reader (a stream Reader should be used with a Stream Runner).
