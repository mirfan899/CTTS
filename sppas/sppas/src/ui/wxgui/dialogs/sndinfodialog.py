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
# File: sndinfodialog.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2016  Brigitte Bigi"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx

from sppas.src.ui.wxgui.panels.audioinfo   import AudioInfo
from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog

from sppas.src.ui.wxgui.sp_icons import INFO_ICON

# ----------------------------------------------------------------------------


class AudioInfoDialog( spBaseDialog ):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL
    @summary: Open a dialog with information about a sound file.

    """
    def __init__(self, parent, preferences, sndname):
        spBaseDialog.__init__(self, parent, preferences, title=" - Information")
        wx.GetApp().SetAppName( "audioinfodlg" )

        titlebox   = self.CreateTitle(INFO_ICON,"Audio description")
        contentbox = self._create_content(sndname)
        buttonbox  = self._create_buttons()

        self.LayoutComponents( titlebox,
                               contentbox,
                               buttonbox )

        self.SetMinSize((480,220))

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_close  = self.CreateCloseButton()
        return self.CreateButtonBox( [],[btn_close] )

    def _create_content(self, sndname):
        # the information panel
        self.trspanel = AudioInfo( self, self.preferences )
        self.trspanel.FileSelected( sndname )
        return self.trspanel

# ------------------------------------------------------------------------------

def ShowAudioInfo(parent, preferences, sndname):
    dlg = AudioInfoDialog( parent, preferences, sndname )
    return dlg.ShowModal()
