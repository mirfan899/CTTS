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
# File: basestats.py
# ---------------------------------------------------------------------------
import wx
import codecs

# ------------------------------------------------------------------------


def writecsv(filename, rows, separator="\t", encoding="utf-8-sig"):
    """Write the rows to the file.
    Args:
        filename (string):
        rows (list):
        separator (string):
        encoding (string):

    """
    with codecs.open(filename, "w+", encoding) as f:
        for row in rows:
            tmp = []
            for s in row:
                if isinstance(s, (float, int)):
                    s = str(s)
                else:
                    s = '"%s"' % s
                tmp.append(s)
            f.write('%s\n' % separator.join(tmp))


# ----------------------------------------------------------------------------
# Base Stat Panel
# ----------------------------------------------------------------------------


class BaseStatPanel( wx.Panel ):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL
    @summary: Base stat panel.

    """

    def __init__(self, parent, prefsIO, name):

        wx.Panel.__init__(self, parent)

        self.preferences = prefsIO
        self.name = name.lower()
        self.rowdata = []

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.ShowNothing()
        self.sizer.FitInside(self)
        self.SetMinSize((320,200))

    # ------------------------------------------------------------------------

    def ShowNothing(self):
        """
        Method to show a message in the panel.

        """
        self.sizer.DeleteWindows()
        self.sizer.Add(wx.StaticText(self, -1, "Nothing to view!"), 1, flag=wx.ALL|wx.EXPAND, border=5)
        self.SendSizeEvent()

    # ------------------------------------------------------------------------

    def ShowStats(self, tier):
        """
        Base method to show a tier in the panel.

        """
        self.ShowNothing()

    # ------------------------------------------------------------------------

    def SaveAs(self, outfilename="stats.csv"):
        dlg = wx.FileDialog(self,
                           "Save as",
                           "Save as",
                           outfilename,
                           "UTF-16 (*.csv)|*.csv |UTF-8 (*.csv)|*.csv",
                           wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return

        path, index = dlg.GetPath(), dlg.GetFilterIndex()
        dlg.Destroy()
        encoding = "utf-16" if index == 0 else "utf-8"

        self.rowdata.insert(0, self.cols)
        writecsv(path, self.rowdata, separator=";", encoding=encoding)
        self.rowdata.pop(0)

    # ------------------------------------------------------------------------

    def AppendRow(self, i, row, listctrl):
        # append the row in the list
        pos = self.statctrl.InsertStringItem(i, row[0])
        for j in range(1,len(row)):
            s = row[j]
            if isinstance(s, float):
                s = str(round(s,4))
            elif isinstance(s, int):
                s = str(s)
            listctrl.SetStringItem(pos, j, s)

