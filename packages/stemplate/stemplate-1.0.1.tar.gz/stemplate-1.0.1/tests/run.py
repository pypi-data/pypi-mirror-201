#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager
from json import load, dumps
from pathlib import Path
from shutil import copytree
from subprocess import CalledProcessError, run
from sys import stderr
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import main, TestCase

from stemplate.core import colors, files


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
    print("\n"+dumps(data, indent=4), file=stderr)


class TestCore(TestCase):
    """Class for testing core subpackage."""

    def test_files_get_content(self):
        """Test file content retrieval."""
        with temporary() as material:
            content = files.get_beginning(material/'data.txt', 1)
            self.assertEqual(ref['file']['content'], content)

    def test_files_get_size(self):
        """Test file size retrieval."""
        with temporary() as material:
            size = files.get_size(material/'data.txt')
            self.assertEqual(ref['file']['size'], size)

    def test_colors_get_code(self):
        """Test color code retrieval."""
        code = colors.get_code('red')
        self.assertEqual('\033[31m', code)


class TestCommandLineInterface(TestCase):
    """Class for testing the CLI."""

    def test_help(self):
        """Test help option."""
        runcheck("stemplate --help")
        runcheck("stemplate head --help")
        runcheck("stemplate date --help")

    def test_head(self):
        """Test head subparser."""
        with temporary() as material:
            runcheck(f"stemplate head {material}/data.txt")
            runcheck(
                f"stemplate -c {material}/custom.conf "
                f"head {material}/data.txt"
            )

    def test_date(self):
        """Test date subparser."""
        with temporary() as material:
            runcheck("stemplate date")
            runcheck(f"stemplate -c {material}/custom.conf date")


if __name__ == '__main__':
    main()
