"""
This type stub file was generated by pyright.
"""

from __future__ import absolute_import, division, print_function
from unittest import TestCase
from ._private.utils import *
from ._private import decorators as dec
from ._private.nosetester import NoseTester as Tester, run_module_suite
from numpy._pytesttester import PytestTester

"""Common test support for all numpy test scripts.

This single module should provide all the common functionality for numpy tests
in a single location, so that test scripts can just import it and work right
away.

"""
test = PytestTester(__name__)