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

    anndata.annloc.duration.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from ...anndataexc import AnnDataTypeError
from ...anndataexc import AnnDataNegValueError

# ---------------------------------------------------------------------------


class sppasDuration(object):
    """Representation of a duration with vagueness.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi

    Represents a duration identified by 2 float values:

        - the duration value;
        - the duration margin.

    """

    def __init__(self, value, vagueness=0.):
        """Create a new sppasDuration instance.

        :param value: (float) value of the duration.
        :param vagueness: (float) represents the vagueness of the value.

        """
        self.__value = 0.
        self.__margin = 0.

        self.set_value(value)
        self.set_margin(vagueness)

    # -----------------------------------------------------------------------

    def get(self):
        """Return myself."""
        return self

    # -----------------------------------------------------------------------

    def set(self, other):
        """Set the value/vagueness of another sppasDuration instance.

        :param other: (sppasDuration)

        """
        if isinstance(other, sppasDuration) is False:
            raise AnnDataTypeError(other, "sppasDuration")

        self.__value = other.get_value()
        self.__margin = other.get_margin()

    # -----------------------------------------------------------------------

    def get_value(self):
        """Return the duration value (float)."""
        return self.__value

    # -----------------------------------------------------------------------

    def set_value(self, value):
        """Set the duration to a new value.

        :param value: (float) the new duration value.

        """
        try:
            self.__value = float(value)
            if self.__value < 0.:
                self.__value = 0.
                raise AnnDataNegValueError(value)
        except TypeError:
            raise AnnDataTypeError(value, "float")

    # -----------------------------------------------------------------------

    def get_margin(self):
        """Return the vagueness of the duration (float)."""
        return self.__margin

    # -----------------------------------------------------------------------

    def set_margin(self, vagueness):
        """Fix the vagueness margin of the duration.

        :param vagueness: (float) the duration margin.

        """
        try:
            self.__margin = float(vagueness)
            if self.__margin < 0.:
                self.__margin = 0.
                raise AnnDataNegValueError(vagueness)
        except TypeError:
            raise AnnDataTypeError(vagueness, "float")

    # -----------------------------------------------------------------------

    def copy(self):
        """Return a deep copy of self."""
        t = self.__value
        r = self.__margin
        return sppasDuration(t, r)

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __format__(self, fmt):
        return str(self).__format__(fmt)

    # -----------------------------------------------------------------------

    def __repr__(self):
        return "Duration: {:f}, {:f}" \
               "".format(self.get_value(), self.get_margin())

    # -----------------------------------------------------------------------

    def __str__(self):
        return "({:f}, {:f})".format(self.get_value(), self.get_margin())

    # -----------------------------------------------------------------------

    def __hash__(self):
        return hash((self.__value, self.__margin))

    # -----------------------------------------------------------------------

    def __eq__(self, other):
        """Equal is required to use '==' between 2 sppasDuration instances or
        between a sppasDuration and an other object representing time.
        This relationship takes into account the vagueness.

        :param other: (Duration, float, int) is the other duration to compare with.

        """
        if isinstance(other, (int, float, sppasDuration)) is False:
            return False

        if isinstance(other, sppasDuration) is True:
            delta = abs(self.__value - other.get_value())
            radius = self.__margin + other.get_margin()
            return delta <= radius

        if isinstance(other, (int, float)):
            delta = abs(self.__value - other)
            radius = self.__margin
            return delta <= radius

    # -----------------------------------------------------------------------

    def __lt__(self, other):
        """LowerThan is required to use '<' between 2 sppasDuration instances
        or between a sppasDuration and an other time object.

        :param other: (Duration, float, int) is the other duration to compare with.

        """
        if isinstance(other, sppasDuration) is True:
            return self != other and self.__value < other.get_value()

        return (self != other) and (self.__value < other)

    # -----------------------------------------------------------------------

    def __gt__(self, other):
        """GreaterThan is required to use '>' between 2 Duration instances
        or between a Duration and an other time object.

        :param other: (Duration, float, int) is the other duration to compare with.

        """
        if isinstance(other, sppasDuration) is True:
            return self != other and self.__value > other.get_value()

        return (self != other) and (self.__value > other)

    # ------------------------------------------------------------------------

    def __ne__(self, other):
        """Not equals."""

        return not (self == other)

    # ------------------------------------------------------------------------

    def __le__(self, other):
        """Lesser or equal."""

        return (self < other) or (self == other)

    # ------------------------------------------------------------------------

    def __ge__(self, other):
        """Greater or equal."""

        return (self > other) or (self == other)
