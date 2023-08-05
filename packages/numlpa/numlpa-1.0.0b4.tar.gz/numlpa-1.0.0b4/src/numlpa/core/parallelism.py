# -*- coding: utf-8 -*-

"""Parallelization on multiple machines.

This module implements the functionalities for retrieving the rank of
the machine and the number of machines allocated to the current task.

"""

from logging import getLogger, Formatter
from os import getenv

from numlpa import config


logger = getLogger(__name__)


def get_rank():
    """Return the rank of the machine.

    Returns
    -------
    int
        Rank of the machine.

    """
    logger.debug("retrieving rank")
    variable = config.get(__name__, 'rank')
    return int(getenv(variable, '0'))


def get_size():
    """Return the number of allocated machines.

    Returns
    -------
    int
        Number of allocated machines.

    """
    logger.debug("retrieving size")
    variable = config.get(__name__, 'size')
    return int(getenv(variable, '1'))


def get_format():
    """Return the format to use for logging on this machine.

    Returns
    -------
    str
        Logging format.

    """
    formatter = []
    formatter.append('%(levelname)s')
    size = get_size()
    if size > 1:
        width = len(str(size-1))
        formatter.append(str(get_rank()).zfill(width))
    formatter.append('%(name)s')
    formatter.append('%(message)s')
    return ':'.join(formatter)


getLogger().handlers[0].setFormatter(Formatter(get_format()))
