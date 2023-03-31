"""
Exceptions module, contains raised exceptions by pypeliner.
"""


class MissingDependency(Exception):
    """
    Raised when a library that a reader, processor or a runner depends on
    """
