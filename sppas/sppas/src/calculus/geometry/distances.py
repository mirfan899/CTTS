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

    src.calculus.geometry.distances.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

A collection of basic distance functions for python.
Distance axioms:
    - d(x,y) = 0 iff x = y
    - d(x,y) = d(y,x)
    - d(x,z) <= d(x,y) + d(y,z)

"""

from ..calculusexc import VectorsError

# ---------------------------------------------------------------------------


def manathan(x, y):
    """Estimate the Manathan distance between two tuples.

    :param x: a tuple of float values
    :param y: a tuple of float values
    :returns: (float)

    x and y must have the same length.

    >>> x = (1.0, 0.0)
    >>> y = (0.0, 1.0)
    >>> manathan(x, y)
    >>> 2.0

    """
    if len(x) != len(y):
        raise VectorsError

    return sum([abs(a-b) for (a, b) in zip(x, y)])

# ---------------------------------------------------------------------------


def euclidian(x, y):
    """Estimate the Euclidian distance between two tuples.

    :param x: a tuple of float values
    :param y: a tuple of float values
    :returns: (float)

    x and y must have the same length.

    >>> x = (1.0, 0.0)
    >>> y = (0.0, 1.0)
    >>> round(euclidian(x, y), 3)
    >>> 1.414

    """
    if len(x) != len(y):
        raise VectorsError

    return pow(squared_euclidian(x, y), 0.5)

# ---------------------------------------------------------------------------


def squared_euclidian(x, y):
    """Estimate the Squared Euclidian distance between two tuples.

    :param x: a tuple of float values
    :param y: a tuple of float values
    :returns: (float)

    x and y must have the same length.

    >>> x = (1.0, 0.0)
    >>> y = (0.0, 1.0)
    >>> squared_euclidian(x, y)
    >>> 2.0

    """
    if len(x) != len(y):
        raise VectorsError

    return sum([(a-b)**2 for (a, b) in zip(x, y)])

# ---------------------------------------------------------------------------


def minkowski(x, y, p=2):
    """Estimate the Minkowski distance between two tuples.

    :param x: a tuple of float values
    :param y: a tuple of float values
    :param p: power value (p=2 corresponds to the euclidian distance)
    :returns: (float)

    x and y must have the same length.

    >>> x = (1.0, 0.0)
    >>> y = (0.0, 1.0)
    >>> round(minkowski(x, y), 3)
    >>> 1.414

    """
    if len(x) != len(y):
        raise VectorsError

    summ = 0.
    for (a, b) in zip(x, y):
        summ += pow((a-b), p)

    return pow(summ, 1./p)

# ---------------------------------------------------------------------------


def chi_squared(x, y):
    """Estimate the Chi-squared distance between two tuples.

    :param x: a tuple of float values
    :param y: a tuple of float values
    :returns: (float)

    x and y must have the same length.

    >>> x = (1.0, 0.0)
    >>> y = (0.0, 1.0)
    >>> round(chi_squared(x, y), 3)
    >>> 1.414

    """
    if len(x) != len(y):
        raise VectorsError

    summ = 0.
    for (a, b) in zip(x, y):
        summ += (float((a-b)**2) / float((a+b)))

    return pow(summ, 0.5)
