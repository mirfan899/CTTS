#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /      |   \   |   \   |   \  /              Automatic
#           \__    | __/   | __/   | ___ |  \__             Annotation
#              \   |       |       |     |     \             of
#           ___/   |       |       |     |  ___/              Speech
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
# File: components.py
# ----------------------------------------------------------------------------

import wx

from sppas.src.ui.wxgui.sp_icons import AUDIOROAMER_APP_ICON
from sppas.src.ui.wxgui.sp_icons import DATAROAMER_APP_ICON
from sppas.src.ui.wxgui.sp_icons import IPUSCRIBE_APP_ICON
from sppas.src.ui.wxgui.sp_icons import SPPASEDIT_APP_ICON
from sppas.src.ui.wxgui.sp_icons import STATISTICS_APP_ICON
from sppas.src.ui.wxgui.sp_icons import DATAFILTER_APP_ICON

from sppas.src.ui.wxgui.panels.buttons import ButtonPanel

from sppas.src.ui.wxgui.sp_consts import ID_FRAME_DATAROAMER
from sppas.src.ui.wxgui.sp_consts import ID_FRAME_SNDROAMER
from sppas.src.ui.wxgui.sp_consts import ID_FRAME_IPUSCRIBE
from sppas.src.ui.wxgui.sp_consts import ID_FRAME_SPPASEDIT
from sppas.src.ui.wxgui.sp_consts import ID_FRAME_STATISTICS
from sppas.src.ui.wxgui.sp_consts import ID_FRAME_DATAFILTER

# ----------------------------------------------------------------------------


class AnalyzePanel(wx.Panel):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      develop@sppas.org
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    @summary:      Tools for analyzing annotated data.

    """
    def __init__(self, parent, preferences):
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.SetBackgroundColour(preferences.GetValue('M_BG_COLOUR'))
        self._prefs = preferences

        content = self.__create_buttons()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(content, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick)
        self.SetSizerAndFit(sizer)

    # -----------------------------------------------------------------------

    def __create_buttons(self):
        """Create buttons to call tools."""

        annotateButton = ButtonPanel(self, ID_FRAME_DATAROAMER, self._prefs, DATAROAMER_APP_ICON, "DataRoamer")
        analyzeButton = ButtonPanel(self, ID_FRAME_SNDROAMER, self._prefs, AUDIOROAMER_APP_ICON, "AudioRoamer")
        pluginsButton = ButtonPanel(self, ID_FRAME_IPUSCRIBE, self._prefs, IPUSCRIBE_APP_ICON, "IPUscriber")
        settingsButton = ButtonPanel(self, ID_FRAME_SPPASEDIT, self._prefs, SPPASEDIT_APP_ICON, "Visualizer")
        helpButton = ButtonPanel(self, ID_FRAME_DATAFILTER, self._prefs, DATAFILTER_APP_ICON, "DataFilter")
        aboutButton = ButtonPanel(self, ID_FRAME_STATISTICS, self._prefs, STATISTICS_APP_ICON, "DataStats")

        _box = wx.GridBagSizer()
        _box.Add(annotateButton, pos=(0, 0), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)
        _box.Add(pluginsButton,  pos=(1, 1), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)
        _box.Add(analyzeButton,  pos=(0, 1), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)
        _box.Add(settingsButton, pos=(1, 0), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)
        _box.Add(aboutButton,    pos=(2, 0), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)
        _box.Add(helpButton,     pos=(2, 1), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, border=2)

        _box.AddGrowableCol(0)
        _box.AddGrowableCol(1)
        _box.AddGrowableRow(0)
        _box.AddGrowableRow(1)
        _box.AddGrowableRow(2)

        return _box

    # -----------------------------------------------------------------------

    def OnButtonClick(self, evt):
        obj = evt.GetEventObject()
        evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, obj.GetId())
        evt.SetEventObject(self)
        wx.PostEvent(self.GetParent(), evt)
