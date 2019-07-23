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
# File: audioinfo.py
# ----------------------------------------------------------------------------

import wx
import logging

import sppas.src.audiodata.aio

from sppas.src.ui.wxgui.sp_consts import ERROR_COLOUR
from sppas.src.ui.wxgui.sp_consts import INFO_COLOUR
from sppas.src.ui.wxgui.sp_consts import WARNING_COLOUR
from sppas.src.ui.wxgui.sp_consts import OK_COLOUR

from sppas.src.ui.wxgui.sp_consts import MIN_PANEL_W
from sppas.src.ui.wxgui.sp_consts import MIN_PANEL_H

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LABEL_LIST = [ "Audio file name: ",
               "Duration (seconds): ",
               "Frame rate (Hz): ",
               "Sample width (bits): ",
               "Channels: " ]

NO_INFO_LABEL = " ... "

# ---------------------------------------------------------------------------

class AudioInfo( wx.Panel ):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      develop@sppas.org
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      Display general information about an audio file.

    Information has a different color depending on the level of acceptability
    in SPPAS.

    """
    def __init__(self, parent, preferences):
        """
        Create a new AudioInfo instance.

        @parent (wxWindow)

        """
        wx.Panel.__init__(self, parent)

        self._prefs = preferences
        self._labels = []
        self._values = []

        gbs = self._create_content()

        self.SetFont( self._prefs.GetValue('M_FONT') )
        self.SetBackgroundColour( self._prefs.GetValue('M_BG_COLOUR') )
        self.SetForegroundColour( self._prefs.GetValue('M_FG_COLOUR') )

        self.SetSizer(gbs)
        self.SetAutoLayout( True )
        self.SetMinSize((MIN_PANEL_W,MIN_PANEL_H))
        self.Layout()

    # -----------------------------------------------------------------------
    # Private methods to create the GUI and initialize members
    # -----------------------------------------------------------------------

    def _create_content(self):
        """
        GUI design.

        """
        gbs = wx.GridBagSizer(len(LABEL_LIST), 2)

        for i,label in enumerate(LABEL_LIST):
            static_tx = wx.StaticText(self, -1, label)
            self._labels.append( static_tx )
            gbs.Add(static_tx, (i,0), flag=wx.ALL, border=2)

            tx = wx.TextCtrl(self, -1, NO_INFO_LABEL, style=wx.TE_READONLY)
            self._values.append( tx )
            gbs.Add(tx, (i,1), flag=wx.EXPAND|wx.RIGHT, border=2)

        gbs.AddGrowableCol(1)
        return gbs

    # -----------------------------------------------------------------------
    # GUI
    # -----------------------------------------------------------------------

    def SetPreferences(self, prefs):
        """
        Set new preferences.

        """
        self._prefs = prefs
        self.SetBackgroundColour( self._prefs.GetValue("M_BG_COLOUR") )
        self.SetForegroundColour( self._prefs.GetValue("M_FG_COLOUR") )
        self.SetFont( self._prefs.GetValue("M_FONT") )

    #-------------------------------------------------------------------------

    def SetFont(self, font):
        """
        Change font of all wx texts.

        """
        wx.Window.SetFont( self,font )

        for p in self._values:
            p.SetFont( font )
        for l in self._labels:
            l.SetFont( font )
        self.Refresh()

    # -----------------------------------------------------------------------

    def SetBackgroundColour(self, colour):
        """
        Change the background color of all wx objects.

        """
        wx.Window.SetBackgroundColour( self,colour )

        for p in self._values:
            p.SetBackgroundColour( colour )
        for l in self._labels:
            l.SetBackgroundColour( colour )
        self.Refresh()

    # -----------------------------------------------------------------------

    def SetForegroundColour(self, colour):
        """
        Change the foreground color of all wx objects.

        """
        wx.Window.SetForegroundColour( self,colour )

        for l in self._labels:
            l.SetForegroundColour( colour )
        self.Refresh()

    # -----------------------------------------------------------------------

    def fix_filename(self, filename):
        self._values[0].ChangeValue( filename )
        self._values[0].SetForegroundColour( INFO_COLOUR )

    def fix_duration(self, duration):
        self._values[1].ChangeValue( str(round(float(duration), 3) ))
        self._values[1].SetForegroundColour( INFO_COLOUR )

    def fix_framerate(self, framerate):
        self._values[2].ChangeValue( str(framerate) )
        if framerate < 16000:
            self._values[2].SetForegroundColour( ERROR_COLOUR )
        elif framerate in [16000, 32000, 48000]:
            self._values[2].SetForegroundColour( OK_COLOUR )
        else:
            self._values[2].SetForegroundColour( WARNING_COLOUR )

    def fix_sampwidth(self, sampwidth):
        self._values[3].ChangeValue( str(sampwidth*8) )
        if sampwidth == 1:
            self._values[3].SetForegroundColour( ERROR_COLOUR )
        elif sampwidth == 2:
            self._values[3].SetForegroundColour( OK_COLOUR )
        else:
            self._values[3].SetForegroundColour( WARNING_COLOUR )

    def fix_nchannels(self, nchannels):
        self._values[4].ChangeValue( str(nchannels) )
        if nchannels == 1:
            self._values[4].SetForegroundColour( OK_COLOUR )
        else:
            self._values[4].SetForegroundColour( ERROR_COLOUR )

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def FileSelected(self, filename):
        """
        Show information of a sound file.

        """
        self.fix_filename(filename)
        try:
            _audio = sppas.src.audiodata.aio.open( filename )
            self.fix_duration(  _audio.get_duration())
            self.fix_framerate( _audio.get_framerate())
            self.fix_sampwidth( _audio.get_sampwidth())
            self.fix_nchannels( _audio.get_nchannels())
            _audio.close()
        except Exception as e:
            logging.info(" ... Error reading %s: %s" % (filename,e))
            for i in range(1, len(self._values)):
                self._values[i].ChangeValue( NO_INFO_LABEL )
                self._values[i].SetForegroundColour( self._prefs.GetValue('M_FG_COLOUR') )

    #------------------------------------------------------------------------

    def FileDeSelected(self):
        """
        Reset information.

        """
        for v in self._values:
            v.ChangeValue( NO_INFO_LABEL )
            v.SetForegroundColour( self._prefs.GetValue('M_FG_COLOUR') )
