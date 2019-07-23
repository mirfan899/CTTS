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
# File: textutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx

# ----------------------------------------------------------------------------


class BasicTextValidator(wx.PyValidator):
    """Check if the TextCtrl contains characters."""

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self): # Required method for validator
        return BasicTextValidator()

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        textCtrl.Refresh()
        return True



class TextValidator(wx.PyValidator):
    """Check if the TextCtrl contains characters."""

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self): # Required method for validator
        return TextValidator()

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        if not len(text):
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True


#----------------------------------------------------------------------------


class TextAsNumericValidator(wx.PyValidator):
    """Check if the TextCtrl contains a numeric value."""

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self): # Required method for validator
        return TextAsNumericValidator()

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

    def Validate(self, win):
        success = True
        textCtrl = self.GetWindow()
        try:
            text = float(textCtrl.GetValue())
        except Exception:
            success = False

        if len(textCtrl.GetValue().strip()) == 0 or success is False:
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            success = False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()

        return success


#-----------------------------------------------------------------------------


class TextAsPercentageValidator(wx.PyValidator):
    """Check if the TextCtrl a percentage value."""

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self): # Required method for validator
        return TextAsNumericValidator()

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

    def Validate(self, win):
        success = True
        textCtrl = self.GetWindow()
        try:
            text = float(textCtrl.GetValue())
            if text < 0. or text > 100.:
                success = False
        except Exception:
            success = False

        if len(textCtrl.GetValue().strip()) == 0 or success is False:
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            success = False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
        return success

#-----------------------------------------------------------------------------
