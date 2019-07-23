#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              Automatic
#           \__   |__/  |__/  |___| \__             Annotation
#              \  |     |     |   |    \             of
#           ___/  |     |     |   | ___/              Speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2016  Brigitte Bigi
#
#                   This banner notice must not be removed
# ---------------------------------------------------------------------------
# Use of this software is governed by the GNU Public License, version 3.
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: colorutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import random
import wx

# ----------------------------------------------------------------------------


def PickRandomColour(v1,v2):
    """Return a random color."""

    c = [random.uniform(v1,v2) for _ in range(5)]
    random.shuffle(c)
    return wx.Colour(c[0],c[1],c[2])

#-------------------------------------------------------------------------

def ContrastiveColour(crColor):
    """Return a contrastive (ie lighten or darken) color."""

    byRed   = crColor.Red()
    byGreen = crColor.Green()
    byBlue  = crColor.Blue()

    if byRed+byGreen+byBlue < 191:
        return LightenColor(crColor, random.sample(range(15,30),1)[0])

    if byRed+byGreen+byBlue < 382:
        return LightenColor(crColor, random.sample(range(40,60),1)[0])

    if byRed+byGreen+byBlue < 510:
        return DarkenColor(crColor, random.sample(range(15,30),1)[0])

    return DarkenColor(crColor, random.sample(range(40,60),1)[0])

#-------------------------------------------------------------------------

def LightenColor(crColor, byIncreaseVal):
    """Lightens a colour."""

    byRed = crColor.Red()
    byGreen = crColor.Green()
    byBlue = crColor.Blue()

    byRed = (byRed + byIncreaseVal <= 255 and [byRed + byIncreaseVal] or [255])[0]
    byGreen = (byGreen + byIncreaseVal <= 255 and [byGreen + byIncreaseVal] or [255])[0]
    byBlue = (byBlue + byIncreaseVal <= 255 and [byBlue + byIncreaseVal] or [255])[0]

    return wx.Colour(byRed, byGreen, byBlue)

#-------------------------------------------------------------------------

def DarkenColor(crColor, byReduceVal):
    """Darkens a colour."""

    byRed   = crColor.Red()
    byGreen = crColor.Green()
    byBlue  = crColor.Blue()

    byRed   = (byRed >= byReduceVal and [byRed - byReduceVal] or [0])[0]
    byGreen = (byGreen >= byReduceVal and [byGreen - byReduceVal] or [0])[0]
    byBlue  = (byBlue >= byReduceVal and [byBlue - byReduceVal] or [0])[0]

    return wx.Colour(byRed, byGreen, byBlue)

