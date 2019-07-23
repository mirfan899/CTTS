# -*- coding: utf8 -*-
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

    src.annotations.tests.test_otherrepet.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..SelfRepet.datastructs import DataSpeaker
from ..OtherRepet.rules import OtherRules

# ---------------------------------------------------------------------------


class TestOtherRules(unittest.TestCase):

    def test_rule_strict(self):
        r = OtherRules(['euh'])
        d1 = DataSpeaker(["tok1", "tok2", "tok3", "euh", "ok"])
        d2 = DataSpeaker(["bla", "tok1", "tok2"])
        d3 = DataSpeaker(["bla", "tok1", "tok2", "tok3"])
        d4 = DataSpeaker(["tok1", "euh", "tok2", "tok3"])
        self.assertFalse(r.rule_strict(0, 1, d1, d2))
        self.assertFalse(r.rule_strict(0, 2, d1, d2))
        self.assertTrue(r.rule_strict(0, 2, d1, d3))
        self.assertFalse(r.rule_strict(0, 2, d1, d4))

