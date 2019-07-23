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

    src.wxgui.structs.prefs.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Management of the user' preferences.

"""
import codecs
import pickle

from sppas.src.ui.wxgui.structs.wxoption import sppasWxOption
from .theme import sppasTheme

# ----------------------------------------------------------------------------


class Preferences(object):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      Management of a dictionary of settings.

    """
    def __init__(self, theme=None):
        """Creates a dict of sppasWxOption() instances, with option id as key."""

        self._prefs = {}

        # Set the requested theme.
        if theme is None:
            self.SetTheme(sppasTheme())
        else:
            self.SetTheme(theme)

    # ------------------------------------------------------------------------
    # Getters and Setters
    # ------------------------------------------------------------------------

    def GetValue(self, key):
        """Return the typed-value of the given key."""

        return self._prefs[key].get_value()

    # ------------------------------------------------------------------------

    def SetValue(self, key, t=None, v=None, text=''):
        """Set a new couple key/(type,typed-value,text)."""

        if key not in self._prefs:
            self._prefs[key] = sppasWxOption(t, v, text)

        self._prefs[key].set_value(v)

    # ------------------------------------------------------------------------

    def SetOption(self, key, option):
        """Set a new couple key/Option."""

        self._prefs[key] = option

    # ------------------------------------------------------------------------

    def GetTheme(self):
        """Return the the current theme."""

        return self._prefs.get('THEME', None)

    # ------------------------------------------------------------------------

    def SetTheme(self, theme):
        """Set a new theme."""

        self._prefs['THEME'] = theme
        for key in theme.get_keys():
            opt = theme.get_choice(key)
            if opt is not None:
                self.SetOption(key, opt)

# ----------------------------------------------------------------------------


class Preferences_IO(Preferences):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    :summary:      Preferences with I/O extended features.

    """
    def __init__(self, filename=None):
        """Create a new dictionary of preferences."""

        Preferences.__init__(self)
        self._filename = filename

    # ------------------------------------------------------------------------

    def HasFilename(self):
        """Return True is a file name was defined."""

        if self._filename is None:
            return False
        return True

    # ------------------------------------------------------------------------

    def Read(self):
        """Read user preferences from a file.
        Return True if preferences have been read.

        :returns: boolean

        """
        try:
            with codecs.open(self._filename, mode="rb") as f:
                prefs = pickle.load(f)
        except Exception:
            return False

        self._prefs = prefs
        return True

    # ------------------------------------------------------------------------

    def Write(self):
        """Save user preferences into a file.
        Return True if preferences have been saved.

        :returns: boolean

        """
        if self._filename is None:
            return False

        try:
            with codecs.open(self._filename, mode="wb") as f:
                pickle.dump(self._prefs, f, pickle.HIGHEST_PROTOCOL)
        except Exception:
            return False

        return True

    # ------------------------------------------------------------------------

    def Copy(self):
        """Return a deep copy of self.

        :returns: (Preferences_IO)

        """
        #import copy
        #return copy.deepcopy( self._prefs ) -->
        #BUG: TypeError: object.__new__(PySwigObject) is not safe, use PySwigObject.__new__()

        cpref = Preferences_IO()

        for key in self._prefs.keys():
            if key == 'THEME':
                cpref.SetTheme(self._prefs[key])
            else:
                t = self._prefs[key].get_type()
                v = self._prefs[key].get_untypedvalue()
                txt = self._prefs[key].get_text()
                opt = sppasWxOption(t, v, txt)
                cpref.SetOption(key, opt)

        return cpref

# ----------------------------------------------------------------------------
