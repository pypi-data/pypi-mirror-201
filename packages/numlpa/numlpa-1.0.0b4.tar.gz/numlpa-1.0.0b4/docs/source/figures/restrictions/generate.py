#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Restriction figure generator.

"""

from matplotlib import font_manager
from matplotlib.pyplot import rcParams
import matplotlib.pyplot as plt
import numpy as np

from numlpa import config, kits
from numlpa.kits import fonts


font = config.get('numlpa.main.export', 'font')
math = config.get('numlpa.main.export', 'math')
prop = font_manager.FontProperties(fname=fonts.path(font))
font_manager.fontManager.addfont(fonts.path(font))
rcParams["font.family"] = prop.get_name()
rcParams["mathtext.fontset"] = math


def export_basic(restriction, file, variable, amplitude):
    """Export a figure to illustrate the restriction.

    """
    fig, ax = plt.subplots()
    ax.plot(variable, amplitude, "o-", label="simulated $A(L)$")
    i = restriction.limit(variable, amplitude)
    ax.plot(variable[:i], amplitude[:i], ".-", label="restricted $A(L)$")
    ax.grid()
    ax.legend()
    ax.set_xlabel("$L$")
    fig.savefig(file)


def export_affine(restriction, file, variable, amplitude):
    """Export a figure to illustrate the restriction.

    """
    i = restriction.limit(variable, amplitude)
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    amplitude = np.log(amplitude)/variable**2
    ax.plot(variable, amplitude, "o-", label="simulated $\ln[A(L)]/L^2$")
    ax.plot(variable[:i], amplitude[:i], label="restricted $\ln[A(L)]/L^2$")
    ax.grid()
    ax.legend()
    ax.set_xlabel("$L$")
    fig.savefig(file)


if __name__ == '__main__':

    export_affine(
        kits.get('restrictions', 'affine'),
        'affine.svg',
        np.exp(np.array([0, 1, 2, 3, 4, 5, 6, 7])),
        np.exp(
            np.exp(np.array([0, 1, 2, 3, 4, 5, 6, 7]))**2 *
            (np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.2, 6.8, 8.6])/100000-0.0002),
        )
    )

    export_basic(
        kits.get('restrictions', 'none'),
        'none.svg',
        np.array([0, 1, 2, 3, 4, 5, 6, 7]),
        np.array([10, 9.5, 8.5, 6.5, 2.5, 3, -2, -1])/10,
    )

    export_basic(
        kits.get('restrictions', 'positive'),
        'positive.svg',
        np.array([0, 1, 2, 3, 4, 5, 6, 7]),
        np.array([10, 9.5, 8.5, 6.5, 2.5, 3, -2, -1])/10,
    )
