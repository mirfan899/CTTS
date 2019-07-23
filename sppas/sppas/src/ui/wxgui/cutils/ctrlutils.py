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
# File: ctrlutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx
from wx.lib.buttons import GenBitmapButton, GenBitmapTextButton

# ----------------------------------------------------------------------------


def CreateButton(parent, bmp, handler, sizer, colour=None):
    """Create a bitmap button and bind the event."""

    btn = wx.BitmapButton(parent, -1, bmp, style=wx.NO_BORDER)
    if colour is not None:
        btn.SetBackgroundColour( colour )
    btn.SetInitialSize()
    btn.Bind(wx.EVT_BUTTON, handler)
    btn.Enable( True )

    return btn

# ----------------------------------------------------------------------------


def CreateGenButton(parent, id, bmp, text=None, tooltip=None, colour=None, font=None):
    """Create a bitmap button."""

    if text is None:
        button = GenBitmapButton(parent, id, bmp, style=wx.SIMPLE_BORDER)
    else:
        button = GenBitmapTextButton(parent, id, bmp, text, style=wx.SIMPLE_BORDER)
        if font:
            button.SetFont(font)

    if tooltip is not None:
        button.SetToolTipString(tooltip)
    if colour is not None:
        button.SetBackgroundColour(colour)

    button.SetBezelWidth(0)
    button.SetUseFocusIndicator(False)

    return button

# ----------------------------------------------------------------------------
