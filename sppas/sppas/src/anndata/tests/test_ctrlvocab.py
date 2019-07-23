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

    src.anndata.tests.test_tier
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the class sppasCtrlVocab().

"""
import unittest

from sppas.src.utils.makeunicode import u
from ..anndataexc import AnnDataTypeError
from ..ctrlvocab import sppasCtrlVocab
from ..ann.annlabel import sppasTag

# ---------------------------------------------------------------------------


class TestCtrlVocab(unittest.TestCase):
    """A controlled Vocabulary is a set of tags."""

    def setUp(self):
        pass

    # -----------------------------------------------------------------------

    def test_identifier(self):
        voc = sppasCtrlVocab("être être")
        self.assertEqual(voc.get_name(), u("être_être"))

    # -----------------------------------------------------------------------

    def test_add(self):
        voc = sppasCtrlVocab("Verbal Strategies")
        self.assertEqual(len(voc), 0)
        self.assertTrue(voc.add(sppasTag("definition")))
        self.assertTrue(voc.add(sppasTag("example")))
        self.assertTrue(voc.add(sppasTag("comparison")))
        self.assertTrue(voc.add(sppasTag("gap filling with sound")))
        self.assertFalse(voc.add(sppasTag("definition")))
        self.assertEqual(len(voc), 4)
        with self.assertRaises(AnnDataTypeError):
            voc.add("bla")

        voc_int = sppasCtrlVocab("Intensity")
        self.assertTrue(voc_int.add(sppasTag(1, "int")))
        self.assertTrue(voc_int.add(sppasTag(2, "int")))
        self.assertFalse(voc_int.add(sppasTag(1, "int")))
        with self.assertRaises(AnnDataTypeError):
            # 1 is converted into "str" type by sppasTag. (we expect 'int')
            voc_int.add(sppasTag(1))
        with self.assertRaises(AnnDataTypeError):
            voc_int.add(2)

    # -----------------------------------------------------------------------

    def test_contains(self):
        voc = sppasCtrlVocab("Verbal Strategies")
        self.assertTrue(voc.add(sppasTag("definition")))
        self.assertTrue(voc.add(sppasTag("example")))
        self.assertTrue(voc.add(sppasTag("comparison")))
        self.assertTrue(voc.add(sppasTag("gap filling with sound")))
        self.assertFalse(voc.add(sppasTag(" gap filling with sound ")))
        self.assertTrue(voc.add(sppasTag("contrast")))
        self.assertFalse(voc.add(sppasTag("definition")))
        self.assertTrue(voc.contains(sppasTag("definition")))
        self.assertTrue(voc.contains(sppasTag("   \t  definition\r\n")))
        with self.assertRaises(AnnDataTypeError):
            voc.contains("definition")

        voc_int = sppasCtrlVocab("Intensity")
        self.assertTrue(voc_int.add(sppasTag(1, "int")))
        self.assertTrue(voc_int.add(sppasTag(2, "int")))
        self.assertTrue(voc_int.contains(sppasTag(2, "int")))
        self.assertFalse(voc_int.contains(sppasTag(2, "str")))
        self.assertFalse(voc_int.contains(sppasTag(2)))

    # -----------------------------------------------------------------------

    def test_remove(self):
        voc = sppasCtrlVocab("Verbal Strategies")
        self.assertTrue(voc.add(sppasTag("definition")))
        self.assertTrue(voc.add(sppasTag("example")))
        self.assertTrue(voc.remove(sppasTag("example")))
        self.assertFalse(voc.remove(sppasTag("example")))
        with self.assertRaises(AnnDataTypeError):
            voc.remove("definition")
