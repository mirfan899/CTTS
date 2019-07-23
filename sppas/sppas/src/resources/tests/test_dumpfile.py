# -*- coding: utf8 -*-
# -*- coding: UTF-8 -*-
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

    src.resources.tests.test_dumpfile.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..dumpfile import sppasDumpFile
from ..resourcesexc import DumpExtensionError

# ---------------------------------------------------------------------------


class TestDumpFile(unittest.TestCase):

    def test_extension(self):
        dp = sppasDumpFile("E://data/toto.txt")
        self.assertEqual(dp.get_dump_extension(), sppasDumpFile.DUMP_FILENAME_EXT)
        dp.set_dump_extension(".DUMP")
        self.assertEqual(dp.get_dump_extension(), ".DUMP")
        dp.set_dump_extension("DUMP")
        self.assertEqual(dp.get_dump_extension(), ".DUMP")
        dp.set_dump_extension()
        self.assertEqual(dp.get_dump_extension(), sppasDumpFile.DUMP_FILENAME_EXT)
        with self.assertRaises(DumpExtensionError):
            dp.set_dump_extension(".txt")
        with self.assertRaises(DumpExtensionError):
            dp.set_dump_extension(".TXT")
        with self.assertRaises(DumpExtensionError):
            dp.set_dump_extension("TXT")

    def test_filename(self):
        dp = sppasDumpFile("E://data/toto.txt")
        self.assertEqual(dp.get_dump_filename(), "E://data/toto.dump")
        self.assertFalse(dp.has_dump())
