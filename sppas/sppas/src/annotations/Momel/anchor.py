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

    src.annotations.Momel.anchor.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class Anchor(object):
    """Data structure to store a selected anchor.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    An anchor was initially called a "target". Daniel Hirst changed the name
    in 2017.

    An anchor is made of 2 or 3 values:
        - x: float : the number of the frame ; required
        - y: float ; the pitch value ; required
        - p: int   ; optional

    """

    def __init__(self):
        """Create a new Anchor instance with default values."""
        self.__x = 0.
        self.__y = 0.
        self.__p = 0

    # ------------------------------------------------------------------

    def set(self, x, y, p=0):
        """Set new values to an anchor.

        :param x: (float)
        :param y: (float)
        :param p: (int)

        """
        self.set_x(x)
        self.set_y(y)
        self.set_p(p)

    # ------------------------------------------------------------------

    def get_x(self):
        """Return the x value of an anchor."""
        return self.__x

    # ------------------------------------------------------------------

    def set_x(self, x):
        """Set a new x value to an anchor.

        :param x: (float)
        :raises: TypeError

        """
        self.__x = float(x)

    # ------------------------------------------------------------------

    def get_y(self):
        """Return the y value of an anchor."""
        return self.__y

    # ------------------------------------------------------------------

    def set_y(self, y):
        """Set a new y value to an anchor.

        :param y: (float)
        :raises: TypeError

        """
        self.__y = float(y)

    # ------------------------------------------------------------------

    def get_p(self):
        """Return the p value of an anchor."""
        return self.__p

    # ------------------------------------------------------------------

    def set_p(self, p):
        """Set a new p value to an anchor.

        :param p: (int)
        :raises: TypeError

        """
        self.__p = int(p)

    # ------------------------------------------------------------------

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    p = property(get_p, set_p)

    # ------------------------------------------------------------------
    # overload
    # ------------------------------------------------------------------

    def __str__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ")"
