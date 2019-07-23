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

    src.wxgui.views.about.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    GUI frame for displaying information about a software.

"""
import wx

from sppas.src.ui.wxgui.sp_icons import ABOUT_ICON

from sppas.src.ui.wxgui.panels.about import AboutSPPASPanel
from sppas.src.ui.wxgui.panels.about import AboutPluginPanel
from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog

# ----------------------------------------------------------------------------


class AboutSPPASDialog(spBaseDialog):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      Display an about frame for SPPAS software.

    """
    def __init__(self, parent, preferences):
        spBaseDialog.__init__(self, parent, preferences, title="About")
        wx.GetApp().SetAppName("about")

        self.about_panel = AboutSPPASPanel(self, preferences)

        self.LayoutComponents(self.CreateTitle(ABOUT_ICON, "About"),
                              self.about_panel,
                              self.CreateButtonBox([], [self.CreateOkayButton()]))
        self.SetMinSize((520, 580))

# ------------------------------------------------------------------------


class AboutPluginDialog(spBaseDialog):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :summary:      Display an about frame for a plugin.

    """
    def __init__(self, parent, preferences, plugin):
        spBaseDialog.__init__(self, parent, preferences, title="About")
        wx.GetApp().SetAppName("about"+plugin.get_key())

        title_box = self.CreateTitle(ABOUT_ICON, "About")
        content_box = AboutPluginPanel(self, preferences, plugin)
        button_box = self.CreateButtonBox([], [self.CreateOkayButton()])

        self.LayoutComponents(title_box,
                              content_box,
                              button_box)
        self.SetMinSize((520, 580))

# ------------------------------------------------------------------------


def ShowAboutDialog(parent, preferences):
    dialog = AboutSPPASDialog(parent, preferences)
    dialog.ShowModal()
    dialog.Destroy()
