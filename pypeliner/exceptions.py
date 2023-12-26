"""
Exceptions module, contains raised exceptions by pypeliner.
"""


class MissingDependencyError(Exception):
    """
    Raised when a library that a reader, processor or a runner depends on
    """
