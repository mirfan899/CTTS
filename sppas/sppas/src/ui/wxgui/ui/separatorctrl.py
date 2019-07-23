# coding=UTF8
# Copyright (C) 2014  Brigitte Bigi
#
# This file is part of SPPAS.
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

import wx
import wx.lib.newevent

import sppas.src.ui.wxgui.cutils.colorutils as colorutils

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

MIN_W=20
MIN_H=1
MAX_H=20
COLOUR=wx.Colour(70,70,70)


# ----------------------------------------------------------------------------
# Events
# ----------------------------------------------------------------------------

# While the separator is moving, the event is sent,
# with the new position as attribute.

SeparatorMovingEvent, spEVT_MOVING = wx.lib.newevent.NewEvent()
SeparatorMovingCommandEvent, spEVT_MOVING_COMMAND = wx.lib.newevent.NewCommandEvent()

SeparatorMovedEvent, spEVT_MOVED = wx.lib.newevent.NewEvent()
SeparatorMovedCommandEvent, spEVT_MOVED_COMMAND = wx.lib.newevent.NewCommandEvent()

# You can bind the events normally via either binding syntax:
#   self.Bind(spEVT_MOVED, self.handler)
#   spEVT_MOVED(self, self.handler)


# ----------------------------------------------------------------------------
# Pixmaps
# ----------------------------------------------------------------------------

cursor_move = [
    "16 16 2 1",
    " 	c None",
    ".	c #000000",
    "       ..       ",
    "      ....      ",
    "     ......     ",
    "    ........    ",
    "      ....      ",
    "      ....      ",
    "                ",
    "................",
    "................",
    "                ",
    "      ....      ",
    "      ....      ",
    "    ........    ",
    "     ......     ",
    "      ....      ",
    "       ..       "
]


# ----------------------------------------------------------------------------
# Class SeparatorCtrl
# ----------------------------------------------------------------------------


class SeparatorCtrl( wx.Control ):
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: This class is used to draw a movable horizontal line.

    This class implements an horizontal line that can be placed anywhere
    to any wxPython widget, and that can be moved up/down with the mouse.

    @deprecated: Just because it is currently unused (BUT IT WILL BE!!)
    @bug: can move down; CAN'T move up.

    """

    def __init__(self, parent, id=wx.ID_ANY, label="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="Separator"):
        """
        Constructor.
        """

        wx.Control.__init__(self, parent, id, pos, size, style, validator, name)

        # Initialize the pen colour, for faster drawing later
        self.InitializeColours()
        self.InitialSize(size)
        self.InitializeCursor()

        # Allows to move the separator
        self._motional   = False
        self._m_dragging = None

        # Bind the events related to our control: first of all, we use a
        # combination of wx.BufferedPaintDC and an empty handler for
        # wx.EVT_ERASE_BACKGROUND (see later) to reduce flicker
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        # Handling mouse moving.
        wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvents)

    # End __init__
    #-------------------------------------------------------------------------


    def InitializeColours(self):
        """Initializes the pens."""

        self._pen      = wx.Pen(COLOUR,1,wx.SOLID)
        self._brush    = wx.Brush(COLOUR, wx.SOLID)

        contrast = colorutils.ContrastiveColour(COLOUR)
        self._movbrush = wx.Brush(contrast,wx.SOLID)
        self._movpen   = wx.Pen(colorutils.ContrastiveColour(contrast),1,wx.SOLID)


    def InitialSize(self, size):
        """Initialize the size."""

        self.SetMinSize(wx.Size(MIN_W,MIN_H))
        self.SetSize(size)


    def InitializeCursor(self):
        """Initialize cursors."""

        # get cursor image
        bmp = wx.BitmapFromXPMData(cursor_move)
        image = wx.ImageFromBitmap(bmp)

        # since this image didn't come from a .cur file, tell it where the hotspot is
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 8)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 8)
        # make the image into a cursor
        self._cursormove = wx.CursorFromImage(image)


    #-------------------------------------------------------------------------
    # Members
    #-------------------------------------------------------------------------

    def SetMovable(self, value):
        """Activate/Disable the mouse shifting.

        @param value (Boolean)

        """
        self._motional = value


    def GetMovable(self, value):
        """
        Return the mouse shifting state (Boolean).
        """

        return self._motional


    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Look & style
    #-------------------------------------------------------------------------


    def SetColour(self, colour):
        """
        Change the color of the SeparatorCtrl.

        @param colour (wx.Colour)

        """

        self._pen = wx.Pen(colour,1,wx.SOLID)
        self._brush = wx.Brush(colour, wx.SOLID)

        contrast = colorutils.ContrastiveColour(colour)
        self._movpen = wx.Pen(colorutils.ContrastiveColour(contrast),1,wx.SOLID)
        self._movbrush = wx.Brush(contrast,wx.SOLID)

        self.Refresh()

    # End SetColour
    #-------------------------------------------------------------------------


    def SetThickness(self, thick):
        """
        Change the width of the separator.

        @param width (int) is the new width, must be less than 20.

        """

        if int(thick)>MAX_H:
            raise ValueError('Separator.SetThickness. Hum... this is very very large: %d '% int(thick))

        w = self.GetSize().width
        self.SetSize(wx.Size(w,int(thick)))
        self.Refresh()

    # End SetThickness
    #-------------------------------------------------------------------------


    def GetThickness(self):
        """
        Return the current thickness.
        """

        return self.GetSize().height

    # End GetThickness
    #-------------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------


    def OnClose(self, event):
        """Handles the wx.EVT_CLOSE event for Separator."""

        self.Destroy()

    # End OnClose
    #-------------------------------------------------------------------------


    def OnMouseEvents(self, event):
        """Handles the wx.EVT_MOUSE_EVENTS event for Separator."""

        if self._motional is False:
            event.Skip()
            return

        if event.Entering():
            # change cursor to something else to denote possible event capture
            self.SetCursor(self._cursormove)

        elif event.Leaving():
            # change cursor to normal
            self.SetCursor(wx.NullCursor)

        elif event.LeftDown():
            self.OnMouseLeftDown(event)

        elif event.LeftUp():
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

        self._m_dragging = None

        # Left mouse button down, change cursor to
        # something else to denote event capture
        self.SetCursor(self._cursormove)
        # cache current position
        (x,y) = self.GetPosition()
        (ex,ey) = event.GetPosition()
        self._m_dragging = y - ey

    # End onMouseLeftDown
    #-------------------------------------------------------------------------


    def OnMouseLeftUp(self,event):
        """
        Respond to mouse events.
        """
        sx,sy = self.GetPosition()
        x,y = event.GetPosition()

        if self._m_dragging is not None:
            self._m_dragging = None
            self.SetCursor(wx.NullCursor)
            evt = SeparatorMovedEvent(pos=wx.Point(sx,sy))
            evt.SetEventObject(self)
            wx.PostEvent(self.GetParent(), evt)
            self.Refresh()

    # End onMouseLeftUp
    #-------------------------------------------------------------------------


    def OnMouseDragging(self, event):
        """
        Respond to mouse events.
        """
        x,y = self.GetPosition()    # absolute
        ex,ey = event.GetPosition() # relative

        if self._m_dragging is not None:
            direction = self._m_dragging - ey
            if direction > 0 or self._m_dragging==0:
                self._m_dragging = y + ey
            elif direction < 0:
                self._m_dragging = y - ey
            # adjust:
            self._m_dragging = max(self._m_dragging,0)
            self.Move(wx.Point(x,self._m_dragging) )
            evt = SeparatorMovingEvent(pos=wx.Point(x,y))
            evt.SetEventObject(self)
            wx.PostEvent(self.GetParent(), evt)
            self.Refresh()

    # End onMouseDragging
    #-------------------------------------------------------------------------


    def OnPaint(self, event):
        """Handles the wx.EVT_PAINT event for Separator."""

        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    # OnPaint
    #-------------------------------------------------------------------------


    def OnEraseBackground(self, event):
        """Handles the wx.EVT_ERASE_BACKGROUND event for Separator."""
        # This is intentionally empty, because we are using the combination
        # of wx.BufferedPaintDC + an empty OnEraseBackground event to
        # reduce flicker
        pass

    #-------------------------------------------------------------------------


    def Draw(self, dc):
        """
        Draw the separator on the DC, starting at (x,y).

        @param dc
        """
        # Get the actual client size of ourselves
        width, height = self.GetClientSize()

        if not width or not height:
            # Nothing to do, we still don't have dimensions!
            return

        # Initialize the wx.BufferedPaintDC, assigning a background
        # colour and a foreground colour (to draw the text)
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.Clear()

        w,h = self.GetSize()

        dc.SetPen(self._pen)
        dc.SetBrush(self._brush)
        dc.DrawRectangle(0, 0, w, h)

        if self._motional is True and h > 4 and w > 20:
            dc.SetPen(self._movpen)
            dc.SetBrush(self._movbrush)
            middlex = w / 2
            middley = h / 2
            dc.DrawCircle(middlex,middley,2)
            dc.DrawCircle(middlex-8,middley,2)
            dc.DrawCircle(middlex+8,middley,2)
            # add 2 others' sets of circles if very large separator
            if w > 600:
                middlex = w / 8
                middley = h / 2
                dc.DrawCircle(middlex,middley,2)
                dc.DrawCircle(middlex-8,middley,2)
                dc.DrawCircle(middlex+8,middley,2)
                middlex = w - (w / 8)
                middley = h / 2
                dc.DrawCircle(middlex,middley,2)
                dc.DrawCircle(middlex-8,middley,2)
                dc.DrawCircle(middlex+8,middley,2)

    # End Draw
    #-------------------------------------------------------------------------


# ----------------------------------------------------------------------------

import time
import random

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, pos=wx.DefaultPosition, size=wx.Size(840, 320))

        self.w1 = SeparatorCtrl(self, id=-1, pos=(10,80), size=wx.Size(820,10))
        self.w2 = SeparatorCtrl(self, id=-1, pos=(10,100), size=wx.Size(820,10))
        self.w1.SetMovable(True)
        self.w2.SetMovable(True)

        self.b1 = wx.Button(self, -1, "Colour", (10,0))
        self.b2 = wx.Button(self, -1, "Position", (100, 0))
        self.s1 = wx.Button(self, -1, "Size S", (10, 40))
        self.s2 = wx.Button(self, -1, "Size L", (100,40))

        self.Bind(spEVT_MOVING, self.sepmoving)
        self.Bind(spEVT_MOVED,  self.sepmoved)
        self.Bind(wx.EVT_BUTTON, self.repaint1, self.b1)
        self.Bind(wx.EVT_BUTTON, self.repaint2, self.b2)
        self.Bind(wx.EVT_BUTTON, self.repaint3, self.s1)
        self.Bind(wx.EVT_BUTTON, self.repaint4, self.s2)

        self.statusbar = self.CreateStatusBar()
        self.Centre()


    def sepmoving(self,event):
        sep = event.GetEventObject()
        (x,y) = event.pos
        if sep==self.w1:
            self.statusbar.SetStatusText('First separator is moving: %d'%y)
        else:
            self.statusbar.SetStatusText('Second separator is moving: %d'%y)

    def sepmoved(self,event):
        sep = event.GetEventObject()
        (x,y) = event.pos
        if sep==self.w1:
            self.statusbar.SetStatusText('First separator moved to: %d'%y)
        else:
            self.statusbar.SetStatusText('Second separator moved to: %d'%y)


    def repaint1(self, event):
        (r,g,b) = random.sample(range(5,245),  3)
        self.w1.SetColour(wx.Colour(r,g,b))
        (r,g,b) = random.sample(range(5,245),  3)
        self.w2.SetColour(wx.Colour(r,g,b))
        self.statusbar.SetStatusText('Color ok.')

    def repaint2(self, event):
        p1,p2 = random.sample(range(80,300),  2)
        self.w1.Move(wx.Point(10, p1))
        self.w2.Move(wx.Point(10, p2))
        self.Refresh()
        self.statusbar.SetStatusText('Move ok.')

    def repaint3(self, event):
        p1,p2 = random.sample(range(1,10),  2)
        self.w1.SetThickness(p1)
        self.w2.SetThickness(p2)
        self.Refresh()
        self.statusbar.SetStatusText('Size S ok.')

    def repaint4(self, event):
        p1,p2 = random.sample(range(11,20),  2)
        self.w1.SetThickness(p1)
        self.w2.SetThickness(p2)
        self.Refresh()
        self.statusbar.SetStatusText('Size L ok.')


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Test')
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

# ---------------------------------------------------------------------------
