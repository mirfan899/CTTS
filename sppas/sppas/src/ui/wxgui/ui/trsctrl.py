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
#                   Copyright (C) 2011-2018  Brigitte Bigi
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
# File: trsctrl.py
# ----------------------------------------------------------------------------

import logging
import wx

from sppas.src.ui.wxgui.cutils.colorutils import PickRandomColour

from .tierctrl import TierCtrl
from .spControl import spControl

# ---------------------------------------------------------------------------


class TranscriptionCtrl(spControl):
    """Display a Transcription (see anndata for details).

    :author:  Brigitte Bigi
    :contact: contact@sppas.org
    :license: GPL, v3
    :summary:

    """
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 trs=None):
        """Constructor.

        Non-wxPython related parameter:
        :param trs: (Transcription) the object to display (see sppas.annodationdata)

        """
        # Members
        self._trs = trs
        self._tiers = None
        spControl.__init__(self, parent, id, pos, size)

        # Disable Pane (because each tier has its own pane)
        self._infopanep = wx.ALIGN_CENTRE

        # Members
        self._textalign = wx.ALIGN_CENTRE
        self._fontsizeauto = False

        # Transcription members
        self.__set(trs)

        # Bind the events related to our control:
        #wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvents)

        # Handling mouse
        #spEVT_CTRL_SELECTED(self, self.OnTierSelected)

    # -----------------------------------------------------------------------

    def __set(self, trs):
        self._tiers = list()  # list of tier controls

        if trs is not None:
            # estimate the exact height of each tier
            (x, y) = self.GetPosition()  # (0,0)
            (w, h) = self.GetSize()
            theight = self._getTierHeight(h)

            # Create each tier instance
            for t in trs:
                logging.debug('Create TierCtrl for tier: %s' % t.get_name())
                pos = wx.Point(x, y)
                size = wx.Size(w, theight)
                tdc = TierCtrl(self, -1, pos, size, tier=t)
                tdc.SetTime(self._mintime, self._maxtime)
                tdc.SetLabelColours(fontnormalcolour=self._textcolor,
                                    fontuncertaincolour=wx.Colour(30, 30, 130))
                tdc.SetPointColour(colourmidpoint=self._fgcolor)
                tdc.SetFont(self._font)
                tdc.SetLabelAlign(self._textalign)
                self._tiers.append(tdc)

    # -----------------------------------------------------------------------
    # Members: Getters and Setters
    # -----------------------------------------------------------------------

    def GetBegin(self):
        """Override. Return the begin time value of the Transcription()."""

        if self._trs is not None:
            return self._trs.get_min_loc().get_midpoint()
        return 0.

    # -----------------------------------------------------------------------

    def GetEnd(self):
        """Override. Return the end time value of the Transcription()."""
        
        if self._trs is not None:
            return self._trs.get_max_loc().get_midpoint()
        return 0.

    # -----------------------------------------------------------------------

    def GetTranscription(self):
        """Return the Transcription()."""
        
        if self._trs is not None:
            return self._trs
        return None

    # -----------------------------------------------------------------------

    def SetTranscription(self, trs):
        """Set a new Transcription."""
        
        self.__set(trs)

    # -----------------------------------------------------------------------

    def GetTierNames(self):

        if self._trs is None:
            return list()
        return [t.get_name() for t in self._trs]

    # -----------------------------------------------------------------------

    def SetTierChecked(self, checked):
        for i, t in enumerate(self._trs):
            if t.get_name() in checked:
                self._tiers[i].Show()
            else:
                self._tiers[i].Hide()
        self.RequestRedraw()

    # -----------------------------------------------------------------------

    def GetTierIdxChecked(self):
        checked = list()
        for i, t in enumerate(self._tiers):
            if t.IsShown() is True:
                checked.append(i)
        return checked

    # -----------------------------------------------------------------------
    # Preferences
    # -----------------------------------------------------------------------

    def SetTextAlign(self, value):
        """Fix the position of the text of an annotation.

        :param value: one of wx.ALIGN_LEFT, wx.ALIGN_CENTRE or wx.ALIGN_RIGHT

        """
        if value != self._textalign:
            self._textalign = value
            for tdc in self._tiers:
                tdc.SetLabelAlign(value)

    # -----------------------------------------------------------------------

    def SetTierBackgroundColour(self, value):
        """Fix the background color of all tiers.

        :param value: (wx.Colour)

        """
        if value is not None:
            for tdc in self._tiers:
                tdc.SetLabelColours(bgcolour=value)
                tdc.SetForegroundColour(value)
        else:
            for tdc in self._tiers:
                value = PickRandomColour(150, 250)
                tdc.SetLabelColours(bgcolour=value)
                tdc.SetForegroundColour(value)

    # -----------------------------------------------------------------------

    def SetPointColour(self, color):
        """Set a new foreground color.

        :param color: (wx.Colour)

        """
        for tdc in self._tiers:
            tdc.SetPointColour(color)

    # -----------------------------------------------------------------------
    # Look Setters and Getters
    # -----------------------------------------------------------------------

    def SetBackgroundColour(self, colour):
        """Sets the TranscriptionCtrl background color.
        Ask to redraw only if color has changed.

        :param colour: (wx.Colour)

        """
        spControl.SetBackgroundColour(self, colour)
        for t in self._tiers:
            t.SetBackgroundColour(colour)

    # -----------------------------------------------------------------------

    def SetHandlesColour(self, colour):
        """Sets the TranscriptionCtrl handles color.
        Ask to redraw only if color has changed.

        :param colour: (wx.Colour)

        """
        spControl.SetHandlesColour(self, colour)

    # -----------------------------------------------------------------------

    def SetTextColour(self, colour):
        """Sets the TranscriptionCtrl text color.
        Ask to redraw only if color has changed.

        :param colour: (wx.Colour)

        """
        spControl.SetTextColour(self, colour)
        for t in self._tiers:
            t.SetLabelColours(fontnormalcolour=colour)

    # -----------------------------------------------------------------------

    def SetFont(self, font):
        """Sets the TranscriptionCtrl text font.
        Ask to redraw only if color has changed.

        :param font: (wx.Font)

        """
        spControl.SetFont(self, font)
        for t in self._tiers:
            t.SetFont(font)

    # -----------------------------------------------------------------------
    # TranscriptionCtrl display
    # -----------------------------------------------------------------------

    def SetPanePosition(self, value):
        """Override. Fix the position of the information pane for tiers.

        :param value: is one of wx.ALIGN_LEFT, wx.ALIGN_CENTRE or wx.ALIGN_RIGHT.

        """
        for t in self._tiers:
            t.SetPanePosition(value)

    # -----------------------------------------------------------------------

    def SetPaneWidth(self, value):
        """
        Override. Fix the width of the information pane.

        :param value: (int) is between 10 and 200.

        """
        spControl.SetPaneWidth(self, value)
        for t in self._tiers:
            t.SetPaneWidth(value)

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def OnMouseEvents(self, event):
        """Handles the wx.EVT_MOUSE_EVENTS event for this Ctrl."""

        if event.Moving():
            wx.PostEvent(self.GetParent().GetEventHandler(), event)

        event.Skip()

    # ------------------------------------------------------------------------

    def OnTierSelected(self, event):
        """A tier was selected."""

        return
        # Which tier was selected?
        #tierctrl = event.GetEventObject()
        #tier     = event.tier

    # -----------------------------------------------------------------------
    # Paint
    # -----------------------------------------------------------------------

    def DrawPane(self, dc, x, y, w, h):
        """Do not draw anything (each tier draw its own pane)."""
        pass

    # -----------------------------------------------------------------------

    def DrawContent(self, dc, x, y, w, h):
        """Draw each tier of the trs on the DC, in the range of the given time period."""

        if self._trs is None:
            return  # not initialized
        if self._tiers is None:
            return  # not initialized

        # the period is not covering this trs: do not draw anything
        if self._mintime > self.GetEnd():
            return

        # estimate the exact height of each tier
        theight = self._getTierHeight(h)

        # draw each tier (only if necessary).
        for t in self._tiers:
            if t.IsShown() is True:
                t.SetTime(self._mintime, self._maxtime)
                t.MoveWindow(wx.Point(x, y), wx.Size(w, theight))
                ht = t.GetHeight()
                y = y + ht

        if y != h:
            logging.info('[WARNING] Transcription. '
                         'DO NOT Force resize from %d to %d.' % (h, y))
            self.SetSize(wx.Size(w, y))

    # -----------------------------------------------------------------------
    # Private...
    # -----------------------------------------------------------------------

    def _getTierHeight(self, h):
        nbt = 0
        for i, t in enumerate(self._tiers):
            if t.IsShown() is True:
                nbt = nbt + 1
        if nbt == 0:
            return 0
        seph = 0  # self._sep.GetPenWidth()
        septh = seph * (nbt-1)
        return int((h-septh) / nbt)
