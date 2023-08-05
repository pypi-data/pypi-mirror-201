#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager
from json import dumps, load, loads
from pathlib import Path
from shutil import copytree
from subprocess import CalledProcessError, run
from sys import stderr
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import main, TestCase

from numlpa import kits


dir_tests = Path(__file__).parent
dir_material = dir_tests/'material'

with open(dir_tests/'references.json', 'r', encoding='utf-8') as ref_file:
    ref = load(ref_file)


def runcheck(command):
    """Run a command and check the exit code.

    If the exit code of the executed command is different from 0, a
    RuntimeError containing the output of the command is raised.

    Parameters
    ----------
    command : str
        Command to be runned.

    Raises
    ------
    RuntimeError
        If the command exited with an error code.

    """
    with TemporaryFile() as file:
        try:
            run(command, shell=True, check=True, stdout=file, stderr=file)
        except CalledProcessError as error:
            file.seek(0)
            raise RuntimeError(file.read().decode()) from error


@contextmanager
def temporary(directory='.'):
    """Return a temporary clone of the target test directory.

    Parameters
    ----------
    directory : str
        Name of the directory to clone from material.

    Returns
    -------
    str
        Path to the cloned target directory.

    """
    temp_dir = TemporaryDirectory()
    path = Path(temp_dir.name)
    copytree(dir_material/directory, path, dirs_exist_ok=True)
    try:
        yield path
    finally:
        temp_dir.cleanup()


def display(data):
    """Print data in JSON format.

    Parameters
    ----------
    data : dict or list
        Data to be displayed.

    """
    print("\n"+dumps(rounded(data), indent=4), file=stderr)


def rounded(data):
    """Decreases the float precision.

    Transcendental functions can have very close but different results
    for different implementations. The goal here is to hide the part
    of the number that may be different for different implementations.

    Parameters
    ----------
    data
        JSON serializable data.

    Returns
    -------
    Any
        Data with decreased precision.

    """
    def parse_float(number):
        return float(f'{float(number):1.7e}')
    return loads(dumps(data, indent=4), parse_float=parse_float)


class TestKits(TestCase):
    """Class for testing kits."""

    def test_distributions(self):
        """Test dislocation distributions."""
        self.__dict__['maxDiff'] = None
        tested = kits.names('distributions')
        for name in tested:
            with self.subTest(name=name):
                distribution = kits.get('distributions', name)
                parameters = ref['distributions'][name]['parameters']
                dat = distribution.draw(**parameters)
                self.assertEqual(
                    ref['distributions'][name]['returns']['positions'],
                    rounded(dat['dislocations']['positions']),
                )
                self.assertEqual(
                    ref['distributions'][name]['returns']['senses'],
                    dat['dislocations']['senses'],
                )
                self.assertEqual(
                    ref['distributions'][name]['returns']['density'],
                    rounded(dat['distribution']['density']),
                )

    def test_diffractometers(self):
        """Test diffractometers."""
        self.__dict__['maxDiff'] = None
        tested = kits.names('diffractometers')
        for name in tested:
            for kind in ('screw', 'edge',):
                with self.subTest(name=name, kind=kind):
                    params_key = f'parameters-{kind}'
                    return_key = f'returns-{kind}'
                    diffractometer = kits.get('diffractometers', name)
                    parameters = ref['diffractometers'][name][params_key]
                    dat = diffractometer.diffract(**parameters)
                    self.assertEqual(
                        ref['diffractometers'][name][return_key],
                        rounded(dat['coefficients']),
                    )

    def test_models(self):
        """Test LPA models."""
        self.__dict__['maxDiff'] = None
        tested = kits.names('models')
        for name in tested:
            transform = ref['models'][name]['parameters']['transform']
            harmonic = ref['models'][name]['parameters']['harmonic']
            parameters = ref['models'][name]['parameters']['parameters']
            model = kits.get('models', name)
            dat = model.model(transform, harmonic)(*parameters)
            self.assertEqual(
                ref['models'][name]['returns'],
                rounded(list(dat)),
            )


class TestCommandLineInterface(TestCase):
    """Class for testing the command-line interface."""

    def test_draw(self):
        """Test draw command."""
        for distribution in kits.names('distributions'):
            with self.subTest(distribution=distribution):
                with temporary() as target:
                    runcheck(f"cd {target}; numlpa draw {distribution}")

    def test_diffract(self):
        """Test diffract command."""
        for diff in kits.names('diffractometers'):
            with self.subTest(diff=diff):
                with temporary() as target:
                    runcheck(f"cd {target}; numlpa draw samples -n 1")
                    runcheck(f"cd {target}; numlpa diffract samples {diff}")


if __name__ == '__main__':
    main()
