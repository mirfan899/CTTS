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

    anndata.annloc.localization.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class sppasBaseLocalization(object):
    """Represents a base class for any kind of localization.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi

    """

    def __init__(self):
        """Create a sppasLocalization instance."""
        pass

    # -----------------------------------------------------------------------

    def get(self):
        """Return myself."""
        return self

    # -----------------------------------------------------------------------

    def set(self, other):
        """Set self members from another localization.

        :param other: (sppasBaseLocalization)

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def duration(self):
        """Return the duration of the localization.

        Must be overridden

        :returns: (sppasDuration) Duration and its vagueness.

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def copy(self):
        """Return a deep copy of self."""
        raise NotImplementedError

    # ---------------------------------------------------------------------

    def is_point(self):
        """Return True if this object is an instance of sppasPoint.

        Should be overridden.

        """
        return False

    # ---------------------------------------------------------------------

    def is_interval(self):
        """Return True if this object is an instance of sppasInterval.

        Should be overridden.

        """
        return False

    # ---------------------------------------------------------------------

    def is_disjoint(self):
        """Return True if this object is an instance of sppasDisjoint.

        Should be overridden.

        """
        return False

    # ---------------------------------------------------------------------

    def set_radius(self, radius):
        """Set radius value to all points."""
        raise NotImplementedError

    # ---------------------------------------------------------------------

    def shift(self, delay):
        """Shift all the points to a given delay.

        :param delay: (int, float) delay to shift points
        :raise: AnnDataTypeError

        """
        raise NotImplementedError

    # ---------------------------------------------------------------------
    # Overloads
    # ---------------------------------------------------------------------

    def __eq__(self, other):
        """Equal is required to use '==' between 2 localization instances.

        Two localization instances are equals iff they are of the same
        instance and their values are equals.

        :param other: the other localization to compare with.

        """
        raise NotImplementedError

    # ---------------------------------------------------------------------

    def __lt__(self, other):
        """LowerThan is required to use '<' between two loc instances.

        :param other: the other localization to compare with.

        """
        raise NotImplementedError

    # ---------------------------------------------------------------------

    def __gt__(self, other):
        """GreaterThan is required to use '>' between two loc instances.

        :param other: the other localization to compare with.

        """
        raise NotImplementedError

    # ---------------------------------------------------------------------

    def __ne__(self, other):
        return not self == other

    # ---------------------------------------------------------------------

    def __le__(self, other):
        return self < other or self == other

    # ---------------------------------------------------------------------

    def __ge__(self, other):
        return self > other or self == other
