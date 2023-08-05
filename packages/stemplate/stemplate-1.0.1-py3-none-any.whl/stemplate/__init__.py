# -*- coding: utf-8 -*-

"""Stemplate package.

This Python package is a template.

"""

__author__ = 'Author Name'

from configparser import ConfigParser
from logging import basicConfig
from pkgutil import get_data


config = ConfigParser()
config.read_string(get_data(__package__, 'default.conf').decode())

basicConfig(level=config.get(__name__, 'log'))
