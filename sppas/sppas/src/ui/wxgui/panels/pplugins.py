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
# File: pplugins.py
# ----------------------------------------------------------------------------

import logging
import wx
import wx.lib.scrolledpanel
import wx.lib.newevent
import os

from sppas.src.plugins.manager import sppasPluginsManager

from sppas.src.ui.wxgui.sp_icons import PLUGIN_IMPORT_ICON, PLUGIN_REMOVE_ICON
from sppas.src.ui.wxgui.sp_consts import ID_FILES

from sppas.src.ui.wxgui.panels.buttons import ButtonPanel
from sppas.src.ui.wxgui.panels.mainbuttons import MainToolbarPanel
from sppas.src.ui.wxgui.dialogs.msgdialogs import ShowInformation
from sppas.src.ui.wxgui.dialogs.msgdialogs import Choice
from sppas.src.ui.wxgui.dialogs.filedialogs import OpenSpecificFiles
from sppas.src.ui.wxgui.views.about import AboutPluginDialog
from sppas.src.ui.wxgui.views.pluginoptions import spPluginConfig
from sppas.src.ui.wxgui.views.processprogress import ProcessProgressDialog

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

IMPORT_ID = wx.NewId()
REMOVE_ID = wx.NewId()

PluginApplyEvent, spEVT_PLUGIN_APPLY = wx.lib.newevent.NewEvent()
PluginApplyCommandEvent, spEVT_PLUGIN_APPLY_COMMAND = wx.lib.newevent.NewCommandEvent()

PluginReadmeEvent, spEVT_PLUGIN_README = wx.lib.newevent.NewEvent()
PluginReadmeCommandEvent, spEVT_PLUGIN_README_COMMAND = wx.lib.newevent.NewCommandEvent()

# ----------------------------------------------------------------------------


class PluginsPanel(wx.Panel):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      Main panel to work with SPPAS plugin.

    """
    def __init__(self, parent, preferences):

        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.SetBackgroundColour(preferences.GetValue('M_BG_COLOUR'))
        self._preferences = preferences

        try:
            self._manager = sppasPluginsManager()
        except Exception as e:
            self._manager = None
            logging.info('%s' % str(e))
            ShowInformation(self, preferences, "%s" % str(e), style=wx.ICON_ERROR)

        self._toolbar = self._create_toolbar()
        self._plugins_panel = PluginsListPanel(self, preferences)
        if self._manager is not None:
            for plugin_id in self._manager.get_plugin_ids():
                plugin = self._manager.get_plugin(plugin_id)
                self._plugins_panel.Append(plugin)

        _vbox = wx.BoxSizer(wx.VERTICAL)
        _vbox.Add(self._toolbar, proportion=0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=4)
        _vbox.Add(self._plugins_panel, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=4)

        self.Bind(wx.EVT_BUTTON, self.ProcessEvent)
        self.Bind(spEVT_PLUGIN_APPLY, self.OnApply)
        self.Bind(spEVT_PLUGIN_README, self.OnReadme)

        self.SetSizerAndFit(_vbox)

    # -----------------------------------------------------------------------

    def _create_toolbar(self):
        """Creates a toolbar panel."""

        activated = True
        if self._manager is None:
            activated = False

        toolbar = MainToolbarPanel(self, self._preferences)
        toolbar.AddSpacer()
        toolbar.AddButton(IMPORT_ID, PLUGIN_IMPORT_ICON, 'Install',
                          tooltip="Install a plugin in SPPAS plugins directory.",
                          activated=activated)
        toolbar.AddButton(REMOVE_ID, PLUGIN_REMOVE_ICON, 'Delete',
                          tooltip="Delete a plugin of SPPAS plugins directory.",
                          activated=activated)
        toolbar.AddSpacer()
        return toolbar

    # -----------------------------------------------------------------------

    def ProcessEvent(self, event):
        """
        Processes an event, searching event tables and calling zero or more
        suitable event handler function(s).  Note that the ProcessEvent
        method is called from the wxPython docview framework directly since
        wxPython does not have a virtual ProcessEvent function.

        """
        ide = event.GetId()

        if ide == IMPORT_ID:
            self.Import()
            return True
        elif ide == REMOVE_ID:
            self.Remove()
            return True

        return wx.GetApp().ProcessEvent(event)

    # -----------------------------------------------------------------------

    def Import(self):
        """Import and install a plugin."""

        filename = OpenSpecificFiles("Plugin archive", ['zip', "*.zip", "*.[zZ][iI][pP]"])
        if len(filename) > 0:
            try:
                # fix a name for the plugin directory
                plugin_folder = os.path.splitext(os.path.basename(filename))[0]
                plugin_folder.replace(' ', "_")

                # install the plugin.
                plugin_id = self._manager.install(filename, plugin_folder)

                ShowInformation( self, self._preferences,
                                 "Plugin %s successfully installed in %s folder." % (plugin_id, plugin_folder),
                                 style=wx.ICON_INFORMATION)

                self._plugins_panel.Append(self._manager.get_plugin(plugin_id))
                self._plugins_panel.Layout()
                self._plugins_panel.Refresh()

            except Exception as e:
                logging.info('%s' % str(e))
                ShowInformation(self, self._preferences, "%s" % str(e), style=wx.ICON_ERROR)

    # -----------------------------------------------------------------------

    def Remove(self):
        """Remove and delete a plugin."""

        try:
            plugin_id = self._plugins_panel.Remove()
            if plugin_id is not None:
                self._manager.delete(plugin_id)

                ShowInformation(self, self._preferences,
                                "Plugin %s was successfully deleted." % plugin_id,
                                style=wx.ICON_INFORMATION)

        except Exception as e:
            logging.info('%s' % str(e))
            ShowInformation(self, self._preferences, "%s" % str(e), style=wx.ICON_ERROR)

    # -----------------------------------------------------------------------

    def OnApply(self, event):
        """A plugin was clicked: Apply it on a set of files.

        :param event: (PluginApplyEvent) Event indicating the identifier of
        the plugin to apply.

        """
        # Get the list of files (from the main frame).
        trs_files = self.GetTopLevelParent().GetTrsSelection()
        audio_files = self.GetTopLevelParent().GetAudioSelection()
        file_names = trs_files + audio_files
        if len(file_names) == 0:
            ShowInformation(self, self._preferences,
                            "No file(s) selected to apply a plugin!",
                            style=wx.ICON_WARNING)
            return

        # Set the options of the plugin
        plugin_id = event.pid
        logging.debug("Apply plugin %s on %d files." % (plugin_id, len(file_names)))
        dlg = spPluginConfig(self, self._preferences,
                             self._manager.get_plugin(plugin_id))
        res = dlg.ShowModal()

        # OK... now execute the plugin.
        if res == wx.ID_OK:
            log_text = ""
            style = wx.ICON_INFORMATION

            try:
                wx.BeginBusyCursor()
                p = ProcessProgressDialog(self, self._preferences, "Plugin %s is processing..." % plugin_id)
                self._manager.set_progress(p)
                log_text = self._manager.run_plugin(plugin_id, file_names)
                p.close()
                wx.EndBusyCursor()

                if len(log_text) == 0:
                    log_text = "Done."

            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.info('%s' % str(e))
                log_text = str(e)
                style = wx.ICON_ERROR

            # Show the output message
            ShowInformation(self, self._preferences, log_text, style=style)

        dlg.Destroy()

        # Update the filetree of the main frame
        evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, ID_FILES)
        evt.SetEventObject(self)
        wx.PostEvent(self.GetTopLevelParent(), evt)

    # -----------------------------------------------------------------------

    def OnReadme(self, event):
        """A plugin was clicked: Display the README.txt file content.

        :param event: (PluginReadmeEvent) Event indicating the identifier of
        the plugin to read.

        """
        dialog = AboutPluginDialog(self, self._preferences, self._manager.get_plugin(event.pid))
        dialog.ShowModal()
        dialog.Destroy()

# ---------------------------------------------------------------------------


class PluginsListPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      List of buttons to call a plugin.

    """
    def __init__(self, parent, preferences):
        """Constructor.

        :param parent:
        :param preferences:

        """
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        self.SetBackgroundColour(preferences.GetValue('M_BG_COLOUR'))

        self._preferences = preferences
        self._plugins = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick)
        self.SetAutoLayout(True)
        self.Layout()
        self.SetupScrolling()

    # -----------------------------------------------------------------------

    def Append(self, plugin):
        """Append a plugin into the panel.

        :param plugin (sppasPluginParam) The plugin to append

        """
        plugin_id = plugin.get_key()

        # Create the button
        button_id = wx.NewId()
        button_icon = os.path.join(plugin.get_directory(), plugin.get_icon())
        button = ButtonPanel(self, button_id, self._preferences, button_icon, plugin_id, activated=True)

        # Create a description with the plugin name and its description.
        p = wx.Panel(self, -1)
        p.SetBackgroundColour(self._preferences.GetValue('M_BG_COLOUR'))

        n = plugin.get_name()
        if len(n) == 0:
            n = "Unknown plugin name"
        txt_name = wx.TextCtrl(p, wx.ID_ANY, value=n, style=wx.TE_READONLY | wx.NO_BORDER)
        self.__apply_preferences(txt_name)
        font = self._preferences.GetValue('M_FONT')
        font.SetWeight(wx.BOLD)
        txt_name.SetFont(font)

        d = plugin.get_descr()
        if len(d) == 0:
            d = "No description available."
        txt_descr = wx.TextCtrl(p, wx.ID_ANY,
                                value=d,
                                style=wx.TE_READONLY | wx.TE_MULTILINE | wx.NO_BORDER | wx.TE_WORDWRAP | wx.TE_NO_VSCROLL)
        self.__apply_preferences(txt_descr)

        txt_readme = wx.StaticText(p, -1, "About...")
        self.__apply_preferences(txt_readme)
        txt_readme.SetForegroundColour(wx.Colour(80, 100, 220))
        txt_readme.Bind(wx.EVT_LEFT_UP, self.OnReadme)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(txt_name, proportion=0, flag=wx.LEFT | wx.EXPAND, border=2)
        s.Add(txt_readme, proportion=0, flag=wx.LEFT | wx.BOTTOM, border=2)
        s.Add(txt_descr, proportion=1, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=2)
        p.SetSizerAndFit(s)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(button, proportion=0, flag=wx.ALL, border=4)
        box.Add(p, proportion=1, flag=wx.ALL | wx.EXPAND, border=4)

        # Add to the main sizer
        self.GetSizer().Add(box, flag=wx.ALL | wx.EXPAND, border=0)
        self._plugins[plugin_id] = (button_id, box, txt_readme)

        self.Layout()
        self.Refresh()

    # -----------------------------------------------------------------------

    def Remove(self):
        """Ask for the plugin to be removed, remove of the list.

        :returns: plugin identifier of the plugin to be deleted.

        """
        plugin_id = None
        dlg = Choice(self, self._preferences, "Choose the plugin to delete:",
                     self._plugins.keys())
        if dlg.ShowModal() == wx.ID_OK:
            plugin_idx = dlg.GetSelection()
            plugin_id = self._plugins.keys()[plugin_idx]
            plugin_box = self._plugins[plugin_id][1]
            sizer = self.GetSizer()
            sizer.Hide(plugin_box)
            sizer.Remove(plugin_box)
            del self._plugins[plugin_id]
        dlg.Destroy()
        self.Layout()
        self.Refresh()

        return plugin_id

    # -----------------------------------------------------------------------
    # Callback to events
    # -----------------------------------------------------------------------

    def OnButtonClick(self, evt):
        """A plugin has been clicked: send the plugin identifier to the parent.

        :param evt: (wx event)

        """
        obj = evt.GetEventObject()
        button_id = obj.GetId()

        for p in self._plugins.keys():
            if button_id == self._plugins[p][0]:
                evt = PluginApplyEvent(pid=p)
                evt.SetEventObject(self)
                wx.PostEvent(self.GetParent(), evt)
                break

    # ------------------------------------------------------------------------

    def OnReadme(self, evt):
        """The About text was clicked.
        Send the information to the parent.

        """
        obj = evt.GetEventObject()
        for p in self._plugins.keys():
            if obj == self._plugins[p][2]:
                evt = PluginReadmeEvent(pid=p)
                evt.SetEventObject(self)
                wx.PostEvent(self.GetParent(), evt)
                break

    # ------------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------------

    def __apply_preferences(self, wx_object):
        """Set font, background color and foreground color to an object."""

        wx_object.SetFont(self._preferences.GetValue('M_FONT'))
        wx_object.SetForegroundColour(self._preferences.GetValue('M_FG_COLOUR'))
        wx_object.SetBackgroundColour(self._preferences.GetValue('M_BG_COLOUR'))
