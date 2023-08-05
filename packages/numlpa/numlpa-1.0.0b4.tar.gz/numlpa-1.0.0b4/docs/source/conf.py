# -*- coding: utf-8 -*-

"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see:
https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

from numlpa._version import __version__

# Project information

project = 'numlpa'
author = 'Dunstan Becht'
version = __version__
release = __version__

# General configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'myst_parser',
]

templates_path = []
exclude_patterns = []

# Options for HTML output

# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    # Table of contents options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': True,
    'titles_only': True,
    # Miscellaneous options
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#343131ff',
}
html_logo = "logo.svg"
html_static_path = []
html_show_copyright = False
html_show_sphinx = False
