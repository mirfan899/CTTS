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
# File: sp_images.py
# ----------------------------------------------------------------------------

import os.path
from sppas.src.config import paths

# ----------------------------------------------------------------------------

IMAGES_PATH = os.path.join(paths.etc, "images")

# ----------------------------------------------------------------------------

WIZARD_WELCOME_MAIN_BMP = os.path.join(IMAGES_PATH, "wizard-display.bmp")
WIZARD_WELCOME_SCROLL_BMP = os.path.join(IMAGES_PATH, "wizard-scroll.bmp")
WIZARD_WELCOME_SOUND_BMP = os.path.join(IMAGES_PATH, "wizard-sound.bmp")
WIZARD_WELCOME_TRS_BMP = os.path.join(IMAGES_PATH, "wizard-trs.bmp")
WIZARD_WELCOME_ZOOM_BMP = os.path.join(IMAGES_PATH, "wizard-zoom.bmp")

WIZARD_SCROLL_PANEL_BMP = os.path.join(IMAGES_PATH, "scroll-panel.png")
WIZARD_ZOOM_PANEL_BMP = os.path.join(IMAGES_PATH, "zoom-panel.png")
WIZARD_ZOOM_KEYBOARD_BMP = os.path.join(IMAGES_PATH, "keyboard-zoom.png")
WIZARD_ZOOM_MOUSE_BMP = os.path.join(IMAGES_PATH, "keyboard-mouse-zoom.png")

# PlayerBoard
PLAYER_BACKGROUND = os.path.join(IMAGES_PATH, "music.jpg")
