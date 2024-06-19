# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'Snail in the bar'
copyright = '2024, ebonicra, scrimgeo, withersh'
author = 'ebonicra, scrimgeo, withersh'
release = '1.0.0'
html_logo = 'logo.jpg'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Опции для HTML вывода --------------------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Опции для автодокументации --------------------------------------------------------

autodoc_mock_imports = ["aiogram", "logging", "argparse"]



