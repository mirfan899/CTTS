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
# File: CustomStatus.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

import wx
import time

# -------------------------------------------------------------------------

REFRESH_TIMER = 2000

# -------------------------------------------------------------------------


class CustomStatusBar( wx.StatusBar ):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL, v3
    @summary: This class is used to manage a custom status bar.

    The customized status bar is made of 3 areas.
    In the SppasEdit component:
    - the left one is for general information,
    - the middle one is used to display time information,
    - the left one is used to indicate the position of the mouse.

    """
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # Status bar fields
        self.SetFieldsCount(3)

        # Sets the fields to be relative widths to each other.
        self.SetStatusWidths([-4, -2, -1])
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.SetStatusText("...", 0)
        # Field 1 ... just text
        self.SetStatusText(" ... ", 1)
        # Field 2 ... just text
        self.SetStatusText(" ... ", 2)

        # We're going to use a timer to drive a 'clock' in the first field.
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start( REFRESH_TIMER )
        self.Notify()

        # set the initial position
        self.Reposition()

    # End __init__
    # ------------------------------------------------------------------------


    def Notify(self):
        """
        Handles events from the timer we started in __init__().
        """
        t = time.localtime(time.time())
        st = time.strftime("%d-%b-%Y %I:%M:%S", t)
        try:
            st = st.decode('utf8')
        except Exception:
            pass
        try:
            self.SetStatusText(st, 0)
        except Exception:
            pass

    # End Notify
    # ------------------------------------------------------------------------


    def StartTime(self):
        """
        Start the timer.
        """
        self.timer.Start( REFRESH_TIMER )

    # End StartTime
    # ------------------------------------------------------------------------


    def StopTime(self):
        """
        Stop the timer.
        """
        self.timer.Stop()

    # End StopTime
    # ------------------------------------------------------------------------


    def Reposition(self):
        """
        Reposition the checkbox (if progress bar is used).
        """
        rect = self.GetFieldRect(0)
        rect.x += 1
        rect.y += 1
        self.sizeChanged = False

    # End Reposition
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------------


    def OnSize(self, evt):
        """
        Callback to EVT_SIZE event.
        """
        evt.Skip()
        self.Reposition() # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    # End OnSize
    # ------------------------------------------------------------------------


    def OnIdle(self, evt):
        """
        Callback to EVT_IDLE event.
        """
        if self.sizeChanged:
            self.Reposition()

    # End OnIdle
    # ------------------------------------------------------------------------

# ----------------------------------------------------------------------------
