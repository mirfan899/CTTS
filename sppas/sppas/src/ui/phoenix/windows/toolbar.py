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

    src.ui.phoenix.windows.toolbar.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import wx

from .panel import sppasPanel
from .text import sppasStaticText
from .button import BitmapTextButton, TextButton

# ----------------------------------------------------------------------------


class sppasToolbar(sppasPanel):
    """Panel imitating the behaviors of an horizontal toolbar.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    """

    def __init__(self, parent, orient=wx.HORIZONTAL):
        super(sppasToolbar, self).__init__(
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.NO_BORDER | wx.NO_FULL_REPAINT_ON_RESIZE,
            name=wx.PanelNameStr)

        # Focus Color&Style
        self._fs = wx.PENSTYLE_SOLID
        self._fw = 3
        self._fc = wx.Colour(128, 128, 128, 128)

        # List of children with their own style (color, font)
        self.__fg = list()
        self.__ft = list()

        self.SetSizer(wx.BoxSizer(orient))
        self.SetAutoLayout(True)

    # -----------------------------------------------------------------------

    def get_button(self, name):
        """Return the button matching the given name or None.

        :param name: (str) Name of the object
        :returns: (wx.Window) a button or None

        """
        for b in self.GetSizer().GetChildren():
            if b.GetName() == name:
                return b

        return None

    # -----------------------------------------------------------------------

    def AddTextButton(self, name="sppasButton", text="", activated=True):
        """Append a text button into the toolbar.

        :param name: (str) Name of the button
        :param text: (str) Label of the button
        :param activated: (bool) Enable or disable the button

        """
        btn = self.create_button(text, None)
        btn.SetName(name)
        btn.Enable(activated)
        if self.GetSizer().GetOrientation() == wx.HORIZONTAL:
            self.GetSizer().Add(btn, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 1)
        else:
            self.GetSizer().Add(btn, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
        return btn

    # -----------------------------------------------------------------------

    def AddButton(self, icon, text="", activated=True):
        """Append a button into the toolbar.

        The button can contain either:
            - an icon only;
            - an icon with a text.

        :param icon: (str) Name of the .png file of the icon or None
        :param text: (str) Label of the button
        :param activated: (bool) Enable or disable the button

        """
        btn = self.create_button(text, icon)
        btn.Enable(activated)
        if self.GetSizer().GetOrientation() == wx.HORIZONTAL:
            self.GetSizer().Add(btn, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 1)
        else:
            self.GetSizer().Add(btn, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
        return btn

    # -----------------------------------------------------------------------

    def AddSpacer(self, proportion=1):
        """Append a stretch space into the toolbar.

        :param proportion: (int)

        """
        self.GetSizer().AddStretchSpacer(proportion)

    # -----------------------------------------------------------------------

    def AddText(self, text="", color=None):
        """Append a colored static text into the toolbar.

        :param text: (str)
        :param color: (wx.Colour)

        """
        st = sppasStaticText(self, label=text)
        if color is not None:
            st.SetForegroundColour(color)
            self.__fg.append(st)
        self.GetSizer().Add(st, 0, wx.LEFT | wx.TOP | wx.BOTTOM, 6)

    # -----------------------------------------------------------------------

    def AddTitleText(self, text="", color=None):
        """Append a colored static text with an higher font into the toolbar.

        :param text: (str)
        :param color: (wx.Colour)

        """
        st = sppasStaticText(self, label=text)
        st.SetFont(self.__title_font())
        self.__ft.append(st)
        if color is not None:
            st.SetForegroundColour(color)
            self.__fg.append(st)
        self.GetSizer().Add(st, 0, wx.ALL, 6)

    # -----------------------------------------------------------------------

    def set_focus_color(self, value):
        self._fc = value

    def set_focus_penstyle(self, value):
        self._fs = value

    def set_focus_width(self, value):
        self._fw = value

    # -----------------------------------------------------------------------

    def create_button(self, text, icon):
        if icon is not None:
            btn = BitmapTextButton(self, label=text, name=icon)
            btn.LabelPosition = wx.RIGHT

        else:
            btn = TextButton(self, label=text)
            btn.LabelPosition = wx.CENTRE

        btn.FocusStyle = self._fs
        btn.FocusWidth = self._fw
        btn.FocusColour = self._fc
        btn.Spacing = sppasPanel.fix_size(12)
        btn.BorderWidth = 0
        btn.BitmapColour = self.GetForegroundColour()
        btn.SetMinSize((sppasPanel.fix_size(32), sppasPanel.fix_size(32)))

        return btn

    # -----------------------------------------------------------------------

    def SetForegroundColour(self, colour):
        """Override."""
        wx.Panel.SetForegroundColour(self, colour)
        for c in self.GetChildren():
            if c not in self.__fg:
                c.SetForegroundColour(colour)

    # -----------------------------------------------------------------------

    def SetFont(self, font):
        """Override."""
        wx.Panel.SetFont(self, font)
        for c in self.GetChildren():
            if c not in self.__ft:
                c.SetFont(font)

    # -----------------------------------------------------------------------

    def __title_font(self):
        try:  # wx4
            font = wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT)
        except AttributeError:  # wx3
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        s = font.GetPointSize()

        title_font = wx.Font(int(float(s)*1.2),      # point size
                             wx.FONTFAMILY_DEFAULT,  # family,
                             wx.FONTSTYLE_NORMAL,    # style,
                             wx.FONTWEIGHT_BOLD,     # weight,
                             underline=False,
                             faceName="Calibri",
                             encoding=wx.FONTENCODING_SYSTEM)
        return title_font

