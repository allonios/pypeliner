"""
Exceptions module, contains raised exceptions by pypeliner.
"""


class MissingDependencyError(Exception):
    """
    Raised when a library that a reader, processor or a runner depends on
    """


class StateIntegrityError(Exception):
    """
    Raised when an error regarding the state integrity happens,
    e.g: trying to set state to None.
    """
