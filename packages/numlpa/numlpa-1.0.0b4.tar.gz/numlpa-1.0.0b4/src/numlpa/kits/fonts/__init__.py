# -*- coding: utf-8 -*-

"""Text fonts for figures.

This package gathers the different fonts available and implements the
functionalities to list the names and get the path of the files.

"""

from importlib import resources


def names():
    """Return the name of the available fonts.

    Returns
    -------
    list of str
        Names of the available fonts.

    """
    return []


def path(name):
    """Return the path to the font file.

    Parameters
    ----------
    name : str
        Name of the font.

    Returns
    -------
    str
        Path to the font file.

    """
    with resources.path(__package__, name) as file:
        file = str(file)
    return file
