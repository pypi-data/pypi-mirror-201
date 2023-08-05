# -*- coding: utf-8 -*-

"""Upgradeable collections of features.

This package groups by category the different implementations or
alternatives proposed to the user to perform a given task.

"""

from importlib import import_module
from os.path import join
from pkgutil import iter_modules


def names(subpackage):
    """Return the names of the modules contained in the subpackage.

    Parameters
    ----------
    subpackage : str
        Name of the subpackage.

    Returns
    -------
    list of str
        Names of the modules in the subpackage.

    """
    paths = [join(path, subpackage) for path in __path__]
    return [module.name for module in iter_modules(paths)]


def get(subpackage, module):
    """Import and return a module contained in a subpackage.

    Parameters
    ----------
    subpackage : str
        Name of the subpackage.
    module : str
        Name of the submodule.

    Returns
    -------
    ModuleType
        Module from the subpackage.

    """
    return import_module(f'{__name__}.{subpackage}.{module}')
