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
# File: viewsutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx

from sppas.src.ui.wxgui.sp_consts import FRAME_TITLE
from sppas.src.ui.wxgui.sp_icons  import APP_ICON
from sppas.src.ui.wxgui.cutils.imageutils import spBitmap

# ----------------------------------------------------------------------------


class spFrame( wx.Frame ):
    """
    Simple Frame.
    """

    def __init__(self, parent, title, preferences, btype=None, size=(640,480)):
        """
        Create a new sppasFrame.
        """
        # Create the frame and set properties
        wx.Frame.__init__(self, parent, -1, FRAME_TITLE, size=size)
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)

        # Create the main panel and the main sizer
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create the SPPAS specific header at the top of the panel
        spHeaderPanel(btype, title, parent.preferences).Draw(self.panel, self.sizer)

        self.panel.SetSizer(self.sizer)
        self.Centre()

# ----------------------------------------------------------------------------


class spHeaderPanel():
    """
    Create a panel with a specific header containing a bitmap and a 'nice'
    colored title.
    """

    def __init__(self, bmptype, label, preferences):
        if preferences:
            self.bmp = spBitmap(bmptype, 32, theme=preferences.get_theme())
        else:
            self.bmp = spBitmap(bmptype, 32, theme=None)
        self.label = label
        self.preferences = preferences


    def Draw(self, panel, sizer):
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        icon = wx.StaticBitmap(panel, bitmap=self.bmp)
        titlesizer.Add(icon, flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        text1 = wx.StaticText(panel, label=self.label)
        text1.SetFont(wx.Font(self.preferences.GetValue('M_HEADER_FONTSIZE'), wx.SWISS, wx.NORMAL, wx.BOLD))
        if self.preferences:
            text1.SetForegroundColour(self.preferences.GetValue('M_FG_COLOUR'))
        titlesizer.Add(text1, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        sizer.Add(titlesizer, 0, flag=wx.EXPAND, border=5)

        line1 = wx.StaticLine(panel)
        sizer.Add(line1, flag=wx.EXPAND|wx.BOTTOM, border=10)

# ----------------------------------------------------------------------------
