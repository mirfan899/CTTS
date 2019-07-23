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

    src.calculus.stats.variability.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

A collection of basic statistical functions for python.

"""

import math

from .central import fmean
from .central import fsum

# ----------------------------------------------------------------------------


def lunbiasedvariance(items):
    """Calculate the unbiased sample variance of the data values, for a sample.

    It means that the estimation is using N-1 for the denominator.
    The variance is a measure of dispersion near the mean.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.
    mn = fmean(items)

    return fsum(pow(i-mn, 2) for i in items) / (len(items)-1)

# ----------------------------------------------------------------------------


def lvariance(items):
    """Calculate the variance of the data values, for a population.

    It means that the estimation is using N for the denominator.
    The variance is a measure of dispersion near the mean.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.
    mn = fmean(items)

    return fsum(pow(i-mn, 2) for i in items) / (len(items))

# ----------------------------------------------------------------------------


def lunbiasedstdev(items):
    """Calculate the standard deviation of the data values, for a sample.

    The standard deviation is the positive square root of the variance.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.

    return math.sqrt(lunbiasedvariance(items))

# ----------------------------------------------------------------------------


def lstdev(items):
    """Calculate the standard deviation of the data values, for a population.

    The standard deviation is the positive square root of the variance.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.

    return math.sqrt(lvariance(items))

# ----------------------------------------------------------------------------


def lsterr(items):
    """Calculate the standard error of the data values.

    :param items: (list) list of data values
    :returns: (float)

    """
    return lstdev(items) / float(math.sqrt(len(items)))

# ----------------------------------------------------------------------------


def lz(items, score):
    """Calculate the z-score for a given input score.

    given that score and the data values from which that score came.

    The z-score determines the relative location of a data value.

    :param items: (list) list of data values
    :param score: (float) a score of any items
    :returns: (float)

    """
    if len(items) < 2:
        return 0.

    return (score - fmean(items)) / lstdev(items)

# ----------------------------------------------------------------------------


def lzs(items):
    """Calculate a list of z-scores, one for each score in the data values.

    :param items: (list) list of data values
    :returns: (list)

    """
    return [lz(items, i) for i in items]

# ----------------------------------------------------------------------------


def rPVI(items):
    """Calculate the Raw Pairwise Variability Index.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.
    n = len(items) - 1
    sumd = fsum([math.fabs(items[i]-items[i+1]) for i in range(n)])

    return sumd / n

# ----------------------------------------------------------------------------


def nPVI(items):
    """Calculate the Normalized Pairwise Variability Index.

    :param items: (list) list of data values
    :returns: (float)

    """
    if len(items) < 2:
        return 0.
    n = len(items) - 1
    sumd = 0.
    for i in range(n):
        d1 = items[i]
        d2 = items[i+1]
        delta = math.fabs(d1 - d2)
        meand = (d1 + d2) / 2.
        sumd += delta / meand

    return 100. * sumd / n
