# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


sys.path.insert(0, os.path.abspath('../../src/sfrout'))

project = 'sfrout'
copyright = '2023, Lukasz Hoszowski'
author = 'Lukasz Hoszowski'
release = '0.0.7'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosectionlabel',
              "sphinx.ext.viewcode",
              'sphinx.ext.duration',
              'sphinx.ext.coverage',
              'sphinx_click.ext']

# autodoc_default_flags = [
#     'members',
#     'undoc-members',
#     'private-members',
#     'special-members',
#     'inherited-members',
#     'show-inheritance'
# ]

autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
