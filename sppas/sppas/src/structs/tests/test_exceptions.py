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

    src.structs.tests.test_exceptions.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..structsexc import MetaKeyError
from ..structsexc import LangTypeError
from ..structsexc import LangNameError
from ..structsexc import LangPathError

# ---------------------------------------------------------------------------


class TestExceptions(unittest.TestCase):

    def test_glob_exceptions(self):
        try:
            raise MetaKeyError("clé")
        except Exception as e:
            self.assertTrue(isinstance(e, MetaKeyError))
            self.assertTrue('6010' in str(e))

    def test_lang_exceptions(self):
        try:
            raise LangTypeError("français")
        except Exception as e:
            self.assertTrue(isinstance(e, LangTypeError))
            self.assertTrue('6020' in str(e))

        try:
            raise LangPathError("directory/folder")
        except Exception as e:
            self.assertTrue(isinstance(e, LangPathError))
            self.assertTrue('6024' in str(e))

        try:
            raise LangNameError("iso639-3")
        except Exception as e:
            self.assertTrue(isinstance(e, LangNameError))
            self.assertTrue('6028' in str(e))
