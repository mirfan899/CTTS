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
# File: feedback.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2016  Brigitte Bigi"""

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

import wx
import urllib
import webbrowser

from sppas.src.config import sg

from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.dialogs.msgdialogs import ShowInformation

from sppas.src.ui.wxgui.sp_icons import FEEDBACK_ICON
from sppas.src.ui.wxgui.sp_icons import MAIL_DEFAULT_ICON
from sppas.src.ui.wxgui.sp_icons import MAIL_GMAIL_ICON
from sppas.src.ui.wxgui.sp_icons import MAIL_OTHER_ICON

# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------

DESCRIBE_TEXT = "Describe what you did here..."

# -------------------------------------------------------------------------

class FeedbackForm(object):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL
    @summary: This class is used to send feedback to the author.

    """
    def __init__(self, dialog, webbrowser):
        self.dialog = dialog
        self.webbrowser = webbrowser

    def Populate(self, subject=None, body=None):
        self.dialog.SetToText(sg.__contact__)
        if subject: self.dialog.SetSubjectText(subject)
        if body: self.dialog.SetBodyText(body)
        if body and body.startswith(DESCRIBE_TEXT):
            self.dialog.SetBodySelection(0, len(DESCRIBE_TEXT))

    def SendWithDefault(self):
        text = self.dialog.GetBodyText()
        text = text.strip()
        self.webbrowser.open("mailto:%s?subject=%s&body=%s" % (
            urllib.quote(self.dialog.GetToText()),
            urllib.quote(self.dialog.GetSubjectText()),
            urllib.quote(text.encode('utf-8'))))

    def SendWithGmail(self):
        self.webbrowser.open("https://mail.google.com/mail/?compose=1&view=cm&fs=1&to=%s&su=%s&body=%s" % (
            urllib.quote(self.dialog.GetToText()),
            urllib.quote(self.dialog.GetSubjectText()),
            urllib.quote(self.dialog.GetBodyText())))

    def SendWithOther(self):
        ShowInformation( self.dialog,
                         self.dialog.preferences,
                         "Copy and paste this email into your favorite email "
                         "client and send it from there.")

# ----------------------------------------------------------------------------

class FeedbackDialog( spBaseDialog ):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL
    @summary: Dialog to send feedback comments by email to the author.

    """
    def __init__(self, parent, preferences):
        spBaseDialog.__init__(self, parent, preferences, title="Feedback")
        wx.GetApp().SetAppName( "feedback" )

        self.controller = FeedbackForm(self, webbrowser)

        titlebox   = self.CreateTitle(FEEDBACK_ICON,"Email Feedback")
        contentbox = self._create_content()
        buttonbox  = self._create_buttons()

        self.LayoutComponents( titlebox,
                               contentbox,
                               buttonbox )

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        self.btn_default = self.CreateButton(MAIL_DEFAULT_ICON, " Default ", "Send with your default email client.")
        self.btn_gmail = self.CreateButton(MAIL_GMAIL_ICON,   " Gmail ",   "Send with Gmail.")
        self.btn_other = self.CreateButton(MAIL_OTHER_ICON,   " Other ",   "Send with another email client.")
        btn_close = self.CreateCloseButton()
        self.Bind(wx.EVT_BUTTON, self._on_send, self.btn_default)
        self.Bind(wx.EVT_BUTTON, self._on_send, self.btn_other)
        self.Bind(wx.EVT_BUTTON, self._on_send, self.btn_gmail)
        return self.CreateButtonBox( [self.btn_default,self.btn_gmail,self.btn_other], [btn_close])

    def _create_content(self):
        self.to_text = self.CreateTextCtrl("", style=wx.TE_READONLY)
        self.subject_text = self.CreateTextCtrl(sg.__name__ +
                                                " " +
                                                sg.__version__ +
                                                " - Feedback...",
                                                style=wx.TE_READONLY)
        self.body_text = self.CreateTextCtrl(DESCRIBE_TEXT, style=wx.TE_MULTILINE)
        self.body_text.SetMinSize((300,200))
        self.body_text.SetForegroundColour(wx.Colour(128, 128, 128))
        self.body_text.Bind(wx.EVT_CHAR, self._on_char)

        grid = wx.FlexGridSizer(4, 2, 5, 5)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(2)
        grid.Add(wx.StaticText(self, label="To: "), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.to_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Subject: "), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.subject_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Body: "), flag=wx.TOP)
        grid.Add(self.body_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Send with: "), flag=wx.ALIGN_CENTER_VERTICAL)

        return grid

    # ------------------------------------------------------------------------
    # Callback to events
    # ------------------------------------------------------------------------

    def _on_char(self, evt):
        if self.body_text.GetValue().strip() == DESCRIBE_TEXT:
            self.body_text.SetForegroundColour( self.preferences.GetValue('M_FG_COLOUR') )
            self.body_text.SetValue('')
        if self._ctrl_a(evt):
            self.body_text.SelectAll()
        else:
            evt.Skip()

    def _ctrl_a(self, evt):
        KEY_CODE_A = 1
        return evt.ControlDown() and evt.KeyCode == KEY_CODE_A

    def _on_send(self, event):
        idb = event.GetId()
        if idb == self.btn_default.GetId():
            self.controller.SendWithDefault()
        elif idb == self.btn_gmail.GetId():
            self.controller.SendWithGmail()
        elif idb == self.btn_other.GetId():
            self.controller.SendWithOther()
        else:
            event.Skip()

    # ------------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------------

    def GetToText(self):
        return self.to_text.GetValue()

    def GetSubjectText(self):
        return self.subject_text.GetValue()

    def GetBodyText(self):
        return self.body_text.GetValue()

    def SetToText(self, text):
        self.to_text.SetValue(text)

    def SetSubjectText(self, text):
        if text: self.subject_text.SetValue(text)

    def SetBodyText(self, text):
        if text: self.body_text.SetValue(text)

    def SetBodySelection(self, start, end):
        self.body_text.SetSelection(start, end)

# ----------------------------------------------------------------------------

def ShowFeedbackDialog(parent, preferences=None):
    dialog = FeedbackDialog(parent, preferences)
    dialog.controller.Populate(None, None)
    dialog.ShowModal()
    dialog.Destroy()

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = wx.PySimpleApp()
    ShowFeedbackDialog(None,None)
    app.MainLoop()

# ---------------------------------------------------------------------------
