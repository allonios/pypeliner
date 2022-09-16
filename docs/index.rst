.. pipeliner documentation master file, created by
   sphinx-quickstart on Sat Sep  3 21:40:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pipeliner's documentation!
=====================================

********
Pipliner
********

`pipeliner` is a simple python framework for building data processing pipelines.

The main goal for pipeliner is to make processing units as robust as it can be by making it

- usable outside of the framework environment so you don't need redefine the processor logic when using this logic outside of the pipeline.

- testable.

- easily used in any desired order within the pipeline.



.. toctree::
   :maxdepth: 1
   :caption: Table of Contents:

   API Reference <_autosummary/pipeliner>

************
Installation
************

pypi
~~~~
it can be simply installing using `pip`::

    pip install librosa

github (for development)
~~~~~~~~~~~~~~~~~~~~~~~~
or by cloning the repo::

   git clone https://github.com/allonios/pipeliner.git
   pip install -r requirements.txt
   # for development
   pip install pre-commit
