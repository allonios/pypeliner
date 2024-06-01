# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# for local build.
# sys.path.insert(0, os.path.abspath(".."))
# for rtd hosting build.
sys.path.insert(0, os.path.abspath("../.."))

project = "pypeliner"
copyright = "2024, Fareck Allony"
author = "Fareck Allony"

autodoc_mock_imports = ["cv2", "numpy", "pypeliner"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "autoapi.extension",
]

autoapi_dirs = ["../pypeliner"]

autosummary_generate = True
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
