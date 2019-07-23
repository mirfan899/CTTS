#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
# ----------------------------------------------------------------------------
# File: clock.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

import wx
import time

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

MIN_W=40
MIN_H=10

STYLE=wx.NO_BORDER|wx.NO_FULL_REPAINT_ON_RESIZE

#-----------------------------------------------------------------------------


class CustomClock( wx.Window ):
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: Display a clock on the screen!
    """

    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize):

        wx.Window.__init__( self, parent, id, pos, size, STYLE )
        self.SetBackgroundStyle( wx.BG_STYLE_CUSTOM )
        self.SetDoubleBuffered( True )

        self._value        = 0 # time in milliseconds
        self._leftmargin   = 10
        self._rightmargin  = 10
        self._topmargin    = 1
        self._bottommargin = 1

        if size:
            self.__initialSize(size)

        # Bind the events related to our control
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_ERASE_BACKGROUND(self, lambda event: None)

    # End __init__
    # ------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Members
    #-------------------------------------------------------------------------

    def SetValue(self, v):
        """
        Set a new time value (in milliseconds) and display it.
        """
        self._value  = v
        self.Refresh()

    # End SetValue
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Style
    #-------------------------------------------------------------------------


    def SetLeftMargin(self, margin):
        """
        Fix left margin (in pixels).
        """
        self._leftmargin = margin

    # End SetLeftMargin
    #-------------------------------------------------------------------------


    def SetRightMargin(self, margin):
        """
        Fix right margin (in pixels).
        """
        self._rightmargin = margin

    # End SetRightMargin
    #-------------------------------------------------------------------------


    def SetTopMargin(self, margin):
        """
        Fix a top margin (in pixels).
        """
        self._topmargin = margin

    # End SetTopMargin
    #-------------------------------------------------------------------------


    def SetBottomMargin(self, margin):
        """
        Fix a bottom margin (in pixels).
        """
        self._bottommargin = margin

    # End SetBottomMargin
    #-------------------------------------------------------------------------


    def SetFontColour(self, color):
        """
        Set a new color.
        """
        self._FontColour = color

    # End SetFontColour
    #-------------------------------------------------------------------------


    def MoveWindow(self, pos, size):
        """
        Define a new position and/or size to display.

        @param pos (wx.Point)
        @param size (wx.Size)

        """

        (w,h) = size
        (x,y) = pos
        (ow,oh) = self.GetSize()
        (ox,oy) = self.GetPosition()

        if ow != w or oh != h:
            self.SetSize(size)
            self.Refresh()

        if ox != x or oy != y:
            self.SetPosition(pos)

    # End MoveWindow
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Painting
    #-------------------------------------------------------------------------


    def OnPaint(self, event):
        """
        Handles the wx.EVT_PAINT event for PointCtrl.
        """

        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    # OnPaint
    #-------------------------------------------------------------------------


    def Draw(self, dc):
        """
        Draw a clock in the middle of the panel.
        """

        if self._value is None:
            return

        width,height = self.GetClientSize()
        # Nothing to do, we still don't have dimensions!
        if not width or not height:
            return

        st = self._strfduration(self._value)

        # Background of the clock
        dc.SetPen( wx.Pen( self.GetBackgroundColour() ) )
        dc.SetBrush( wx.Brush( self.GetBackgroundColour() ) )
        dc.SetBackgroundMode( wx.SOLID )
        #dc.SetBackground( wx.Brush( self.GetBackgroundColour() ) )

        dc.SetFont(self.GetFont())
        dc.SetTextForeground( self.GetForegroundColour() )

        wmargins = self._leftmargin + self._rightmargin
        hmargins = self._topmargin + self._bottommargin
        self._optimize_fontsize(dc, st, width-wmargins, height-hmargins)

        dc.DrawText(st, self._x(dc, st, width-wmargins), self._y(dc, st, height-hmargins))

    # End Draw
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------------


    def _strfduration(self, t):
        """convert a duration in ms into a formatted string."""

        return time.strftime("%H:%M:%S", time.gmtime(t/1000)) + '.%03d' % (t%1000)

    # ------------------------------------------------------------------------


    def _optimize_fontsize(self, dc, text, maxwidth, maxheight):

        # Get real text size in pixels
        textwidth, textheight = dc.GetTextExtent(text)
        if not textwidth or not textheight:
            return

        # Find the maximum possible size
        coeff = min( (float(maxwidth)/float(textwidth)),(float(maxheight)/float(textheight)) )
        self.GetFont().SetPointSize( int(self.GetFont().GetPointSize() * coeff) )
        textwidth, textheight = dc.GetTextExtent(text)

        # Now, reduce text size if text is larger than the panel size!
        while textwidth >= maxwidth:
            newsize = int(self.GetFont().GetPointSize() / 1.1)
            self.GetFont().SetPointSize( newsize )
            dc.SetFont( self.GetFont() )
            textwidth, textheight = dc.GetTextExtent(text)

        while textheight >= maxheight:
            newsize = int(self.GetFont().GetPointSize() / 1.1)
            self.GetFont().SetPointSize( newsize )
            dc.SetFont( self.GetFont() )
            textwidth, textheight = dc.GetTextExtent(text)

    # ------------------------------------------------------------------------


    def _x(self, dc, text, maxwidth):
        fs = self.GetFont().GetPointSize()
        textwidth, textheight = dc.GetTextExtent(text)
        if textwidth > maxwidth: # to be sure...
            return maxwidth + 1
        return self._leftmargin + int((maxwidth - textwidth) / 2)

    # ------------------------------------------------------------------------


    def _y(self, dc, text, height):
        fs = self.GetFont().GetPointSize()
        textwidth, textheight = dc.GetTextExtent(text)
        if textheight > height: # to be sure...
            return height - 1
        return self._topmargin + int((height - textheight + 1) / 2)


    # ------------------------------------------------------------------------


    def __initialSize(self, size):
        """Initialize the size."""

        self.SetMinSize(wx.Size(MIN_W,MIN_H))
        if size:
            self.SetSize(size)

    # End __initialSize
    #-------------------------------------------------------------------------


# ----------------------------------------------------------------------------


class TestClock(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, -1, 'Clock test', size=(320,120))
        clock = CustomClock(frame, -1, size=(320,120), pos=(0,0))

        frame.Show(True)
        return True

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    app = TestClock(0)
    app.MainLoop()
