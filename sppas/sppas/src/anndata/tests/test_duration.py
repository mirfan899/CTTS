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

    src.anndata.tests.test_duration
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test annlocation package related to duration.

"""
import unittest

from ..ann.annlocation import sppasDuration
from ..ann.annlocation import sppasDurationCompare
from ..anndataexc import AnnDataTypeError
from ..anndataexc import AnnDataNegValueError

# ---------------------------------------------------------------------------


class TestDuration(unittest.TestCase):

    def setUp(self):
        self.point0 = sppasDuration(0)
        self.pointV = sppasDuration(1.000, 0.001)
        self.pointW = sppasDuration(1.001, 0.001)
        self.pointX = sppasDuration(1.002, 0.001)
        self.pointY = sppasDuration(1.003, 0.003)
        self.pointZ = sppasDuration(1.003, 0.001)

    # -----------------------------------------------------------------------

    def test__eq__(self):
        """
        x = y iff
        |x - y| < dx + dy
        """
        # abs(1.000 - 1.001) < 0.001 + 0.001
        self.assertEqual(self.pointV, self.pointW)

        # abs(1.000 - 1.003) < 0.001 + 0.003
        self.assertEqual(self.pointV, self.pointY)

        # abs(1.000 - 1.002) < 0.001 + 0.001
        self.assertNotEqual(self.pointV, self.pointX)

    # -----------------------------------------------------------------------

    def test__lt__(self):
        """
        x < y iff:
        x != y && x < y
        """
        # 1.000 + (0.001 + 0.001) < 1.003
        # self.assertTrue(self.pointV < self.pointZ)
        self.assertLess(self.pointV, self.pointZ)

        # 1.000 + (0.001 + 0.001) < 1.002
        self.assertLess(self.pointV, self.pointX)

    # -----------------------------------------------------------------------

    def test__gt__(self):
        """
        x > y iff:
        x != y && x > y
        """
        # 1.003 - (0.001 + 0.001) > 1.001
        self.assertGreater(self.pointZ, self.pointV)
        # 1.002 - (0.001 + 0.001) > 1.001
        self.assertGreater(self.pointX, self.pointV)
        self.assertGreater(self.pointX, 1.001)

    # -----------------------------------------------------------------------

    def test__ne__(self):
        self.assertNotEqual(self.pointV, self.pointX)

    # -----------------------------------------------------------------------

    def test__le__(self):
        self.assertLessEqual(self.pointV, self.pointZ)
        self.assertLessEqual(self.pointV, self.pointW)

    # -----------------------------------------------------------------------

    def test__ge__(self):
        self.assertGreater(self.pointX, self.pointV)
        self.assertGreaterEqual(self.pointX, self.pointV)

        self.assertEqual(self.pointV, 1)
        self.assertEqual(self.pointV, 1.001)
        self.assertGreaterEqual(self.pointV, 1.001)
        self.assertGreaterEqual(self.pointV, 0.999)
        self.assertEqual(self.pointV, self.pointW)
        self.assertGreaterEqual(self.pointV, self.pointV)
        self.assertGreaterEqual(self.pointV, self.pointW)

    # -----------------------------------------------------------------------

    def test_get_set(self):
        point0 = sppasDuration(0.1, 0.2)
        self.assertEqual(point0.get_value(), 0.1)
        self.assertEqual(point0.get_margin(), 0.2)
        point1 = point0
        self.assertEqual(point0, point1)
        self.assertTrue(point1 is point0)
        point2 = point0.copy()
        self.assertEqual(point0, point2)
        self.assertFalse(point2 is point0)
        point3 = sppasDuration(0.1, 0.2)
        point2.set(point3)
        self.assertFalse(point2 is point3)

        # now, test errors
        point0 = sppasDuration(0.1)
        with self.assertRaises(AnnDataTypeError):
            point0.set([9])
        with self.assertRaises(AnnDataTypeError):
            point0.set_value([9])
        with self.assertRaises(AnnDataTypeError):
            point0.set_margin([9])
        with self.assertRaises(AnnDataNegValueError):
            point0.set_value(-5)
        with self.assertRaises(AnnDataNegValueError):
            point0.set_margin(-5)

# ---------------------------------------------------------------------------


class TestDurationCompare(unittest.TestCase):
    """Test methods to compare durations."""

    def setUp(self):
        self.dc = sppasDurationCompare()

    # -----------------------------------------------------------------------

    def test_members(self):
        """Test methods getter."""

        self.assertEqual(self.dc.methods['eq'], self.dc.eq)
        self.assertEqual(self.dc.get('eq'), self.dc.eq)

        self.assertEqual(self.dc.methods['ne'], self.dc.ne)
        self.assertEqual(self.dc.get('ne'), self.dc.ne)

        self.assertEqual(self.dc.methods['gt'], self.dc.gt)
        self.assertEqual(self.dc.get('gt'), self.dc.gt)

        self.assertEqual(self.dc.methods['ge'], self.dc.ge)
        self.assertEqual(self.dc.get('ge'), self.dc.ge)

        self.assertEqual(self.dc.methods['lt'], self.dc.lt)
        self.assertEqual(self.dc.get('lt'), self.dc.lt)

        self.assertEqual(self.dc.methods['le'], self.dc.le)
        self.assertEqual(self.dc.get('le'), self.dc.le)

    # -----------------------------------------------------------------------

    def test_eq(self):
        """dur == x."""

        self.assertTrue(self.dc.eq(sppasDuration(1, 0.02), 1.01))
        self.assertFalse(self.dc.eq(sppasDuration(1, 0.02), sppasDuration(2)))

        with self.assertRaises(TypeError):
            self.dc.eq(1, 1)
