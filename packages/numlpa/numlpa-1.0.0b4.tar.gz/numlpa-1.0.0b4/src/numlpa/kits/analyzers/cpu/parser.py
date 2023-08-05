# -*- coding: utf-8 -*-

"""CPU spatial analyzer.

"""

from logging import getLogger


logger = getLogger(__package__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.add_argument(
        '--type',
        help="dislocation type",
        type=str,
        choices=('screw', 'edge'),
    )
    parser.add_argument(
        '--r_0',
        help="core radius (m)",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--r_roi',
        help="size of the region of interest (m)",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--r_max',
        help="maximum radius value (m)",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--steps',
        help="number of subdivision on the absice axis",
        type=int,
        metavar='int',
    )
    parser.add_argument(
        '--b_len',
        help="Burgers vector length (m)",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--poisson',
        help="Poisson number",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--shear',
        help="shear modulus (Pa)",
        type=float,
        metavar='float',
    )
    parser.add_argument(
        '--processes',
        help="number of parallel processes",
        type=int,
        metavar='int',
    )
