# coding=UTF8
# Copyright (C) 2014  Brigitte Bigi
#
# This file is part of DataEditor.
#
# DataEditor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DataEditor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DataEditor.  If not, see <http://www.gnu.org/licenses/>.
#

__docformat__ = "epytext"


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import logging
import wx

from sppas.src.ui.wxgui.cutils.colorutils import PickRandomColour

from .spControl import spControl

#----------------------------------------------------------------------------
# Class WavePreferences
#----------------------------------------------------------------------------


class WavePreferences:
    """
    Manage preferences of a ChannelCtrl.
    """

    def __init__(self):
        """
        Create a new WavePreferences instance with default values.
        """
        self._gradientbg = True   # draw a gradient background
        self._autocolor  = False  # set random pen color
        self._autoadjust = True   # automatic vertical scroll


    #------------------------------------------------------------------------
    # Setters
    #------------------------------------------------------------------------


    def SetGradientBackground(self, value):
        """
        Activate/Disable gradient background.

        @param value (Boolean)
        """

        if self._gradientbg != value:
            self._gradientbg = value

    # End SetBackgroundGradient
    #------------------------------------------------------------------------


    def SetRandomForeground(self, value):
        """
        Activate/Disable the random foreground color.

        @param value (Boolean)
        """
        self._autocolor = value

    # End SetRandomForeground
    #------------------------------------------------------------------------


    def SetAutomaticScroll(self, value):
        """
        Activate/Disable the automatic vertical scroll.

        @param value (Boolean)
        """
        self._autoadjust = value

    # End SetAutomaticScroll
    #------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Getters
    #------------------------------------------------------------------------

    def GetRandomForeground(self):
        return self._autocolor

    def GetAutomaticScroll(self):
        return self._autoadjust

    def GetGradientBackground(self):
        return self._gradientbg

    #------------------------------------------------------------------------

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Class ChannelCtrl
# ---------------------------------------------------------------------------


class ChannelCtrl( spControl ):
    """
    ChannelCtrl implements a channel of a wave window that can be placed
    anywhere to any wxPython widget.

    @author: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: This class is used to display one channel of a wave file.

    """

    def __init__(self, parent, id=-1,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 datamax=0):
        """
        Constructor.

        Non-wxPython related parameter:
          - datamax: the maximum value of the amplitude.
        """

        spControl.__init__(self, parent, id, pos, size)

        self.isselectable = False

        self._preferences = WavePreferences()
        self._datamax     = datamax
        self._wavedata    = []

        self._bggradientcolor = wx.Colour(180,190,180)

        # temporary
        self._bgcolor    = wx.WHITE
        self._bgpen      = wx.Pen(self._bgcolor, 1, wx.SOLID)
        self._bgbrush    = wx.Brush(self._bgcolor, wx.SOLID)

        self._fgcolor    = wx.Colour(10,60,10)
        self._fgpen      = wx.Pen(self._fgcolor, 1, wx.SOLID)
        self._fgbrush    = wx.Brush(self._fgcolor, wx.SOLID)

        self._handlescolor = wx.Colour(10,140,10)
        self._handlespen   = wx.Pen(self._handlescolor, 1, wx.SOLID)
        self._handlesbrush = wx.Brush(self._handlescolor, wx.SOLID)

        # disable margins (then handles)
        self._margins.Left  = 0
        self._margins.Right = 0

    # End __init__
    #------------------------------------------------------------------------


    #------------------------------------------------------------------------
    # Members: Getters and Setters
    #------------------------------------------------------------------------


    def SetDataMax(self, value):
        """
        Set a new data max value (int), used for the vertical scroll.
        """
        self._datamax = int(value)

    # End SetDataMax
    #------------------------------------------------------------------------


    def SetData(self, data, mintime, maxtime):
        """
        Set values of the ampliture.

        @param data (list) is the list of amplitude values
        @param mintime (float) is the 'from' time value in seconds
        @param maxtime (float) is the 'to' time value in seconds

        """
        self._wavedata = data
        self.SetTime(mintime,maxtime)

    # End SetData
    # -----------------------------------------------------------------------


    def SetPreferences(self, p):
        self._preferences.SetGradientBackground( p.GetGradientBackground() )
        self._preferences.SetRandomForeground( p.GetRandomForeground() )
        self._preferences.SetAutomaticScroll( p.GetAutomaticScroll() )

    # End SetPreferences
    #------------------------------------------------------------------------


    def SetBackgroundGradientColour(self, color):
        """
        Set the background gradient color (used if gradient-background is turned-on).
        """
        if color != self._bggradientcolor:
            self._bggradientcolor = color
            self.RequestRedraw()

    # End SetBackgroundGradientColour
    #------------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Drawing the Channel on a DC
    # -----------------------------------------------------------------------


    def DrawBackground(self, dc, x, y, w, h):
        """
        Draw a filled gradient background.

        @param dc (PaintDC, MemoryDC, BufferedDC...)
        @param x,y (int,int) are coord. of top left corner from which drawing
        @param w,h (int,int) are width and height available for drawing.

        """

        logging.debug(' Draw Background GRADIENT: %s'%self._preferences.GetGradientBackground())
        #dc.SetBrush( self._bgbrush )
        box_rect = wx.Rect(x, y, w, h)
        if self._preferences.GetGradientBackground() is True:
            dc.GradientFillLinear(box_rect, self._bgcolor, self._bggradientcolor, wx.SOUTH)

    # End DrawBackground
    # -----------------------------------------------------------------------


    def DrawPane(self, dc, x,y, w,h):
        """
        Draw a pane with max/min/centre values of the amplitude.

        Known Bug: Works only with a LEFT-PANE

        @param dc (PaintDC, MemoryDC, BufferedDC...)
        @param x,y (int,int) are coord. of top left corner from which drawing
        @param w,h (int,int) are width and height available for drawing.

        """
        if len(self._wavedata) == 0:
            return

        dc.SetFont( self._font )

        # Draw the background
        #dc.SetPen( self._fgpen )
        #dc.SetBrush( self._bgbrush )
        #box_rect = wx.Rect(x, y, w, h)
        #dc.DrawRectangleRect(box_rect)

        # Draw the scale values
        if self._preferences.GetAutomaticScroll() is True:
            # Get min and max (take care if saturation...)
            # autoscroll is limited to at least 10%
            datamax = max(max(self._wavedata)+1, (self._datamax*0.1))
            datamin = min(min(self._wavedata)-1, -(self._datamax*0.1))
            mintext = str( round(float(datamin)/float(self._datamax), 3))
            maxtext = str( round(float(datamax)/float(self._datamax), 3))
        else:
            mintext = "-1"
            maxtext = "1"
        midtext = "0"

        # min: bottom
        textwidth, textheight = dc.GetTextExtent( mintext )
        if self._infopanep == wx.ALIGN_LEFT:
            min_x = x + w - textwidth - 1  # right
        else:
            min_x = x + 1
        min_y = y + h - textheight - 1  # left

        # max: top, right
        textwidth, textheight = dc.GetTextExtent( maxtext )
        if self._infopanep == wx.ALIGN_LEFT:
            max_x = x + w - textwidth - 1
        else:
            max_x = x + 1
        max_y = y

        # mid: centre
        textwidth, textheight = dc.GetTextExtent( midtext )
        if self._infopanep == wx.ALIGN_LEFT:
            mid_x = x + w - textwidth - 1
        else:
            mid_x = x + 1
        mid_y = y + (h/2) - (textheight/2)

        dc.SetPen( self._textpen )
        dc.DrawText(mintext, min_x, min_y)
        dc.DrawText(maxtext, max_x, max_y)
        dc.DrawText(midtext, mid_x, mid_y)

    # End DrawPane
    #-------------------------------------------------------------------------


    def DrawContent(self, dc, x, y, w, h):
        """
        Draw the amplitude of a channel of a wave on the DC.

        @param dc (PaintDC, MemoryDC, BufferedDC...)
        @param x,y (int,int) are coord. of top left corner from which drawing
        @param w,h (int,int) are width and height available for drawing.

        """
        if len(self._wavedata) == 0:
            return

        # Nothing to do, we still don't have dimensions!
        if not w or not h: return

        self.DrawBackground(dc, x, y, w, h)

        localdatamax = self._datamax
        localdatamin = -self._datamax
        if self._preferences.GetAutomaticScroll() is True:
            # autoscroll is limited to at least 10%
            localdatamax = max(max(self._wavedata)+1, (self._datamax*0.1))
            localdatamin = min(min(self._wavedata)-1, -(self._datamax*0.1))

        ycenter = y + int(h/2)
        ypixelsminprec = ycenter
        xprec = x
        xcur  = x
        xstep = 1
        d = 0
        incd = int(len(self._wavedata) / (w/xstep))

        while xcur < (x+w):

            # Get data of n frames (data of xsteps pixels of time) -- width
            dnext = min((d+incd), len(self._wavedata))
            data = self._wavedata[d:dnext]

            # Get min and max (take care if saturation...)
            datamin = max( min(data), localdatamin+1)
            datamax = min( max(data), localdatamax-1)

            # convert the data into a "number of pixels" -- height
            ypixelsmax = int( float(datamax) * (float(h)/2.0) / float(localdatamax))
            ypixelsmin = int( float(datamin) * (float(h)/2.0) / float(abs(localdatamin)))

            # Fix the pen style and color
            if self._preferences.GetRandomForeground() is False:
                dc.SetPen( self._fgpen )
            else:
                # Disco style. Each line is of a different color!
                color = PickRandomColour(50,210)
                dc.SetPen( wx.Pen(color, 1, wx.SOLID))

            # draw a line between prec. value to current value
            dc.DrawLine(xprec, ycenter-ypixelsminprec, xcur, ycenter-ypixelsmax)
            dc.DrawLine(xcur,  ycenter-ypixelsmin, xcur, ycenter-ypixelsmax)

            ypixelsminprec = ypixelsmin

            # set values for next step
            xprec = xcur
            xcur  = xcur + xstep
            d = dnext

    # End DrawContent
    #-------------------------------------------------------------------------

#-----------------------------------------------------------------------------
