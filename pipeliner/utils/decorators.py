"""
Decorators module, contains exec_timer decorator.
"""

from time import time
from typing import Callable


def exec_timer(name: str = "", decimal_places: int = 3):
    """
    When a function is wrapped with this decorator, it will time the function
    execution.

    Args:
        name: verbose function name, if not specified it will use the
            function's __name__ magic attribute as a default value.
        decimal_places: the number of decimal points for the measured time.

    Returns:
        same as the function return value.
    """

    def dec_inner(func: Callable):
        def dec_inner_inner(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            if name:
                display_name = name
            else:
                display_name = func.__name__
            print(
                f"{display_name} Took "
                f"{(time() - start):.{str(decimal_places)}f} seconds"
            )
            return result

        return dec_inner_inner

    return dec_inner
