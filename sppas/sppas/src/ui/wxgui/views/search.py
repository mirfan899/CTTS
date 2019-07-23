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
#                   Copyright (C) 2011-2018  Brigitte Bigi
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
# File: search.py
# ----------------------------------------------------------------------------

import sys
import os.path
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import wx
import wx.lib.newevent as newevent

from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.cutils.imageutils  import spBitmap
from sppas.src.ui.wxgui.cutils.textutils   import TextValidator

from sppas.src.ui.wxgui.sp_icons import TIER_SEARCH
from sppas.src.ui.wxgui.sp_icons import BROOM_ICON
from sppas.src.ui.wxgui.sp_icons import BACKWARD_ICON
from sppas.src.ui.wxgui.sp_icons import FORWARD_ICON
from sppas.src.ui.wxgui.sp_icons import CLOSE_ICON

# ----------------------------------------------------------------------------

DEFAULT_LABEL = 'label1, label2, etc'

SearchedEvent, spEVT_SEARCHED = newevent.NewEvent()
SearchedCommandEvent, spEVT_SEARCHED_COMMAND = newevent.NewCommandEvent()

# ----------------------------------------------------------------------------


class SearchDialog(spBaseDialog):
    """
    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL, v3
    :summary: This class is used to display a Search dialog.

    Open a frame to search patterns in a transcription.

    """
    def __init__(self, parent, preferences, trs):
        """Constructor.

        :param parent: is the parent wx object.
        :param preferences: (Preferences)
        :param trs: (Transcription)

        """
        spBaseDialog.__init__(self, parent, preferences, title=" - Search")
        wx.GetApp().SetAppName("search")

        # Members
        self._trs = trs
        self._pmin = 0.
        self._pmax = 0.

        titlebox = self.CreateTitle(TIER_SEARCH,"Search patterns in a tier")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                              contentbox,
                              buttonbox)

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_next = self.CreateButton(FORWARD_ICON,
                                     " Search forward",
                                     "Search after the current position.")
        btn_previous = self.CreateButton(BACKWARD_ICON,
                                         " Search backward",
                                         "Search before the current position.")
        btn_close = self.CreateButton(CLOSE_ICON,
                                      " Close")
        btn_close.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnFind, btn_next, wx.ID_FORWARD)
        self.Bind(wx.EVT_BUTTON, self.OnFind, btn_previous, wx.ID_BACKWARD)
        self.Bind(wx.EVT_BUTTON, self._on_close, btn_close)
        return self.CreateButtonBox([btn_previous, btn_next], [btn_close])

    # ------------------------------------------------------------------------

    def _create_content(self):
        label = wx.StaticText(self, label="Search for:", pos=wx.DefaultPosition, size=wx.DefaultSize)
        label.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))
        label.SetForegroundColour(self.preferences.GetValue('M_FG_COLOUR'))

        self.text = wx.TextCtrl(self, size=(150, -1), validator=TextValidator())
        self.text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text.SetForegroundColour(wx.Colour(128, 128, 128))
        self.text.SetValue(DEFAULT_LABEL)
        self.text.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.text.Bind(wx.EVT_SET_FOCUS, self.OnTextClick)

        self.broom = wx.BitmapButton(self, bitmap=spBitmap(BROOM_ICON, 16, theme=self.preferences.GetValue('M_ICON_THEME')), style=wx.NO_BORDER)
        self.broom.Bind(wx.EVT_BUTTON, self.OnTextErase)

        self.pattern_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.pattern_layout.Add(label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.pattern_layout.Add(self.text, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        self.pattern_layout.Add(self.broom, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.tp = TierPanel(self, self._trs)
        self.lp = LabelPanel(self)
        self.sh_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.sh_layout.Add(self.lp, 1, wx.EXPAND | wx.LEFT,  0)
        self.sh_layout.Add(self.tp, 2, wx.EXPAND | wx.RIGHT, 0)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.pattern_layout, 0, wx.EXPAND|wx.ALL, border=5)
        vbox.Add(self.sh_layout,
                 1,
                 flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
                 border=5)

        return vbox

    # ------------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------------

    def _on_close(self,event):
        self.Destroy()

    # -----------------------------------------------------------------------

    def OnTextClick(self, event):
        self.text.SetForegroundColour(wx.BLACK)
        if self.text.GetValue() == DEFAULT_LABEL:
            self.OnTextErase(event)
        event.Skip()
        #self.text.SetFocus()

    # -----------------------------------------------------------------------

    def OnTextChanged(self, event):
        self.text.SetFocus()
        self.text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text.Refresh()

    # -----------------------------------------------------------------------

    def OnTextErase(self, event):
        self.text.SetValue('')
        self.text.SetFocus()
        self.text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text.Refresh()

    # -----------------------------------------------------------------------
#
#     def SetPeriod(self, pmin, pmax):
#         self._pmin = pmin
#         self._pmax = pmax

    # -----------------------------------------------------------------------

    def OnFind(self, event):
        """
        Search after or before the current position.

        """
        # Firstly, check if a text to find is given!
        success = self.text.GetValidator().Validate(self.text)
        if success is False:
            return

        ruler = self.GetParent()._display.GetRuler()
        self._pmin = ruler.GetSelectionIndicatorMinValue()
        self._pmax = ruler.GetSelectionIndicatorMaxValue()

        # Get search criteria
        criteria = self.lp.GetCriteria()
        patterns = self.text.GetValue().split(',')

        # Get search direction
        forward = True
        direction = 1
        if event.GetId() == wx.ID_BACKWARD:
            forward = False
            direction = -1

        # Convert criteria into "functions"
        function = criteria['function']
        if criteria['case_sensitive'] is False and function != "regexp":
            function = "i"+function

        # Search... On which tier?
        tieridx  = self.tp.GetSelection()
        tier = self._trs[tieridx]
        if forward is True:
            annidx = tier.Near(self._pmax, direction)
        else:
            annidx = tier.Near(self._pmin, direction)

        # Now, can search the next/previous occurrence
        #logging.debug(' Search %s in %s with function %s in forward direction=%d'%(patterns,tier.GetName(),function,forward))
        annidx = tier.Search(patterns,function,annidx,forward,criteria['reverse'])

        # Show the search result
        if annidx == -1:
            self.text.SetForegroundColour(wx.RED)
            #self.text.SetFocus()
            self.text.Refresh()
            #logging.debug(' ... no occurrence. ')
        else:
            self.text.SetForegroundColour(wx.BLACK)
            ann = tier[annidx]
            #logging.debug(' ... success: %s '%ann)
            if ann.GetLocation().IsPoint():
                radius = ann.GetLocation().GetPointRadius()
                s = ann.GetLocation().GetPointMidpoint() - radius
                e = ann.GetLocation().GetPointMidpoint() + radius
            else:
                s = ann.GetLocation().GetBeginMidpoint()
                e = ann.GetLocation().GetEndMidpoint()
                evt = SearchedEvent(start=s, end=e)
                evt.SetEventObject(self)
                wx.PostEvent(self.GetParent(), evt)

    # -----------------------------------------------------------------------
    # Getters and Setters
    # -----------------------------------------------------------------------

    def SetTranscription(self, trs):
        """
        Set a new transcription.

        """
        if trs != self._trs:
            self._trs = trs
            self.sh.Remove(1)
            self.tp.Destroy()

            self.tp = TierPanel(self, self._trs)
            self.sh.Add(self.tp, 0, wx.ALL | wx.EXPAND, 5)

            self.Layout()
            self.Refresh()

# ---------------------------------------------------------------------------


class LabelPanel(wx.Panel):
    """A panel with the search modes."""

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #self.SetBackgroundColour(FRAME_BG_COLOR)

        self.modes = (
                   ("exact", "exact"),
                   ("not exact", "exact"),
                   ("contains", "contains"),
                   ("not contains", "contains"),
                   ("starts with", "startswith"),
                   ("not starts with", "startswith"),
                   ("ends with", "endswith"),
                   ("not ends with", "endswith"),
                   ("match (regexp)", "regexp"),
                   ("not match", "regexp")
                  )

        choices = []
        for choice in self.modes:
            choices.append(choice[0])

        self.radiobox = wx.RadioBox(self, label="Search mode:",
                                    choices=choices, majorDimension=2)
        self.radiobox.SetForegroundColour(wx.Colour(3, 3, 87))

        self.checkbox = wx.CheckBox(self, label="Case Sensitive")
        self.checkbox.SetValue(True)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.radiobox, 1, wx.EXPAND|wx.ALL, border=2)
        vbox.Add(self.checkbox, 0, wx.EXPAND|wx.ALL, border=2)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        self.Layout()

    def GetCriteria(self):
        criteria = {}
        idx = self.radiobox.GetSelection()
        criteria['name'] = self.modes[idx][0]
        criteria['function'] = self.modes[idx][1]
        criteria['case_sensitive'] = self.checkbox.GetValue()
        criteria['reverse'] = idx % 2 != 0
        return criteria

# ---------------------------------------------------------------------------


class TierPanel(wx.Panel):
    """A panel with the radiolist of tiers of the given transcription."""

    def __init__(self, parent, trs):

        wx.Panel.__init__(self, parent)

        choices = []
        if trs:
            for t in trs:
                choices.append(t.get_name())
        else:
            choices.append('Empty transcription')

        self.radiobox = wx.RadioBox(self, label="Tier:",
                                    choices=choices,
                                    majorDimension=1)
        self.radiobox.SetForegroundColour(wx.Colour(87, 3, 3))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.radiobox, 1, wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        self.Layout()

    def GetSelection(self):
        return self.radiobox.GetSelection()

# ---------------------------------------------------------------------------


def ShowSearchDialog(parent, preferences, trs):
    dialog = SearchDialog(parent, preferences, trs)
    dialog.ShowModal()
    dialog.Destroy()

# ---------------------------------------------------------------------------


if __name__ == "__main__":
    app = wx.PySimpleApp()
    ShowSearchDialog(None,  None, None)
    app.MainLoop()
