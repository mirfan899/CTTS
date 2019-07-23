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

    src.calculus.stats.moment.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

A collection of basic statistical functions for python.

"""

from .central import fmean
from .variability import lstdev

# ----------------------------------------------------------------------------


def lmoment(items, moment=1):
    """Calculate the r-th moment about the mean for a sample.

    1/n * SUM((items(i)-mean)**r)

    :param items: (list) list of data values
    :param moment:
    :returns: (float)

    """
    if moment == 1:
        return 0.
    mn = fmean(items)
    momentlist = [(i-mn)**moment for i in items]

    return sum(momentlist) / float(len(items))

# ---------------------------------------------------------------------------


def lvariation(items):
    """Calculate the coefficient of variation of data values.

    It shows the extent of variability in relation to the mean. It's a
    standardized measure of dispersion: stdev / mean and returned as a
    percentage.

    :param items: (list) list of data values
    :returns: (float)

    """
    return lstdev(items) / float(fmean(items)) * 100.

# ---------------------------------------------------------------------------


def lskew(items):
    """Calculate the skewness of a distribution.

    The skewness represents a measure of the asymmetry: an understanding
    of the skewness of the dataset indicates whether deviations from the
    mean are going to be positive or negative.

    :param items: (list) list of data values
    :returns: (float)

    """
    return lmoment(items, 3) / pow(lmoment(items, 2), 1.5)

# ---------------------------------------------------------------------------


def lkurtosis(items):
    """Return the kurtosis of a distribution.

    The kurtosis represents a measure of the "peakedness": a high kurtosis
    distribution has a sharper peak and fatter tails, while a low kurtosis
    distribution has a more rounded peak and thinner tails.

    :param items: (list) list of data values
    :returns: (float)

    """
    return lmoment(items, 4) / pow(lmoment(items, 2), 2.0)
