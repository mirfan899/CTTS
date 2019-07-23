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
# File: displayctrl.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__ = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx
import wx.lib
import logging
import os

import sppas.src.audiodata.aio
from sppas.src.anndata import sppasRW

from sppas.src.ui.wxgui.structs.files import xFiles
from sppas.src.ui.wxgui.structs.dataperiod import DataPeriod
from sppas.src.ui.wxgui.cutils.imageutils import TakeScreenShot
from sppas.src.ui.wxgui.dialogs.msgdialogs import ShowInformation

from .timerulerctrl import TimeRulerCtrl
from .trsctrl import TranscriptionCtrl
from .wavectrl import WaveCtrl
from .spControl import spEVT_CTRL_SELECTED

from sppas.src.ui.wxgui.ui.CustomEvents import ObjectSelectedEvent

# ----------------------------------------------------------------------------
# CONSTANTS (can not be changed)
# ----------------------------------------------------------------------------

MIN_W = 320
MIN_H = 200

# ----------------------------------------------------------------------------


class DisplayCtrl(wx.Window):
    """Displays annotated files and media files.

    @author:  Brigitte Bigi
    @contact: contact@sppas.org
    @license: GPL, v3
    @summary: This class is used to display speech sounds and annotation files.

    The displayed area is made of two vertical parts: a pane is used to print
    information about what is drawn on the other one.

    """

    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 prefsIO = None):
        """Constructor.

        Non-wxPython related parameter:
            - prefsIO [REQUIRED]

        """
        style = wx.NO_BORDER | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_CHILDREN | wx.WANTS_CHARS
        wx.Window.__init__(self, parent, id, pos, size=(MIN_W, MIN_H), style=style)
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(prefsIO.GetValue('M_BG_COLOUR'))
        self.SetMinSize((MIN_W, MIN_H))

        # Members
        self._xfiles = xFiles()
        self._prefsIO = prefsIO

        # Members indicating the current state
        self._mousescroll = None
        self._ymax = 0

        # Tools (period, ruler, ...)
        self.__set_tools()

        # Set initial dc mode to fast
        self._reInitBuffer = False
        self.InitBuffer()

        # Bind events
        self.__bind_events()

        # Start the background redraw timer.
        self.redrawTimer = wx.Timer(self)
        self.redrawTimer.Start(10)

    # ------------------------------------------------------------------------

    def __set_tools(self):
        """Create tools and set their default parameters."""

        s = self.GetSize()

        try:
            mintime = self._prefsIO.GetValue('D_TIME_MIN')
        except Exception:
            mintime = 0.0

        try:
            maxtime = self._prefsIO.GetValue('D_TIME_MAX')
        except Exception:
            maxtime = 3.0

        try:
            minzoom = self._prefsIO.GetValue('D_TIME_ZOOM_MIN')
        except Exception:
            minzoom = 0.2  # min zoom to 200 milliseconds

        try:
            maxzoom = self._prefsIO.GetValue('D_TIME_ZOOM_MAX')
        except Exception:
            maxzoom = 300.  # max zoom to 5 minutes

        # The displayed period of time
        self._period = DataPeriod(mintime, maxtime)
        self._period.SetMin(mintime)
        self._period.SetMax(maxtime)
        self._period.SetMinDelta(minzoom)
        self._period.SetMaxDelta(maxzoom)

        # The ruler, at the top of the drawing
        self._timeruler = TimeRulerCtrl(self, -1, pos=(0, 0), size=(s.width, 24))
        self._objSetPreferences(self._timeruler)
        self._timeruler.SetDrawingParent(self)
        self._timeruler.SetTime(0., self._period.GetMax())
        # indicators on the ruler:
        self._timeruler.SetPlayerIndicatorValue(self._period.GetStart())
        self._timeruler.SetSelectionIndicatorValues(self._period.GetStart(), self._period.GetStart())
        # Store the ruler into the list of objects
        self._xfiles.Append("TIME_RULER", self._timeruler)

    # -----------------------------------------------------------------------

    def __bind_events(self):
        """Bind events."""

        # Only refresh drawing when resizing is finished
        wx.EVT_PAINT(self, self.onPaint)
        wx.EVT_SIZE(self,  self.onSize)
        wx.EVT_CLOSE(self, self.onClose)
        wx.EVT_IDLE(self,  self.onIdle)
        wx.EVT_ERASE_BACKGROUND(self, lambda event: None)

        # Handling mouse moving.
        wx.EVT_MOUSE_EVENTS(self, self.onMouseEvents)

        # Mouse selection
        self.Bind(spEVT_CTRL_SELECTED, self.onSelectedObject)
        self.Bind(wx.EVT_TOOL_RANGE, self.onSelectionRange)

    # -----------------------------------------------------------------------

    def DisplayPeriodInStatusbar(self, mint, maxt):
        """Display the time period in the status bar."""

        text = 'Period: ' + str(mint) + ' to ' + str(maxt)
        try:
            wx.GetTopLevelParent(self).SetStatusText(text, 1)
        except:
            logging.info(text)

    # -----------------------------------------------------------------------

    def DisplayMouseInStatusbar(self, t):
        """Display the mouse position in the status bar."""

        text = 'Mouse: ' + str(t)
        try:
            wx.GetTopLevelParent(self).SetStatusText(text, 2)
        except:
            pass

    # -----------------------------------------------------------------------
    # Data: -- Setters --
    # -----------------------------------------------------------------------

    def FixWaveHeight(self, wf):
        try:
            channel_height = self._prefsIO.GetValue('W_HEIGHT')
        except:
            channel_height = 100
        return channel_height * wf.get_nchannels()

    # -----------------------------------------------------------------------

    def FixTranscriptionHeight(self, tf):
        try:
            tier_height = self._prefsIO.GetValue('T_HEIGHT')
        except:
            tier_height = 30
        return tier_height * len(tf)

    # -----------------------------------------------------------------------

    def SetData(self, f):
        """Add a new file to draw.

        :param f: (string) is a file name.

        """
        if self._xfiles.Exists(f):
            raise IOError('Display. SetData. The file was already loaded: %s' % f)

        s = self.GetClientSize()
        file_name, file_ext = os.path.splitext(f)
        logging.debug('DisplayCtrl.SetData: %s , %s' % (file_name, file_ext))

        # Load data, create the corresponding control
        if file_ext.lower() in sppas.src.audiodata.aio.extensions:
            try:
                wf = sppas.src.audiodata.aio.open(f)
            except Exception as e:
                ShowInformation(self,
                                self._prefsIO,
                                "The following error occurred while loading file "+f+".\n"+str(e),
                                style=wx.ICON_INFORMATION)
                raise
            h = self.FixWaveHeight(wf)
            dcobj = WaveCtrl(self, -1,
                             pos=wx.Point(0, self._ymax),
                             size=wx.Size(s.width, h),
                             audio=wf)
            dcobj.SetGradientBackground(True)  # Gradient bg

        else:
            try:
                parser = sppasRW(f)
                tf = parser.read()
            except Exception as e:
                ShowInformation(self,
                                self._prefsIO,
                                "The following error occurred while loading file "+f+".\n"+str(e),
                                style=wx.ICON_INFORMATION)
                raise

            h = self.FixTranscriptionHeight(tf)
            dcobj = TranscriptionCtrl(self, -1,
                                      pos=wx.Point(0, self._ymax),
                                      size=wx.Size(s.width, h),
                                      trs=tf)

        self._period.SetMax(max(dcobj.GetEnd(), self._period.GetMax()))

        # Preferences
        dcobj.SetTime(self._period.GetStart(), self._period.GetEnd())
        self._objSetPreferences(dcobj)

        # Add the bottom separator
        #s = Separator(self, -1, pos=wx.Point(0,0), size=wx.Size(s.width,self._prefsIO.GetValue('S_PEN_WIDTH')))
        #s.SetColour(self._prefsIO.GetValue('S_COLOUR'))

        # Store the filename , the control and the separator
        self._xfiles.Append(f, dcobj)

        # updates
        self.DisplayPeriodInStatusbar(self._period.GetStart(),
                                      self._period.GetEnd())

        self.RequestRedraw()

    # ------------------------------------------------------------------------

    def UnsetData(self, f):
        """Remove a file of the drawing.

        :param f: (string) is a file name.

        """
        if self._xfiles.Exists(f) is False:
            return False

        # Get information about the object to remove (idx, filename)
        idx = self._xfiles.GetIndex(f)
        obj = self._xfiles.GetFilename(idx)
        dcobj = self._xfiles.GetObject(idx)
        if dcobj.IsSelected():
            self.SetSelectedObject(None)

        # remove the filemane/control of the dict
        self._xfiles.Remove(idx)

        # ask the control to close itself
        wx.PostEvent(dcobj.GetEventHandler(), 
                     wx.PyCommandEvent(wx.EVT_CLOSE.typeId, dcobj.GetId()))
        dcobj.Destroy()

        # update the max time value
        mmax = self._period.GetMin()
        for i in range(self._xfiles.GetSize()):
            o = self._xfiles.GetObject(i)
            m = o.GetEnd()
            if m > mmax:
                mmax = m
        self._period.SetMax(mmax)
        self.DisplayPeriodInStatusbar(self._period.GetStart(),
                                      self._period.GetEnd())

        self.RequestRedraw()
        return True

    # ------------------------------------------------------------------------

    def UnsetAllData(self):
        """
        Clean information and destroy all data.
        """

        for i in reversed(range(self._xfiles.GetSize())):
            f = self._xfiles.GetFilename(i)
            self.UnsetData(f)

    # ------------------------------------------------------------------------
    # Preferences: -- Setters --
    # ------------------------------------------------------------------------

    def SetPreferences(self, prefs):
        """Set new preferences."""

        self._prefsIO = prefs
        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            self._objSetPreferences(obj)

        self.RequestRedraw()

    # ------------------------------------------------------------------------
    # Members: -- Getters -- Setters --
    # ------------------------------------------------------------------------

    def GetData(self):
        """Return the list of really displayed file names."""

        l = []
        for i in range(self._xfiles.GetSize()):
            if self._xfiles.GetObject(i) is not None:
                f = self._xfiles.GetFilename(i)
                #if f != "TIME_RULER":
                l.append(f)
        return l

    # ------------------------------------------------------------------------

    def GetRuler(self):
        """Return the ruler (TimeRuler)."""

        return self._timeruler

    # ------------------------------------------------------------------------

    def GetSelectedObject(self):
        """Return the the selected object (or None)."""

        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if obj.IsSelected():
                return obj

        return None

    # ------------------------------------------------------------------------

    def SetSelectedObject(self, sel):
        """Set selected object (if sel is different of the current' one)."""

        # Nothing to do: same object selected!
        if self.GetSelectedObject() == sel:
            return

        f = ""
        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if obj != sel:
                obj.SetSelected(False)
            else:
                obj.SetSelected(True)
                if "TIME_RULER" != self._xfiles.GetFilename(i):
                    f = self._xfiles.GetFilename(i)
                break

        evt = ObjectSelectedEvent(object=sel,string=f)
        evt.SetEventObject(self)
        wx.PostEvent(self.GetParent(), evt)

    # ------------------------------------------------------------------------

    def GetSelectionFilename(self):
        """Return the file name of the selected object (or an empty string)."""

        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if obj.IsSelected():
                return self._xfiles.GetFilename(i)

        return ""

    # ------------------------------------------------------------------------

    def GetPeriod(self):
        """Return the displayed period."""

        return self._period

    # ------------------------------------------------------------------------

    def SetPeriod(self, period):
        """Set a new data period."""
        
        self._period = period
        self._updatedPeriod()
        self._updateRulerIndicators(period)
        self.RequestRedraw()

        self.DisplayPeriodInStatusbar(self._period.GetStart(),
                                      self._period.GetEnd())
        self.DisplayMouseInStatusbar("...")

    # ------------------------------------------------------------------------

    def GetPeriodValues(self):
        """Return a tuple with (mintime,maxtime) of the displayed period."""

        return self._period.GetStart() , self._period.GetEnd()

    # ------------------------------------------------------------------------

    def SetPeriodValues(self, start, end):
        """Return a tuple with (mintime,maxtime) of the displayed period."""

        self._period.Update(start, end)
        self._updatedPeriod()
        self.RequestRedraw()

        self.DisplayPeriodInStatusbar(self._period.GetStart(),
                                      self._period.GetEnd())

    # ------------------------------------------------------------------------
    # Callbacks to MOUSE events
    # ------------------------------------------------------------------------

    def onSelectionRange(self, event):
        """The period selection was changed by an object."""

        idt = event.GetId()
        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if idt == obj.GetId():
                (x1, x2) = obj.GetCurrentMouseSelection()
                s = self._getTimeValue(x1, self.GetSize()[1])
                e = self._getTimeValue(x2, self.GetSize()[1])
                # Report on the ruler indicators...
                period = DataPeriod(s, e)
                self.SetPeriod(period)

    # ------------------------------------------------------------------------

    def onSelectedObject(self, event):
        """Event handler used by an object when it is selected."""

        idt = event.GetId()
        ctrl = event.GetEventObject()

        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if idt == obj.GetId() or ctrl == obj:
                self.SetSelectedObject(obj)

    # ------------------------------------------------------------------------

    def onMouseEvents(self, event):
        """Event handler used when the mouse is operated."""

        if event.Entering():
            pass

        elif event.Leaving():
            pass

        elif event.LeftDown():
            self.onMouseLeftDown(event)

        elif event.LeftUp():
            self.onMouseLeftUp(event)

        elif event.Moving():
            # moving without a button pressed
            self.onMouseMotion(event)

        elif event.Dragging():
            # moving while a button is pressed
            self.onMouseDragging(event)

        elif event.ControlDown() and event.GetWheelRotation() > 0:
            try:
                self.GetParent().GetNavigPanel().onPeriodZoomIn(event)
            except Exception:
                pass

        elif event.ControlDown() and event.GetWheelRotation() < 0:
            try:
                self.GetParent().GetNavigPanel().onPeriodZoomOut(event)
            except Exception:
                pass

        elif event.ShiftDown() and event.GetWheelRotation() > 0:
            self.ZoomUp()

        elif event.ShiftDown() and event.GetWheelRotation() < 0:
            self.ZoomDown()

        elif event.AltDown() and event.GetWheelRotation() > 0:
            pass

        elif event.AltDown() and event.GetWheelRotation() < 0:
            pass

        elif event.GetWheelRotation() > 0:
            try:
                self.GetParent().GetNavigPanel().onGoNext(event)
            except Exception:
                pass

        elif event.GetWheelRotation() < 0:
            try:
                self.GetParent().GetNavigPanel().onGoBack(event)
            except Exception:
                pass
        else:
            logging.info(' Mouse event ignored ')

        event.Skip()

    # ------------------------------------------------------------------------

    def onMouseMotion(self, event):
        """
        Respond to mouse events in the main drawing panel
        """
        self.DisplayMousePosition(event.X, event.Y)

    # ------------------------------------------------------------------------

    def onMouseLeftDown(self, event):
        """
        Respond to mouse events in the main drawing panel.
        """
        self._mousescroll = wx.Point(event.X,event.Y)

    # ------------------------------------------------------------------------

    def onMouseLeftUp(self,event):
        """
        Respond to mouse events in the main drawing panel.
        """

        # Handle the selected object
        mousePt = wx.Point(event.X,event.Y)

        if self._mousescroll is not None:
            # this is an approximation (do not take into account the left pane)
            w, h = self.GetSize()
            (_x, _y) = mousePt
            coeff = float(self._mousescroll.x - _x) / float(w)
            # update the navig panel (it will do everything)
            try:
                self.GetParent().GetNavigPanel().SetNewPeriod(1.0+coeff, "scroll")
            except Exception:
                pass

        self._mousescroll = None
        self.SetSelectedObject(None)
        self.RequestRedraw()

    # ------------------------------------------------------------------------

    def onMouseDragging(self, event):
        """
        Respond to mouse events in the main drawing panel.
        """
        if self._mousescroll is not None:
            # this is an approximation (do not take into account the left pane)
            w, h = self.GetSize()
            (_x, _y) = wx.Point(event.GetX(), event.GetY())
            coeff = float(self._mousescroll.x - _x) / float(w)
            try:
                self.GetParent().GetNavigPanel().SetNewPeriod(1.0+coeff, "scroll")
            except Exception:
                pass
            # Show changes
            self.RequestRedraw()
            self._mousescroll = wx.Point(event.GetX(), event.GetY())
            
    # ------------------------------------------------------------------------
    # Display management -- Vertical Zoom --
    # ------------------------------------------------------------------------

    def ZoomUp(self):
        self.SetVertZoom(1.0 + self._prefsIO.GetValue('D_V_ZOOM')/100.0)

    # ------------------------------------------------------------------------

    def ZoomDown(self):
        self.SetVertZoom(1.0 - self._prefsIO.GetValue('D_V_ZOOM')/100.0)

    # ------------------------------------------------------------------------

    def SetVertZoom(self, z):
        """Apply a vertical zoom to all objects or only on the selected (if any).

        :param z: (float) is a zoom coefficient (typical values are ranging from 0.5 to 1.5).

        """
        if z == 1.0 or z < 0.0 or z > 2.0:
            return

        selected = self.GetSelectedObject()

        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            if obj.IsSelected() or selected is None:
                obj.VertZoom(z)

        self.RequestRedraw()

    # ------------------------------------------------------------------------
    # DC management (draw, redraw, resize, refresh, ...)
    # ------------------------------------------------------------------------

    def InitBuffer(self):
        """Initialize the bitmap used for buffering the display."""
        
        w, h = self.GetSize()

        self._buffer = wx.EmptyBitmap(max(1, w), max(1, h))
        dc = wx.BufferedDC(None, self._buffer)
        dc.SetBackground(wx.Brush(self._prefsIO.GetValue('W_BG_COLOUR')))
        dc.Clear()

        self.Draw()
        del dc  # commits all drawing to the buffer
        self._reInitBuffer = False

    # ------------------------------------------------------------------------

    def RequestRedraw(self):
        """Requests a redraw of the drawing panel contents.

        The actual redrawing doesn't happen until the next idle time.
        
        """
        self._reInitBuffer = True

    # ------------------------------------------------------------------------

    def onSize(self, event):
        """Event handler used when the window has been resized."""
        self.Layout()
        self.RequestRedraw()

    # ------------------------------------------------------------------------

    def onIdle(self, event):
        """
        If the size was changed then resize the bitmap used for double
        buffering to match the window size.  We do it in Idle time so
        there is only one refresh after resizing is done, not lots while
        it is happening.
        
        """
        if self._reInitBuffer and self.IsShown():
            self.InitBuffer()
            self.Refresh(False)

    # ------------------------------------------------------------------------

    def onPaint(self, event):
        """Called when the window is exposed."""
        dc = wx.BufferedPaintDC(self, self._buffer)

    # ------------------------------------------------------------------------

    def Draw(self):
        """Draw all the objects on the DC."""
        if self._xfiles.GetSize() == 0:
            return

        size = self.GetSize()
        w, h = size.width, size.height
        x, y = 0, 0

        # The objects
        for i in range(self._xfiles.GetSize()):

            dcobj = self._xfiles.GetObject(i)
            if dcobj is None:
                continue
            try:
                logging.debug('DisplayCtrl.draw. %s, y=%d'%(self._xfiles.GetFilename(i), y))
                (wo, ho) = dcobj.GetSize()
                dcobj.MoveWindow(wx.Point(x,y) , wx.Size(w,ho))
                h = dcobj.GetHeight()
            except Exception as e:
                logging.info(' * * * * Error while drawing * * *  ... %s ' % str(e))
                h = 0
            y = y + h

        self._ymax = y

    # ------------------------------------------------------------------------

    def GetImage(self):
        """Return the drawer as an image, or None."""

        rect = self.GetParent().GetRect()
        client_x, client_y = self.ClientToScreen((0,0))
        logging.info('Take a snap shot of the display: %d,%d,%d,%d ; '
                     '%d,%d' % (rect.x, rect.y, rect.width, rect.height, 
                                client_x, client_y))
        (rect.x, rect.y) = self.ClientToScreenXY(rect.x, rect.y)

        return TakeScreenShot(rect, client_x, client_y)

    # ------------------------------------------------------------------------

    def DisplayMousePosition(self, x, y):
        """Display the time value corresponding to the mouse position
        in the parent statusbar.
        
        """
        size = self.GetSize()
        w, h = size.width, size.height
        t = self._getTimeValue(x, w)
        if t >= 0:
            self.DisplayMouseInStatusbar(t)
        else:
            self.DisplayMouseInStatusbar('...')

    # ------------------------------------------------------------------------
    # EVENT CALLBACKS
    # ------------------------------------------------------------------------

    def onClose(self, event):
        """
        Close (destructor).
        """

        self.redrawTimer.Stop()

        # The objects
        for i in range(self._xfiles.GetSize()):
            dcobj = self._xfiles.GetObject(i)
            if dcobj is not None:
                # ask the control to close itself
                wx.PostEvent(dcobj.GetEventHandler(), 
                             wx.PyCommandEvent(wx.EVT_CLOSE.typeId, dcobj.GetId()))
                dcobj.Destroy()

        self.Destroy()

    # ------------------------------------------------------------------------

    # =====================
    # == Private Methods ==
    # =====================

    def _objSetPreferences(self, obj):
        """Set current preferences to any spControl object."""

        if isinstance(obj,TimeRulerCtrl):
            obj.SetBackgroundColour(self._prefsIO.GetValue('R_BG_COLOUR'))
            obj.SetForegroundColour(self._prefsIO.GetValue('R_FG_COLOUR'))
            obj.SetTicksColour(self._prefsIO.GetValue('R_FG_COLOUR'))
            obj.SetFont(self._prefsIO.GetValue('R_FONT'))
            obj.SetHandlesColour(self._prefsIO.GetValue('R_HANDLES_COLOUR'))
            obj.SetTextColour(self._prefsIO.GetValue('R_FONT_COLOUR'))
            obj.SetHeight(self._prefsIO.GetValue('R_HEIGHT'))

        if isinstance(obj, TranscriptionCtrl):
            obj.SetForegroundColour(self._prefsIO.GetValue('T_FG_COLOUR'))
            obj.SetBackgroundColour(self._prefsIO.GetValue('M_BG_COLOUR'))
            obj.SetTierBackgroundColour(self._prefsIO.GetValue('T_BG_COLOUR'))
            obj.SetTextAlign(self._prefsIO.GetValue('T_LABEL_ALIGN'))
            obj.SetHandlesColour(self._prefsIO.GetValue('T_HANDLES_COLOUR'))
            obj.SetPointColour(self._prefsIO.GetValue('T_RADIUS_COLOUR'))
            obj.SetFont(self._prefsIO.GetValue('T_FONT'))
            obj.SetTextColour(self._prefsIO.GetValue('T_FONT_COLOUR'))
            # tier height ???

        if isinstance(obj, WaveCtrl):
            obj.SetForegroundColour(self._prefsIO.GetValue('W_FG_COLOUR'))
            obj.SetBackgroundColour(self._prefsIO.GetValue('W_BG_COLOUR'))
            obj.SetAutoAdjust(self._prefsIO.GetValue('W_AUTOSCROLL'))
            obj.SetAutoColor(self._prefsIO.GetValue('W_FG_DISCO'))
            obj.SetHandlesColour(self._prefsIO.GetValue('W_HANDLES_COLOUR'))
            obj.SetBackgroundGradientColour(self._prefsIO.GetValue('W_BG_GRADIENT_COLOUR'))
            obj.SetFont(self._prefsIO.GetValue('W_FONT'))
            obj.SetTextColour(self._prefsIO.GetValue('W_FONT_COLOUR'))
            # channel height ???

    # ------------------------------------------------------------------------

    def _updatedPeriod(self):
        for i in range(self._xfiles.GetSize()):
            obj = self._xfiles.GetObject(i)
            obj.SetTime(self._period.GetStart(),self._period.GetEnd())

    # ------------------------------------------------------------------------

    def _updateRulerIndicators(self, period):
        # update the ruler selection period, depending on the new period.

        start = period.GetStart()
        end = period.GetEnd()

        self._timeruler.SetPlayerIndicatorValue(start)

        selstart = self._timeruler.GetSelectionIndicatorMinValue()
        selend = self._timeruler.GetSelectionIndicatorMaxValue()
        if selstart >= start and selend <= end:
            return

        quart = (end - start) / 4.
        if selend > start or selstart > end:
            # selection is outside the period
            selstart = start+quart
            selend = end-quart
        elif selstart < start:
            # selection overlaps at start
            selstart = start
            if selstart >= selend:
                selend = selstart+quart
        elif selend > end:
            # selection overlaps at end
            selend = end
            if selend <= selstart:
                selstart = selend - quart

        self._timeruler.SetSelectionIndicatorValues(selstart, selend)

    # ------------------------------------------------------------------------

    def _getTimeValue(self, x, w):
        """
        Convert the X value (in pixels) into a Time value,
        depending on the displayed period.
        """
        ww = w
        xx = x
        if self._xfiles.GetSize() > 0:
            obj = self._xfiles.GetObject(0)
            pos = obj.GetPanePosition()
            if pos != wx.ALIGN_CENTRE:
                panew = obj.GetPaneWidth()
                ww = w - panew
                if pos == wx.ALIGN_LEFT:
                    xx = x - panew

        return self._period.PixelsToDuration(xx, ww)
