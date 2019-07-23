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

    src.structs.tests.test_tips.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TODO: test save

"""
import unittest

from ..tips import sppasTips

# ---------------------------------------------------------------------------


class TestTips(unittest.TestCase):

    def test_init(self):
        tips = sppasTips()
        self.assertGreater(len(tips), 8)

    def test_get_message(self):
        tips = sppasTips()
        t = tips.get_message()
        self.assertGreater(len(t), 8)

    def test_add_message(self):
        tips = sppasTips()
        cur = len(tips)
        tips.add_message("This is a new tips.")
        self.assertEqual(len(tips), cur+1)


