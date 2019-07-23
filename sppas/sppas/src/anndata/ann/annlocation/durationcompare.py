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

    anndata.annlocation.durationcompare.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from sppas.src.utils.datatype import sppasType
from sppas.src.structs.basecompare import sppasBaseCompare

from ...anndataexc import AnnDataTypeError

from .duration import sppasDuration

# ---------------------------------------------------------------------------


class sppasDurationCompare(sppasBaseCompare):
    """Comparison methods for sppasDuration.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    """

    def __init__(self):
        """Create a sppasDurationCompare instance."""
        super(sppasDurationCompare, self).__init__()

        self.methods['eq'] = sppasDurationCompare.eq
        self.methods['ne'] = sppasDurationCompare.ne
        self.methods['gt'] = sppasDurationCompare.gt
        self.methods['lt'] = sppasDurationCompare.lt
        self.methods['le'] = sppasDurationCompare.le
        self.methods['ge'] = sppasDurationCompare.ge

    # -----------------------------------------------------------------------

    @staticmethod
    def eq(duration, x):
        """Return True if duration is equal to x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or
                isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration == x

    # -----------------------------------------------------------------------

    @staticmethod
    def ne(duration, x):
        """Return True if duration is different to x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or
                isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration != x

    # -----------------------------------------------------------------------

    @staticmethod
    def gt(duration, x):
        """Return True if duration is greater than x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or
                isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration > x

    # -----------------------------------------------------------------------

    @staticmethod
    def lt(duration, x):
        """Return True if duration is lower than x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration < x

    # -----------------------------------------------------------------------

    @staticmethod
    def ge(duration, x):
        """Return True if duration is greater or equal than x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or
                isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration >= x

    # -----------------------------------------------------------------------

    @staticmethod
    def le(duration, x):
        """Return True if duration is lower or equal than x.

        :param duration: (sppasDuration)
        :param x: (int, float)
        :returns: (bool)

        """
        if isinstance(duration, sppasDuration) is False:
            raise AnnDataTypeError(duration, "sppasDuration")
        if (sppasType().is_number(x) or
                isinstance(x, sppasDuration)) is False:
            raise AnnDataTypeError(x, "int/float/sppasDuration")

        return duration <= x
