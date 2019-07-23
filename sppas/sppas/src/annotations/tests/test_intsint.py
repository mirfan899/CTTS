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

    src.annotations.tests.test_normalize.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test INTSINT.

    These tests should be extended...

"""
import unittest

from ..Intsint import Intsint, sppasIntsint

# ---------------------------------------------------------------------------


class TestIntsint(unittest.TestCase):
    """Test of the class Intsint."""

    def setUp(self):
        self.anchors = [(0.1, 240), (0.4, 340), (0.6, 240), (0.7, 286)]

    def test_intsint(self):
        result = Intsint().annotate(self.anchors)
        self.assertEqual(len(self.anchors), len(result))
        self.assertEqual(['M', 'T', 'L', 'H'], result)

        with self.assertRaises(IOError):
            Intsint().annotate([(0.1, 240)])

    def test_sppasintsint(self):
        si = sppasIntsint()
        # to be continued...
