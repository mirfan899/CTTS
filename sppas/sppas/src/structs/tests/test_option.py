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

    src.structs.tests.test_option.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi

"""
import unittest

from ..baseoption import sppasBaseOption, sppasOption

# ---------------------------------------------------------------------------


class TestOption(unittest.TestCase):

    def test_init_(self):
        sppasBaseOption("int", 3)
        sppasOption("three", "int", 3)

    def test_baseoption_get(self):
        o = sppasBaseOption("integer", "3")
        self.assertEqual(o.get_value(), 3)
        self.assertEqual(o.get_untypedvalue(), "3")
        self.assertEqual(o.get_type(), "int")
        self.assertEqual(o.get_name(), "")
        self.assertEqual(o.get_text(), "")
        self.assertEqual(o.get_description(), "")

        o = sppasBaseOption("toto", "3")
        self.assertEqual(o.get_value(), "3")
        self.assertEqual(o.get_untypedvalue(), "3")
        self.assertEqual(o.get_type(), "str")

    def test_option(self):
        o = sppasBaseOption("opt")
        self.assertEqual(o.get_value(), "")
        self.assertEqual(o.get_untypedvalue(), "")
        self.assertEqual(o.get_type(), "str")
        self.assertEqual(o.get_name(), "")
        self.assertEqual(o.get_text(), "")
        self.assertEqual(o.get_description(), "")

    def test_option_encoding(self):
        o = sppasBaseOption("str", "çéùàï")
        self.assertEqual(o.get_value(), u"çéùàï")
        self.assertEqual(o.get_untypedvalue(), "çéùàï")
        self.assertEqual(o.get_type(), "str")
        self.assertEqual(o.get_name(), "")
        self.assertEqual(o.get_text(), "")
        self.assertEqual(o.get_description(), "")

        o = sppasBaseOption("str", 3)
        self.assertEqual(o.get_value(), "3")
