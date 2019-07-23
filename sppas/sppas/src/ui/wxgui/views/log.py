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

    src.wxgui.views.log.py
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import os.path
import shutil
import codecs
import wx

from sppas.src.config import sg
from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.dialogs.msgdialogs import ShowInformation
from sppas.src.ui.wxgui.sp_icons import REPORT_ICON
from sppas.src.ui.wxgui.sp_consts import ERROR_COLOUR
from sppas.src.ui.wxgui.sp_consts import INFO_COLOUR
from sppas.src.ui.wxgui.sp_consts import IGNORE_COLOUR
from sppas.src.ui.wxgui.sp_consts import WARNING_COLOUR
from sppas.src.ui.wxgui.sp_consts import OK_COLOUR


# ----------------------------------------------------------------------------


class LogDialog(spBaseDialog):
    """Dialog to show/save the log file of automatic annotations.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018 Brigitte Bigi

    """
    def __init__(self, parent, preferences, filename):
        """Dialog constructor.

        :param parent: is the parent wx object.
        :param preferences: (Preferences)
        :param filename: (str) the file to display in this frame.

        """
        spBaseDialog.__init__(self, parent, preferences, title=" - Report")
        wx.GetApp().SetAppName("log")

        self.preferences = preferences
        self.filename = filename

        titlebox = self.CreateTitle(REPORT_ICON, "Procedure outcome report")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                               contentbox,
                               buttonbox)

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        self.btn_save = self.CreateSaveButton("Save the procedure outcome report.")
        btn_close = self.CreateCloseButton()
        self.Bind(wx.EVT_BUTTON, self._on_save, self.btn_save)
        return self.CreateButtonBox([self.btn_save], [btn_close])

    def _create_content(self):
        try:
            with codecs.open(self.filename, 'r', sg.__encoding__) as fp:
                logcontent = fp.read()
        except Exception as e:
            logcontent = "No report is available...\n" \
                         "Probably you don't have permission to write in the directory. " \
                         "Change the access rights to solve the problem.\n" \
                         "Error is: %s" % str(e)
            self.btn_save.Enable(False)

        self.log_txt = wx.TextCtrl(self, -1, size=(620, 480),
                                   style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL)
        self.log_txt.SetDefaultStyle(wx.TextAttr(wx.BLACK, wx.WHITE))
        fs = self.preferences.GetValue('M_FONT').GetPointSize()
        self.log_txt.SetFont(wx.Font(fs,
                                     wx.SWISS, 
                                     wx.NORMAL, 
                                     wx.NORMAL, 
                                     False, 
                                     u'Courier New'))
        self.log_txt.SetValue(logcontent)
        i = 0
        oldi = 0
        while i >= 0:
            i = logcontent.find("[ ", oldi)
            if logcontent.find("OK", i, i+14) > -1:
                self.log_txt.SetStyle(i, i+12, wx.TextAttr(OK_COLOUR))

            elif logcontent.find("ERROR", i, i+14) > -1:
                self.log_txt.SetStyle(i, i+12, wx.TextAttr(ERROR_COLOUR))

            elif logcontent.find("WARNING", i, i+14) > -1:
                self.log_txt.SetStyle(i, i+12, wx.TextAttr(WARNING_COLOUR))

            elif logcontent.find("INFO", i, i+14) > -1:
                self.log_txt.SetStyle(i, i+12, wx.TextAttr(INFO_COLOUR))

            elif logcontent.find("IGNORED", i, i+14) >- 1:
                self.log_txt.SetStyle(i, i+12, wx.TextAttr(IGNORE_COLOUR))

            oldi = i + 13

        return self.log_txt

    # ------------------------------------------------------------------------
    # Callbacks to events
    # ------------------------------------------------------------------------

    def _on_save(self, evt):
        """
        Save the content in a text file.
        """
        filesel = None
        wildcard = "SPPAS log files (*_log*.txt)|sppas*.txt"
        defaultDir = os.path.dirname(self.filename)
        defaultFile = os.path.basename(self.filename)

        dlg = wx.FileDialog(
            self, message="Save as...",
            defaultDir=defaultDir,
            defaultFile=defaultFile,
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR
           )

        # Show the dialog and retrieve the user response.
        # If it is the OK response, process the data.
        if dlg.ShowModal() == wx.ID_OK:
            filesel = dlg.GetPath()
        dlg.Destroy()

        if filesel:
            # OK. We have a filename...
            # but if this is the default, don't do anything!
            if self.filename == filesel:
                return
            # or copy the file!
            try:
                shutil.copy(self.filename, filesel)
            # eg. src and dest are the same file
            except shutil.Error as e:
                ShowInformation(self, self.preferences,
                                "Error while saving: %s" % str(e), wx.ICON_ERROR)
            # eg. source or destination doesn't exist
            except IOError as e:
                ShowInformation(self, self.preferences,
                                "Error while saving: %s" % str(e), wx.ICON_ERROR)

# ----------------------------------------------------------------------------


def ShowLogDialog(parent, preferences, filename):
    dialog = LogDialog(parent, preferences, filename)
    dialog.ShowModal()
    dialog.Destroy()

# ---------------------------------------------------------------------------


if __name__ == "__main__":
    app = wx.PySimpleApp()
    ShowLogDialog(None, None, filename="log.py")
    app.MainLoop()
