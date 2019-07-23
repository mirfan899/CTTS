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
# File: choosers.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2016  Brigitte Bigi"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx

from sppas.src.ui.wxgui.cutils.textutils import TextAsNumericValidator
from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.sp_icons import INFO_ICON

# ----------------------------------------------------------------------------


class PeriodChooser(spBaseDialog):
    """
    Show a dialog to choose a new period (start/end values).

    """
    def __init__(self, parent, preferences, start, end):
        """

        """
        spBaseDialog.__init__(self, parent, preferences, title=" - Chooser")
        wx.GetApp().SetAppName( "perioddlg" )

        self.start = start
        self.end   = end

        titlebox   = self.CreateTitle(INFO_ICON,"Choose a period:")
        contentbox = self._create_content()
        buttonbox  = self._create_buttons()

        self.SetMinSize((300, 120))
        self.LayoutComponents( titlebox,
                               contentbox,
                               buttonbox )

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_cancel = self.CreateCancelButton()
        btn_okay   = self.CreateOkayButton()
        self.SetAffirmativeId(wx.ID_OK)
        return self.CreateButtonBox( [btn_cancel],[btn_okay] )

    def _create_content(self):
        # create the main sizer.
        font = self.preferences.GetValue('M_FONT')
        gbs = wx.GridBagSizer(hgap=5, vgap=5)

        txtfrom = wx.StaticText(self, label=" From: ", size=(80, 24))
        txtfrom.SetFont( font )
        txtto   = wx.StaticText(self, label=" To:   ", size=(80, 24))
        txtto.SetFont( font )

        self.fieldfrom = wx.TextCtrl(self, -1, str(self.start), size=(150, 24), validator=TextAsNumericValidator())
        self.fieldfrom.SetFont(font)
        self.fieldfrom.SetInsertionPoint(0)
        self.fieldto   = wx.TextCtrl(self, -1, str(self.end),  size=(150, 24), validator=TextAsNumericValidator())
        self.fieldto.SetFont(font)
        self.fieldto.SetInsertionPoint(0)

        gbs.Add(txtfrom,       (0,0), flag=wx.ALL,    border=2)
        gbs.Add(self.fieldfrom,(0,1), flag=wx.EXPAND, border=2)
        gbs.Add(txtto,         (1,0), flag=wx.ALL,    border=2)
        gbs.Add(self.fieldto,  (1,1), flag=wx.EXPAND, border=2)

        gbs.AddGrowableCol(1)

        border = wx.BoxSizer()
        border.Add(gbs, 1, wx.ALL | wx.EXPAND, 10)
        return border

    # -------------------------------------------------------------------------

    def GetValues(self):
        """
        Return the new from/to values.

        """
        return self.fieldfrom.GetValue(), self.fieldto.GetValue()

# ----------------------------------------------------------------------------


class RadiusChooser( wx.Dialog ):
    """
    Show a dialog to choose a new radius value.

    """
    def __init__(self, parent, preferences, radius):
        wx.Dialog.__init__(self, parent, title="Radius", size=(320, 150), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

        self.SetBackgroundColour( preferences.GetValue("M_BG_COLOUR") )
        self.SetForegroundColour( preferences.GetValue("M_FG_COLOUR") )
        font = preferences.GetValue("M_FONT")
        self.SetFont(font)

        self.preferences = preferences
        self.radius = radius

        # create the main sizer.
        gbs = wx.GridBagSizer(hgap=5, vgap=5)

        txtinfo = wx.StaticText(self, label="Fix the vagueness of each boundary.")
        txtinfo.SetFont( font )

        txtradius = wx.StaticText(self, label="  Value: ", size=(80, 24))
        txtradius.SetFont( font )

        self.field = wx.TextCtrl(self, -1, str(self.radius), size=(150, 24), validator=TextAsNumericValidator())
        self.field.SetFont(font)
        self.field.SetInsertionPoint(0)

        gbs.Add(txtinfo,    (0,0), (1,2), flag=wx.ALL, border=2)
        gbs.Add(txtradius,  (1,0), flag=wx.ALL, border=2)
        gbs.Add(self.field, (1,1), flag=wx.EXPAND, border=2)

        # the buttons for close, and cancellation
        Buttons = wx.StdDialogButtonSizer()
        ButtonClose = wx.Button(self, wx.ID_OK)
        Buttons.AddButton(ButtonClose)
        ButtonCancel = wx.Button(self, wx.ID_CANCEL)
        Buttons.AddButton(ButtonCancel)
        Buttons.Realize()
        gbs.Add(Buttons, (2,0), (1,2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.SetMinSize((300, 120))
        self.SetSizer(gbs)
        self.Layout()
        self.Refresh()

    # -------------------------------------------------------------------------

    def GetValue(self):
        """Return the new radius value."""

        return self.field.GetValue()

# ----------------------------------------------------------------------------
