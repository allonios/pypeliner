"""
Runner configuration module contains runner configuration modeling.
"""

from dataclasses import dataclass
from typing import List, Optional

from pypeliner.processors.base import BaseProcessor


@dataclass
class RunnerConfiguration:
    """
    A configuration class used to configure the runner behaviour.

    pre_processors: A list of preprocessors that will run before each processor.
    post_processors: A list of preprocessors that will run after each processor.
    deep_copy_state: Whether to copy the state or not. Defaults to True.
    verbose: Whether to output running status on terminal. Defaults to False.
    run_timers: Whether to print the timing for each processor. Defaults to False.
    timers_decimal_places: when run_timers is True,
        it will specify the number of decimal points for the measured time,
        if run_timers is False and this parameter is specified
        it will have no effect. Defaults to 3.
    """

    pre_processors: Optional[List[BaseProcessor]] = None
    post_processors: Optional[List[BaseProcessor]] = None
    deep_copy_state: bool = True
    verbose: bool = False
    run_timers: bool = False
    timers_decimal_places: int = 3
