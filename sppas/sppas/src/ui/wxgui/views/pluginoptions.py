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
# File: pluginsoptions.py
# ----------------------------------------------------------------------------

import wx
import wx.lib.agw.floatspin

from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.panels.options import sppasOptionsPanel
from sppas.src.ui.wxgui.sp_icons import PLUGINS_ICON

# ----------------------------------------------------------------------------


class spPluginConfig(spBaseDialog):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      develop@sppas.org
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    @summary:      Dialog to configure plugin options.

    """
    def __init__(self, parent, preferences, plugin):
        """
        Constructor.

        :param plugin: (sppasPluginParam)

        """
        spBaseDialog.__init__(self, parent, preferences, title=" - Plugin")
        wx.GetApp().SetAppName("plugin")

        self.preferences = preferences
        self.plugin = plugin
        self.items = []
        self._options_key = []

        self.LayoutComponents(self._create_title(),
                              self._create_content(),
                              self._create_buttons())

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_title(self):
        return self.CreateTitle(PLUGINS_ICON, self.plugin.get_name())

    def _create_content(self):
        all_options = self.plugin.get_options()  #.values()
        selected_options = []
        for option in all_options:
            if option.get_key() != "input" and option.get_value() != "input":
                self._options_key.append(option.get_key())
                selected_options.append(option)

        options_panel = sppasOptionsPanel(self, self.preferences, selected_options)
        options_panel.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))
        options_panel.SetForegroundColour(self.preferences.GetValue('M_FG_COLOUR'))
        options_panel.SetFont(self.preferences.GetValue('M_FONT'))
        self.items = options_panel.GetItems()
        return options_panel

    def _create_buttons(self):
        btn_save = self.CreateSaveButton("Save the plugin configuration.")
        btn_cancel = self.CreateCancelButton()
        btn_okay = self.CreateOkayButton()
        self.Bind(wx.EVT_BUTTON, self._on_save, btn_save)
        self.Bind(wx.EVT_BUTTON, self._on_okay, btn_okay)
        return self.CreateButtonBox([btn_save], [btn_cancel, btn_okay])

    # ------------------------------------------------------------------------
    # Callbacks to events
    # ------------------------------------------------------------------------

    def _on_save(self, evt):
        """Save the content in a text file."""

        self.__set_items()
        self.plugin.save()

    # ------------------------------------------------------------------------

    def _on_okay(self, evt):
        """Set the list of "Option" instances to the plugin."""

        self.__set_items()
        evt.Skip()

    # ------------------------------------------------------------------------

    def __set_items(self):
        """Set the list of "Option" instances to the plugin."""

        for i, item in enumerate(self.items):
            new_value = item.GetValue()
            key = self._options_key[i]
            option = self.plugin.get_option_from_key(key)
            option.set_value(str(new_value))
