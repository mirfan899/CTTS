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
# File: wavectrl.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

import math
import logging

import wx

from .spControl import spControl
from .channelctrl import ChannelCtrl, WavePreferences

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SELECTION_BRUSH_COLOUR = wx.Colour(180,200,230,128)
SELECTION_PEN_COLOUR   = wx.Colour(30,70,110)

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Class SelectArea
# ---------------------------------------------------------------------------

class SelectArea:
    """
    @author: Brigitte Bigi
    @contact: contact@sppas.org
    @license: GPL
    @summary: This class is used to select an area on a displayed speech file.

    SelectArea holds information about a selected part in WaveCtrl.
    Start value and End value are related to the user selection
    (this means that start can be greater than end).

    """

    def __init__(self):
        """Constructor."""

        # Wave... is focused?
        self._isselected = False

        # mouse selection start point
        self._pos1 = 0
        # mouse selection end point
        self._pos2 = 0

    # End __init__
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Getters
    # -----------------------------------------------------------------------

    def IsSelected(self):
        return self._isselected

    def IsEmpty(self):
        return (self._pos1 == 0 and self._pos2 == 0)


    # -----------------------------------------------------------------------
    # Setters
    # -----------------------------------------------------------------------

    def Select(self, value):
        self._isselected = value

    def SetArea(self, xstart, xend):
        self._pos1 = xstart
        self._pos2 = xend

    def SetStart(self, xstart):
        self._pos1 = xstart

    def SetEnd(self, xend):
        self._pos2 = xend

    def SetEmpty(self):
        self._pos1 = 0
        self._pos2 = 0


    # -----------------------------------------------------------------------
    # Getters
    # -----------------------------------------------------------------------

    def GetStart(self):
        return self._pos1

    def GetEnd(self):
        return self._pos2

    # -----------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Class WaveCtrl
# ---------------------------------------------------------------------------

#TODO: Rename to AudioCtrl, thanks to Nicolas!
class WaveCtrl( spControl ):
    """
    WaveCtrl implements an audio window that can be placed anywhere
    to any wxPython widget.

    @author: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: This class is used to display an audio speech file.

    """

    def __init__(self, parent, id=-1,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 audio=None):
        """
        Constructor.

        Non-wxPython related parameter:
          - audio (sppasAudioPCM): the audio instance.

        """
        spControl.__init__(self, parent, id, pos, size)

        # Preferences
        self._preferences = WavePreferences()

        # Disable Pane (because each channel has its own pane)
        self._infopanep = wx.ALIGN_CENTRE

        # Members
        self._selectarea = SelectArea()
        self._m_dragging = False

        # Wave
        self.__set( audio )

        # Handling mouse moving.
        wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvents)

    # End __init__
    #------------------------------------------------------------------------


    def __set(self, audio):

        self._audio = audio
        self._channels = []

        if audio is None:
            return

        # find the maximum amplitude value
        datamax = int(math.pow(2, (8*self._audio.get_sampwidth())) / 2) - 1

        # estimate the exact height of each channel
        (x,y) = (0,0)
        (w,h) = self.GetSize()
        cheight = self._getChannelHeight(h)

        for i in range( self._audio.get_nchannels() ):
            pos  = wx.Point( x,y )
            size = wx.Size( w,cheight )
            c =  ChannelCtrl(self, -1, pos, size, datamax)
            self._channels.append( c )
            y = y + cheight

    #------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Members: Getters and Setters
    #------------------------------------------------------------------------


    def SetDataMax(self, value):
        """
        Set a new data max value, used for the vertical scroll.

        @param value (int)
        """
        for i in range( self._audio.get_nchannels() ):
            self._channels.SetDataMax( value )

    # End SetDataMax
    #------------------------------------------------------------------------

    # TODO: Rename as SetAudio
    def SetWave(self, audio):
        """
        Set a new Wave.
        """
        self.__set(audio)

    # End SetWave
    #------------------------------------------------------------------------


    def get_duration(self):
        """
        Return the duration of the Wave, in seconds, or 0 if no Wave.
        """
        if self._audio is None:
            return 0.0

        return float(self._audio.get_nframes())/float(self._audio.get_framerate())

    # End get_duration
    #------------------------------------------------------------------------


    def GetBegin(self):
        """Override."""
        return 0.0

    # End GetBegin
    #------------------------------------------------------------------------


    def GetEnd(self):
        """Override."""
        return self.get_duration()

    # End GetEnd
    #------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Preferences
    #------------------------------------------------------------------------


    def SetAutoAdjust(self, value):
        """
        Set auto-ajustment vertical scroll.

        @param value (Boolean) is True to active, False to disable.
        """
        if value != self._preferences.SetAutomaticScroll( value ):
            self._preferences.SetAutomaticScroll( value )
            self.RequestRedraw()

    # End SetAutoAdjust
    #------------------------------------------------------------------------


    def SetAutoColor(self, value):
        """
        Activate/Disable the random foreground color, used to draw the amplitude lines.

        @param value (Boolean) is True to active, False to disable.

        """
        if value != self._preferences.SetRandomForeground( value ):
            self._preferences.SetRandomForeground( value )
            self.RequestRedraw()

    # End SetAutoColor
    #------------------------------------------------------------------------


    def SetGradientBackground(self, value):
        """
        Activate/Disable gradient background.

        @param value (Boolean) is True to active, False to disable.

        """
        if value != self._preferences.SetGradientBackground( value ):
            self._preferences.SetGradientBackground( value )
            self.RequestRedraw()

    # End SetBackgroundGradient
    #------------------------------------------------------------------------


    def SetBackgroundGradientColour(self, color):
        """
        Set the background gradient color (used if gradient-background is turned-on).
        """
        for c in self._channels:
            c.SetBackgroundGradientColour( color )

    # End SetBackgroundGradientColour
    #------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # WaveCtrl look
    #------------------------------------------------------------------------


    def SetBackgroundColour(self, colour):
        """
        Override. Sets the WaveCtrl background color.
        Ask to redraw only if color has changed.

        @param colour (wx.Colour)

        """

        spControl.SetBackgroundColour( self,colour )
        for c in self._channels:
            c.SetBackgroundColour( colour )

    # End SetBackgroundColour
    #-------------------------------------------------------------------------


    def SetForegroundColour(self, colour):
        """
        Sets the WaveCtrl foreground color.
        Ask to redraw only if color has changed.

        @param colour (wx.Colour)

        """

        spControl.SetForegroundColour( self,colour )
        for c in self._channels:
            c.SetForegroundColour( colour )

    # End SetForegroundColour
    #-------------------------------------------------------------------------


    def SetHandlesColour(self, colour):
        """
        Sets the WaveCtrl handles color.
        Ask to redraw only if color has changed.

        @param colour (wx.Colour)

        """
        spControl.SetHandlesColour( self,colour )
        for c in self._channels:
            c.SetHandlesColour( colour )

    # End SetHandlesColour
    #-------------------------------------------------------------------------


    def SetTextColour(self, colour):
        """
        Sets the WaveCtrl text color.
        Ask to redraw only if color has changed.

        @param colour (wx.Colour)

        """

        spControl.SetTextColour( self,colour )
        for c in self._channels:
            c.SetTextColour( colour )

    # End SetTextColour
    #-------------------------------------------------------------------------


    def SetFont(self, font):
        """
        Sets the WaveCtrl text font.
        Ask to redraw only if color has changed.

        @param font (wx.Font)

        """

        spControl.SetFont( self,font )
        for c in self._channels:
            c.SetFont( font )

    # End SetFont
    #-------------------------------------------------------------------------



    #------------------------------------------------------------------------
    # WaveCtrl display
    #------------------------------------------------------------------------


    def SetPanePosition(self, value):
        """
        Override. Fix the position of the information pane for channels.

        @param value is one of wx.ALIGN_LEFT, wx.ALIGN_CENTRE or wx.ALIGN_RIGHT.

        """
        for tdc in self._channels:
            tdc.SetPanePosition( value )
        self.RequestRedraw()

    # End SetPanePosition
    #-------------------------------------------------------------------------


    def SetPaneWidth(self, value):
        """
        Override. Fix the width of the information pane.

        @param value (int) is between 10 and 200.

        """
        spControl.SetPaneWidth(self, value)
        for tdc in self._channels:
            tdc.SetPaneWidth( value )

    # End SetPaneWidth
    #-------------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------


    def OnMouseEvents(self, event):
        """Handles the wx.EVT_MOUSE_EVENTS event for WaveCtrl."""

        if event.Moving():
            wx.PostEvent(self.GetParent().GetEventHandler(), event)

        elif event.LeftDown():
            self.OnMouseLeftDown(event)

        elif event.LeftUp():
            spControl.OnMouseLeftUp(self,event)
            self.OnMouseLeftUp(event)

        elif event.Dragging():
            # moving while a button is pressed
            self.OnMouseDragging(event)

        event.Skip()

    # End OnMouseEvents
    #-------------------------------------------------------------------------


    def OnMouseLeftDown(self, event):
        """
        Respond to mouse events.
        """

        self._m_dragging = False
        self.ResetMouseSelection()

        if self._selectarea.IsSelected() is True:
            # Left mouse button down, change cursor to
            # something else to denote event capture
            sx,sy = event.GetPosition()
            self._selectarea.SetStart(sx)
            self._selectarea.SetEnd(sx)
            cur = wx.StockCursor(wx.CURSOR_SIZING)
            self.SetCursor(cur)
            # invalidate current canvas
            self.RequestRedraw()
            # cache current position
            self._m_dragging = True

    # End onMouseLeftDown
    #-------------------------------------------------------------------------


    def OnMouseLeftUp(self,event):
        """
        Override. Respond to mouse events.
        """
        spControl.OnMouseLeftUp(self, event)

        if self._m_dragging is True:
            self._m_dragging = False
            sx,sy = event.GetPosition()
            self._selectarea.SetEnd(sx)
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            # send such info to the parent!
            wx.PostEvent(self.GetParent().GetEventHandler(), wx.PyCommandEvent(wx.EVT_TOOL_RANGE.typeId, self.GetId()))

        self.RequestRedraw()

    # End onMouseLeftUp
    #-------------------------------------------------------------------------


    def OnMouseDragging(self, event):
        """
        Respond to mouse events.
        """
        if self._m_dragging is True:
            # Draw a selected area
            sx,sy = event.GetPosition()
            self._selectarea.SetEnd(sx)
            # Show changes
            self.RequestRedraw()

    # End onMouseDragging
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Selection area
    #-------------------------------------------------------------------------


    def GetCurrentMouseSelection(self):
        """
        Return the current selected area,
        as a tuple (left-x, right-x).
        """

        if self._selectarea.IsEmpty() is True:
            return (0,0)

        # user dragged mouse to right
        if self._selectarea.GetEnd() >= self._selectarea.GetStart():
            return self._selectarea.GetStart() , self._selectarea.GetEnd()

        # user dragged mouse to left
        return self._selectarea.GetEnd() , self._selectarea.GetStart()

    # GetCurrentMouseSelection
    #-------------------------------------------------------------------------


    def ResetMouseSelection(self):
        """Resets the mouse selection."""

        self._selectarea.SetEmpty()

    # ResetMouseSelection
    #-------------------------------------------------------------------------


    def SetMouseSelection(self, point1, point2):
        """
        Sets the mouse selection to a specific position.
        Only point.x will be used.
        """

        self._selectarea.GetStart(point1)
        self._selectarea.SetEnd(point2)

    # SetMouseSelection
    #-------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Drawing the amplitude
    #------------------------------------------------------------------------


    def DrawPane(self, dc, x,y, w,h):
        """Do not draw anything (each channel draw its own pane)."""
        return

    # End DrawPane
    # -----------------------------------------------------------------------


    def DrawContent(self, dc, x,y, w,h):
        """
        Draw each channel of the wav on the DC, in the range of the given time period.
        """
        logging.debug(' ******* audiocontrol.drawcontent. x=%d,y=%d,w=%d,h=%d'%(x,y,w,h))

        if self._audio is None:
            return

        # the period is not covering this audio file: do not draw anything
        if self._mintime > self.GetEnd():
            return

        # Normal case
        self._drawChannels(dc,x,y,w,h)

    # End DrawContent
    # -----------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Private...
    #------------------------------------------------------------------------


    def _getChannelHeight(self, h):
        seph  = 0 #self._sep.GetPenWidth()
        septh = seph * (self._audio.get_nchannels()-1)
        return int( (h-septh) / self._audio.get_nchannels() )


    def _drawChannels(self, dc, x, y, w, h):
        """
        Draw the audio on the DC, in the range of the given time period.
        """

        if self._audio is None or self._mintime > self.GetEnd():
            return

        # estimate the exact height of each channel
        cheight = self._getChannelHeight(h)

        # set current prefs and look to each channel
        for c in self._channels:
            c.SetPreferences( self._preferences )

        # draw the selected area
        (l,r) = self.GetCurrentMouseSelection()
        if (r-l)>2:
            self._drawMouseSelection(dc)

        # draw each channel amplitude

        # Position in the audio
        pos = int(self._mintime * self._audio.get_framerate())

        # Read samples
        duration = self._maxtime - self._mintime
        self._audio.seek( pos )
        nframes = int( duration * self._audio.get_framerate() )
        data = self._audio.read_samples( nframes )

        # draw each channel
        for i,c in enumerate(self._channels):
            ww = w
            # the period is overlaping this channel: draw partly
            if self._mintime < self.GetEnd() and self._maxtime > self.GetEnd():
                ## reduce w (to cover until the end of the tier)
                missing = self._maxtime - self.GetEnd()
                real_w = w - c.GetPaneWidth()
                ww = w - int ((missing * float(real_w) ) / (self._maxtime-self._mintime))

            c.MoveWindow( wx.Point(x,y), wx.Size(ww,cheight) )
            c.SetData(data[i], self._mintime, self._maxtime)
            y = y + cheight

        if y != h:
            self.SetSize(wx.Size(w,y))

    # End _drawWave
    #------------------------------------------------------------------------


    def _drawMouseSelection(self, dc):
        """
        Draw mouse selection area for this WaveCtrl.
        """

        dc.SetBrush(wx.Brush(SELECTION_BRUSH_COLOUR, wx.SOLID))
        dc.SetPen(wx.Pen(SELECTION_PEN_COLOUR, 1, wx.SOLID))

        (x,y) = self.GetDrawingPosition()
        (w,h) = self.GetSize()
        (l,r) = self.GetCurrentMouseSelection()
        x = x+l
        w = r-l

        dc.DrawRectangle(x, y, w, h)

    # End drawMouseSelection
    # -----------------------------------------------------------------------

#----------------------------------------------------------------------------
