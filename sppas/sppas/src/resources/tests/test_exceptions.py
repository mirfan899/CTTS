# -*- coding:utf-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    src.resources.tests.test_exceptions.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..resourcesexc import FileIOError, FileFormatError
from ..resourcesexc import NgramRangeError, GapRangeError, ScoreRangeError
from ..resourcesexc import DumpExtensionError

# ---------------------------------------------------------------------------


class TestExceptions(unittest.TestCase):

    def test_file_exceptions(self):
        try:
            raise FileIOError("path/filename")
        except Exception as e:
            self.assertTrue(isinstance(e, FileIOError))
            self.assertTrue("5010" in str(e))

        try:
            raise FileFormatError(10, "wrong line content or filename")
        except Exception as e:
            self.assertTrue(isinstance(e, FileFormatError))
            self.assertTrue("5015" in str(e))

        try:
            raise DumpExtensionError(".doc")
        except Exception as e:
            self.assertTrue(isinstance(e, DumpExtensionError))
            self.assertTrue("5030" in str(e))

    def test_range_exceptions(self):
        try:
            raise NgramRangeError(100, 300)  # maximum, observed
        except Exception as e:
            self.assertTrue(isinstance(e, NgramRangeError))
            self.assertTrue("5020" in str(e))

        try:
            raise GapRangeError(100, 300)  # maximum, observed
        except Exception as e:
            self.assertTrue(isinstance(e, GapRangeError))
            self.assertTrue("5022" in str(e))

        try:
            raise ScoreRangeError(3.)  # observed
        except Exception as e:
            self.assertTrue(isinstance(e, ScoreRangeError))
            self.assertTrue("5024" in str(e))
