**************
Best Practices
**************


Here are some general tips when implementing anything using pypeliner:

#. When implementing a Reader, Processor or a Runner you are expected to inherit from the base class for these components.
#. When overriding a method of a some base class make sure you read the method and read its docstring to see if it is what you actually need, you are encouraged to always read the code for the base classes, eventually it is just simple code.
#. Processors shouldn't always be primitive typed state to be processed, in fact it can be anything, so a complex type is welcomed and encouraged to be used.
#. Call a processor with the `__call__` method inside a Runner to enforce having an initial state to be passed and updated throughout the running operations.
#. :code:`CallbackProcessor` can be helpful for oneliner processors or making a processor on the run.
#. Try to set :code:`PROCESSOR_NAME` it will be helpful when starting the Runner in verbose mode.
#. When implementing a multithreading/multiprocessing runner, override :code:`run` method to implement the threads/processes initialization and starting mechanism (you'd might run parallel processing loops or not run a loop at all).
#. In a Runner override :code:`run_processors_loop` if there are some conditions you'd like to enforce before running a certain processor.
#. For complex processing operations, you can break it into sub-pipelines by implementing each section in a pipeline with its own Runner and then create a parent Runner its Processors are calling each sub-pipeline Runner.
#. Use Stream Readers for huge files that you'd want to avoid loading in fully to the memory.
#. Try to always use the appropriate Runner wit the appropriate Reader (a stream Reader should be used with a Stream Runner).
