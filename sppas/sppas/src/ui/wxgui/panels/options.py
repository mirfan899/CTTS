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
# File: options.py
# ----------------------------------------------------------------------------

import os
import wx.lib.scrolledpanel

from sppas.src.ui.wxgui.cutils.imageutils  import spBitmap
from sppas.src.ui.wxgui.cutils.dialogutils import create_wildcard

from sppas.src.ui.wxgui.sp_icons import TREE_FOLDER_OPEN

# ----------------------------------------------------------------------------


class sppasOptionsPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      develop@sppas.org
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    @summary:      Create dynamically a panel depending on a list of options.

    """
    def __init__(self, parent, preferences, options):
        """
        Constructor.

        :param options: (list) List of "Option" instances.

        """
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self._preferences = preferences

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # wx objects to fill option values
        self._items = []
        self.file_buttons = {}

        for opt in options:
            self.AppendOption(opt)

        self.SetMinSize((320, 180))
        self.Fit()
        self.SetupScrolling()

    # ------------------------------------------------------------------------

    def AppendOption(self, opt):
        """
        Append an option in the panel.

        :param opt: an "Option" to append to the bottom of the panel.

        """
        if opt.get_type() == "bool":
            self.__add_bool(opt.get_text(), value=opt.get_value())

        elif opt.get_type() == "int":
            self.__add_int(opt.get_text(), value=opt.get_value())

        elif opt.get_type() == "float":
            self.__add_float(opt.get_text(), value=opt.get_value())

        elif opt.get_type().startswith("file"):
            self.__add_file(opt.get_text(), opt.get_value(), opt.get_type())

        else:  # if opt.get_type() == "str":
            self.__add_text(opt.get_text(), value=opt.get_value())

    # ------------------------------------------------------------------------

    def GetItems(self):
        """
        Return the objects created from the given options.

        :returns: wx objects

        """
        return self._items

    # ------------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------------

    def __apply_preferences(self, wx_object):
        """Set font, background color and foreground color to an object."""

        font = self._preferences.GetValue('M_FONT')
        wx_object.SetFont(font)
        wx_object.SetForegroundColour(self._preferences.GetValue('M_FG_COLOUR'))
        wx_object.SetBackgroundColour(self._preferences.GetValue('M_BG_COLOUR'))

    # ------------------------------------------------------------------------

    def __add_bool(self, label, value=True):
        """
        Add a checkbox to the panel.

        :param label: (string) the description of the value
        :param value: (boolean) the current value

        """
        cb = wx.CheckBox(self, -1, label)
        cb.SetValue(value)
        self.__apply_preferences(cb)
        self.GetSizer().Add(cb, 0, wx.BOTTOM, 8)

        self._items.append(cb)

    # ------------------------------------------------------------------------

    def __add_int(self, label, smin=0, smax=2000, value=1, width=130):
        """
        Add a spinner to the panel.

        :param label: (string) the description of the value
        :param smin: (int) the minimum value
        :param smax: (int) the maximum value
        :param value: (int) the current value

        """
        st = wx.StaticText(self, -1, label)
        self.__apply_preferences(st)

        sc = wx.SpinCtrl(self, -1, label, (30, 20), (width, -1))
        sc.SetRange(smin, smax)
        sc.SetValue(value)
        self.__apply_preferences(sc)

        self.GetSizer().Add(st, 0, wx.LEFT, 3)
        self.GetSizer().Add(sc, 0, wx.BOTTOM, 8)

        self._items.append(sc)

    # ------------------------------------------------------------------------

    def __add_float(self, label, smin=0, smax=2000, incr=0.01, value=1.0, width=130):
        """
        Add a float spinner to the panel.

        :param label: (string) the description of the value
        :param smin: (float) the minimum value
        :param smax: (float) the maximum value
        :param incr: (float) increment for every evt_floatspin events
        :param value: (float) the current value

        """
        st = wx.StaticText(self, -1, label)
        self.__apply_preferences(st)

        fsc = wx.lib.agw.floatspin.FloatSpin(self, -1, size=(width, -1), increment=incr, digits=3)
        fsc.SetRange(smin, smax)
        fsc.SetValue(value)
        self.__apply_preferences(fsc)

        self.GetSizer().Add(st, 0, wx.LEFT, 3)
        self.GetSizer().Add(fsc, 0, wx.BOTTOM, 8)

        self._items.append(fsc)

    # ------------------------------------------------------------------------

    def __add_text(self, label, value=""):
        """
        Add a TextCtrl to the panel.

        :param label: (string) the description of the value
        :param value: (string) the current value

        """
        st = wx.StaticText(self, -1, label)
        self.__apply_preferences(st)

        textctrl = wx.TextCtrl(self, -1, size=(300, -1))
        textctrl.SetValue(value)
        self.__apply_preferences(textctrl)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textctrl)

        self.GetSizer().Add(st, 0, wx.LEFT, 8)
        self.GetSizer().Add(sizer, 0, wx.BOTTOM, 8)

        self._items.append(textctrl)

    # ------------------------------------------------------------------------

    def __add_file(self, label, value, opt_type):
        """
        Add a TextCtrl to the panel.

        :param label: (string) the description of the value
        :param value: (string) the current value

        """
        st = wx.StaticText(self, -1, label)
        self.__apply_preferences(st)

        filetext = wx.TextCtrl(self, -1, size=(300, -1))
        filetext.SetValue(value)
        self.__apply_preferences(filetext)

        filebtn = wx.BitmapButton(self, bitmap=spBitmap(TREE_FOLDER_OPEN, 16, theme=self._preferences.GetValue('M_ICON_THEME')), style=wx.NO_BORDER)
        if opt_type == "filepath":
            filebtn.Bind(wx.EVT_BUTTON, self.__on_text_filepath)
        else:
            filebtn.Bind(wx.EVT_BUTTON, self.__on_text_filename)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(filetext, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(filebtn, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=5)

        self.GetSizer().Add(st, 0, wx.BOTTOM, 8)
        self.GetSizer().Add(sizer, 0, wx.BOTTOM, 8)

        self.file_buttons[filebtn] = filetext
        self._items.append(filetext)

    # ------------------------------------------------------------------------

    def __on_text_filepath(self, event):

        dlg = wx.DirDialog(self, message="Choose a directory", defaultPath=os.getcwd())
        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetPath()
            btn_obj = event.GetEventObject()
            obj = self.file_buttons[btn_obj]
            obj.SetValue(directory)
            obj.SetFocus()
            obj.Refresh()

        dlg.Destroy()

    # ------------------------------------------------------------------------

    def __on_text_filename(self, event):

        wildcard = create_wildcard("All files", ['*', '*.*'])
        dlg = wx.FileDialog(None, "Select a file", os.getcwd(), "", wildcard,
                            wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            btn_obj = event.GetEventObject()
            obj = self.file_buttons[btn_obj]
            obj.SetValue(filename)
            obj.SetFocus()
            obj.Refresh()

        dlg.Destroy()

    # ------------------------------------------------------------------------
