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
# File: dataperiod.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


PRECISION = 3  # number of digits, for zoom or scroll.

# -----------------------------------------------------------------------------


class DataPeriod(object):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL
    @summary: This class is used to represent the displayed time period.

    Represents an interval using a start and end value: [start,end].
    It is assumed that start and end are included inside the interval.
    The degenerate interval is not allowed.

    Two pairs of values can be fixed:
        - min/max of the delta (where delta = end - start),
        - min/max of the values.

    """
    def __init__(self, start, end):
        """
        Create a new DataPeriod() instance with default values.

        @param start (float)
        @param end (float)
        """

        self._start = start            # current displayed start value
        self._end   = end              # current displayed end value
        self._mind  = float(start)/10. # minimum displayed delta (for zoom estimation)
        self._maxd  = end-start        # maximum displayed delta (for zoom estimation)
        self._minv  = start            # minimum value (for start)
        self._maxv  = end              # maximum value (for end)

    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def GetStart(self):
        """
        Return the start value (float).
        """
        return self._start

    #-------------------------------------------------------------------------


    def GetEnd(self):
        """
        Return the end value (float).
        """
        return self._end

    #-------------------------------------------------------------------------


    def Delta(self):
        """
        Return the delta (float) of this period.
        """
        return self._end - self._start

    #-------------------------------------------------------------------------


    def GetMin(self):
        """
        Return the min start value (float).
        """
        return self._minv

    #-------------------------------------------------------------------------


    def GetMax(self):
        """
        Return the max end value (float).
        """
        return self._maxv

    #-------------------------------------------------------------------------


    def GetMinDelta(self):
        """
        Return the min delta (float).
        """
        return self._mind

    #-------------------------------------------------------------------------


    def GetMaxDelta(self):
        """
        Return the max delta (float).
        """
        return self._maxd

    #-------------------------------------------------------------------------


    def Inside(self, value):
        """
        Return True if the given value is inside the period or on the border,
        otherwise return False.
        """
        return value >= self._start and value <= self._end

    #-------------------------------------------------------------------------


    def Outside(self, value):
        """
        Return True if the given value is outside the period,
        otherwise return False.
        """
        return not self.Insize(value)

    #-------------------------------------------------------------------------


    def Overlap(self, period):
        """
        Return True if the current period has any overlap with the given period.
        """
        return not (period.get_end() < self._start or
                    period.get_start() > self._end)

    #-------------------------------------------------------------------------
    # Setters...
    #-------------------------------------------------------------------------


    def SetMaxDelta(self, delta):
        """
        Fix a maximum delta value.
        Used to ensure an acceptable zoom.
        """
        self._maxd = delta

    #-------------------------------------------------------------------------


    def SetMinDelta(self, delta):
        """
        Fix a minimum delta value.
        Used to ensure an acceptable zoom.
        """
        self._mind = delta

    #-------------------------------------------------------------------------


    def SetMin(self, value):
        """
        Fix a minimum value.
        """
        self._minv = value

    #-------------------------------------------------------------------------


    def SetMax(self, value):
        """
        Fix a maximum value.
        """
        self._maxv = value

    #-------------------------------------------------------------------------


    def Check(self, start, end):
        """
        Check if a new data period interval is allowed.
        Return the nearest good values.
        """

        # reverse!
        if end < start:
            a = end
            end = start
            start = a

        # check values (compared to minv/maxv)
        if start < self._minv:
            start = self._minv
        if end > self._maxv:
            end = self._maxv

        # check new data period (compared to mind/maxd)
        delta = end - start
        if delta < self._mind:
            # enlarge
            start = start - self._mind/2.
            end   = end + self._mind/2.
        elif delta > self._maxd:
            # reduce
            start = start + self._maxd/2.
            end   = end - self._maxd/2.

        return start,end

    #-------------------------------------------------------------------------


    def Update(self, start, end):
        """
        Change the data period values.

        If range is invalid, it will not be set, and a ValueError will be
        raised instead.
        """
        if start >= end:
            raise ValueError("Invalid period: start after end!")

        (self._start,self._end) = self.Check(start,end)

    #-------------------------------------------------------------------------


    def Zoom(self, times, precision=PRECISION):
        """
        Return a tuple (start,end) of values, if a zoom is applied.
        This will not affect the current period.
        Zoom is estimated by stating on the middle.

        If times is 1.0, zoom will not affect start and end time values.
        If times is less than 1.0, zoom out.
        If times is more than 1.0, zoom in.

        @param times (float) is a value ranging from 0.0 to 2.0.
        """
        # Check times
        times = float(times)
        if times <= 0.0:
            return (self._start, self._end)
        if times > 2.0:
            times = 2.0

        if times > 1.0:
            shift = (self.Delta()*(times-1.0))/2.0
            start = max(self._minv, round(self._start - shift, precision))
            end   = min(self._maxv, round(self._end   + shift, precision))
        else:
            shift = (self.Delta()*times)/2.0
            start = max(self._minv, round(self._start + shift, precision))
            end   = min(self._maxv, round(self._end   - shift, precision))

        return self.Check(start,end)

    #-------------------------------------------------------------------------


    def Scroll(self, times, precision=PRECISION):
        """
        Return a tuple (start,end) of values, if a scroll is applied.
        This will not affect the current period displayed.

        If times is 1.0, scroll will not affect start and end time values.
        If times is less than 1.0, scroll to the right.
        If times is more than 1.0, scroll to the left.

        @param times (float) is a value ranging from 0.0 to 2.0.
        """
        # Check times
        times = float(times)
        if times <= 0.0:
            return (self._start, self._end)
        if times > 2.0:
            times = 2.0

        # Estimates the shift for scrolling
        shift = round( (self.Delta() * times) - self.Delta() , precision)

        # Apply on end (take care of the max value)
        end = self._end + shift
        if end > self._maxv:
            end   = self._maxv
            shift = round(end - self._end , precision)
        else:
            end = round(end, precision)

        # Apply on start (take care of the min value)
        start = self._start + shift
        if start < self._minv:
            start = self._minv
            shift = round(abs(start - self._start), precision)
            end = round(self._end + shift, precision)
        else:
            start = round(start, precision)

        return start,end

    #-------------------------------------------------------------------------


    def ScrollToStart(self, precision=PRECISION):
        """
        Return a tuple (start,end) of values, if a scroll to the min value
        is applied. This will not affect the current period displayed.
        Delta is not changed.
        """
        shift = self._start - self._minv
        end   = round(self._end - shift, precision)

        return (self._minv,end)

    #-------------------------------------------------------------------------


    def ScrollToEnd(self, precision=PRECISION):
        """
        Return a tuple (start,end) of values, if a scroll to the max value
        is applied. This will not affect the current period displayed.
        Delta is not changed.
        """
        shift = self._maxv - self._end
        start  = round(self._start + shift, precision)

        return (start,self._maxv)

    #-------------------------------------------------------------------------


    def PixelsToDuration(self, pixels, width):
        """
        Convert delta period in data units into delta in pixels
        """
        # Verify if width is enough
        if width < 1:
            return 0

        # Convert delta in data units into delta in pixels
        return ((float(pixels) * self.Delta()) / float(width))

