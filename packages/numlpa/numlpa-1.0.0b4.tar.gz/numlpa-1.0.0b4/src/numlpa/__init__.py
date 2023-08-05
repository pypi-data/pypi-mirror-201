# -*- coding: utf-8 -*-

"""Numerical Line Profile Analysis package.

This Python package is intended for the analysis of crystal
microstructure characterization models from simulated X-ray
diffraction line profiles.

"""

__author__ = 'Dunstan Becht'

from configparser import ConfigParser
from logging import basicConfig
from pkgutil import get_data


config = ConfigParser()
config.read_string(get_data(__package__, 'default.conf').decode())

basicConfig(level=config.get(__name__, 'log'))
