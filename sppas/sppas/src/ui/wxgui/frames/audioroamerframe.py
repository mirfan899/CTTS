# -*- coding: UTF-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    src.wxgui.frames.audioroamerframe.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    GUI management of audio files for SPPAS.

"""
from sppas.src.ui.wxgui.frames.baseframe import ComponentFrame
from sppas.src.ui.wxgui.clients.audioroamerclient import AudioRoamerClient
from sppas.src.ui.wxgui.sp_icons import AUDIOROAMER_APP_ICON

# ----------------------------------------------------------------------------


class AudioRoamerFrame(ComponentFrame):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      AudioRoamer allows to manipulate audio files.

    """
    def __init__(self, parent, appid, prefsIO):

        arguments = {}
        arguments['files'] = []
        arguments['title'] = "SPPAS - AudioRoamer"
        arguments['type']  = "SOUNDFILES"
        arguments['icon']  = AUDIOROAMER_APP_ICON
        arguments['prefs'] = prefsIO

        ComponentFrame.__init__(self, parent, appid, arguments)

    # ------------------------------------------------------------------------

    def CreateClient(self, parent, prefsIO):
        """Override."""

        return AudioRoamerClient(parent, prefsIO)

# ----------------------------------------------------------------------------
