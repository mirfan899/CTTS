# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              the automatic
#           \__   |__/  |__/  |___| \__             annotation and
#              \  |     |     |   |    \             analysis
#           ___/  |     |     |   | ___/              of speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2017  Brigitte Bigi
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
# File: wxgui.sp_consts.py
# ----------------------------------------------------------------------------

import os.path
import wx

from sppas.src.config import paths, sg

# ---------------------------------------------------------------------------
# Define all paths (relatively to SPPAS base path)
# ---------------------------------------------------------------------------

PREFS_FILE = os.path.join(paths.etc, "sppas.prefs")


# ---------------------------------------------------------------------------
# Base components:

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE|wx.CLOSE_BOX
FRAME_TITLE = " " + sg.__name__ + " " + sg.__version__ + " "
DIALOG_STYLE = wx.CAPTION|wx.RESIZE_BORDER

DEFAULT_APP_NAME = sg.__name__ + "Component"


# ---------------------------------------------------------------------------
# GUI design.

ERROR_COLOUR = wx.Colour(220, 30, 10)     # red
INFO_COLOUR = wx.Colour(55, 30, 200)      # blue
IGNORE_COLOUR = wx.Colour(140, 100, 160)  # gray-violet
WARNING_COLOUR = wx.Colour(240, 190, 45)  # orange
OK_COLOUR = wx.Colour(25, 160, 50)        # green

# ---------------------------------------------------------------------------
# GUI design.

MIN_PANEL_W = 180
MIN_PANEL_H = 220

MIN_FRAME_W = 720
MIN_FRAME_H = 540

# ----------------------------------------------------------------------------

ID_ANNOTATIONS = wx.NewId()
ID_COMPONENTS = wx.NewId()
ID_PLUGINS = wx.NewId()
ID_ACTIONS = wx.NewId()
ID_FILES = wx.NewId()

ID_EXT_BUG = wx.NewId()
ID_EXT_HOME = wx.NewId()
ID_FEEDBACK = wx.NewId()

ID_FRAME_DATAROAMER = wx.NewId()
ID_FRAME_SNDROAMER = wx.NewId()
ID_FRAME_IPUSCRIBE = wx.NewId()
ID_FRAME_SPPASEDIT = wx.NewId()
ID_FRAME_STATISTICS = wx.NewId()
ID_FRAME_DATAFILTER = wx.NewId()
