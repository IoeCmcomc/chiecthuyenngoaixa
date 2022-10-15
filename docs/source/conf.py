# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'chiecthuyenngoaixa'
copyright = '2022, IoeCmcomc'
author = 'IoeCmcomc'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    # 'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []


napoleon_google_docstring = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
