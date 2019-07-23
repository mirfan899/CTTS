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

    src.calculus.tests.test_kappa.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from sppas.src.calculus.scoring.kappa import sppasKappa

# ---------------------------------------------------------------------------


class TestVectorKappa(unittest.TestCase):

    def setUp(self):
        self.p = [(1.0, 0.0), (0.0, 1.0), (0.0, 1.0), (1.0, 0.0), (1.0, 0.0)]
        self.q = [(1.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 0.0), (1.0, 0.0)]

    def test_kappa(self):
        kappa = sppasKappa(self.p, self.q)
        self.assertTrue(kappa.check())  # check both p and q
        self.assertFalse(kappa.check_vector([(0., 1.), (0., 1., 0.)]))
        self.assertFalse(kappa.check_vector([(0.0, 0.1)]))
        v = kappa.evaluate()
        self.assertEqual(0.54545, round(v, 5))

    def test_kappa3(self):
        p = [(1., 0., 0.), (0., 0., 1.), (0., 1., 0.), (1., 0., 0.), (0., 0., 1.)]
        q = [(0., 0., 1.), (0., 0., 1.), (1., 0., 0.), (0., 1., 0.), (0., 0., 1.)]
        kappa = sppasKappa(p, q)
        v = kappa.evaluate()
        self.assertEqual(0.0625, round(v, 5))
