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

    src.calculus.tests.test_geometry.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest
import random
import time

from ..geometry.distances import squared_euclidian, euclidian, manathan, minkowski, chi_squared
from ..geometry.linear_fct import slope_intercept, linear_fct, linear_values
from ..calculusexc import VectorsError

# ---------------------------------------------------------------------------


def random_vectors(size):
    x = [random.randint(0, 100) for i in range(size)]
    y = [random.randint(0, 100) for i in range(size)]
    return x, y

# ---------------------------------------------------------------------------


class TestGeometryLinearFct(unittest.TestCase):

    def test_slope_intercept(self):
        """Returns the slope and the intercept."""

        a, b = slope_intercept(p1=(1, 1), p2=(3, 3))
        self.assertEqual(a, 1.)
        self.assertEqual(b, 0.)

        a, b = slope_intercept(p1=(1, 1), p2=(30., 30.))
        self.assertEqual(a, 1.)
        self.assertEqual(b, 0.)

        a, b = slope_intercept(p1=(1, 2), p2=(2., 3.))
        self.assertEqual(a, 1.)
        self.assertEqual(b, 1.)

        # errors
        with self.assertRaises(Exception):
            slope_intercept(p1=("a", "b"), p2=(30., 30.))
        with self.assertRaises(Exception):
            slope_intercept(p1=(1, 1), p2=(1, 1))

    # -----------------------------------------------------------------------

    def test_linear_fct(self):
        """Return f(x) of the linear function f(x) = ax + b."""

        y = linear_fct(2, 1., 0.)
        self.assertEqual(y, 2.)

        y = linear_fct(2, 1., 2.)
        self.assertEqual(y, 4.)

    # -----------------------------------------------------------------------

    def test_linear_values(self):
        """Estimate the values between 2 points, step-by-step."""

        y_values = linear_values(2, p1=(2, 2), p2=(8., 8.))
        self.assertEqual(len(y_values), 4)
        self.assertEqual(y_values[0], 2.)
        self.assertEqual(y_values[1], 4.)
        self.assertEqual(y_values[2], 6.)
        self.assertEqual(y_values[3], 8.)

        y_values = linear_values(2.5, p1=(2, 2), p2=(8., 8.))
        self.assertEqual(len(y_values), 4)
        self.assertEqual(y_values[0], 2.)   # p1. x=2
        self.assertEqual(y_values[1], 4.5)  # p1+delta, x=4.5
        self.assertEqual(y_values[2], 7.)   # p2+delta, x=7
        self.assertEqual(y_values[3], 8.)   # p2. x=8.

        y_values = linear_values(0.01, p1=(0, 0), p2=(1., 1.))
        self.assertEqual(len(y_values), 101)
        self.assertEqual(y_values[100], 1.)

        y_values = linear_values(0.01, p1=(0, 0), p2=(20000., 20000.))
        self.assertEqual(len(y_values), 2000001)
        self.assertEqual(y_values[200000], 2000.)

# ---------------------------------------------------------------------------


class TestGeometryDistances(unittest.TestCase):

    def test_distances(self):
        x = (1.0, 0.0)
        y = (0.0, 1.0)

        # Euclidian
        self.assertEqual(round(euclidian(x, y), 3), 1.414)
        with self.assertRaises(VectorsError):
            z = (1.0, 0.0, 1.0)
            euclidian(x, z)

        # Squared Euclidian
        self.assertEqual(squared_euclidian(x, y), 2.)
        with self.assertRaises(VectorsError):
            z = (1.0, 0.0, 1.0)
            squared_euclidian(x, z)

        # Manathan
        self.assertEqual(manathan(x, y), 2.)
        with self.assertRaises(VectorsError):
            z = (1.0, 0.0, 1.0)
            manathan(x, z)

        # Minkowski
        self.assertEqual(round(minkowski(x, y), 3), 1.414)
        with self.assertRaises(VectorsError):
            z = (1.0, 0.0, 1.0)
            minkowski(x, z)

        # Chi-squared
        self.assertEqual(round(chi_squared(x, y), 3), 1.414)
        with self.assertRaises(VectorsError):
            z = (1.0, 0.0, 1.0)
            chi_squared(x, z)

        # Euclidian vs Minkowski
        x, y = random_vectors(50000)
        start = time.time()
        e = euclidian(x, y)
        end = time.time()
        duration_euclidian = (end - start)
        start = time.time()
        m = minkowski(x, y)
        end = time.time()
        duration_minkowski = end - start
        self.assertEqual(e, m)
        # self.assertGreaterEqual(duration_minkowski, duration_euclidian)
