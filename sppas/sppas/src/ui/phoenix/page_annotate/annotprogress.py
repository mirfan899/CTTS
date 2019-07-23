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

    ui.phoenix.page_annotate.annotprogress.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import wx
import time
import logging

from sppas.src.ui.progress import sppasBaseProgress
from sppas.src.ui.cfg import sppasAppConfig

from sppas.src.ui.phoenix.main_settings import WxAppSettings
from sppas.src.ui.phoenix.windows import sppasDialog
from sppas.src.ui.phoenix.windows import sppasPanel
from sppas.src.ui.phoenix.windows import sppasStaticText

# ---------------------------------------------------------------------------


class sppasAnnotProgressDialog(sppasDialog, sppasBaseProgress):
    """Progress dialog for the annotations.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    """

    def __init__(self):
        """Create a dialog with a progress for the annotations."""
        super(sppasAnnotProgressDialog, self).__init__(parent=None)

        self.SetTitle("Automatic annotations")
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP | wx.DIALOG_NO_PARENT)
        self.SetName("annot_progress_dialog")
        self._create_content()

        # Fix frame properties
        self.SetMinSize(wx.Size(sppasDialog.fix_size(400),
                                sppasDialog.fix_size(128)))
        self.LayoutComponents()
        self.CenterOnParent()
        self.GetSizer().Fit(self)
        self.Raise()
        self.SetFocus()
        self.Show(True)

    # -----------------------------------------------------------------------

    def _create_content(self):
        """Create the content of the progress dialog."""
        panel = sppasPanel(self, name="content")

        # an header text used to print the annotation step
        self.header = sppasStaticText(panel, label="HEADER IS HERE", style=wx.ALIGN_CENTRE)
        # the gauge
        self.gauge = wx.Gauge(panel, range=100, size=(400, 24))
        # a bottom text used to print the current file name
        self.text = sppasStaticText(panel, label="BOTTOM IS HERE", style=wx.ALIGN_CENTRE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer.Add(self.gauge, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer.Add(self.text, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)

        panel.SetSizer(sizer)

    # -----------------------------------------------------------------------

    def set_header(self, header):
        """Overridden. Set a new progress header text.

        :param header: (str) new progress header text.

        """
        self.header.SetLabel(header)
        self.Refresh()
        self.Update()

    # -----------------------------------------------------------------------

    def update(self, percent=None, message=None):
        """Overridden. Update the progress box.

        :param message: (str) progress bar value (default: 0)
        :param percent: (float) progress bar text  (default: None)

        """
        if percent is not None:
            fraction = float(percent)
            # convert fraction to a percentage (if necessary)
            if fraction < 1:
                fraction = int(fraction * 100.)
            if fraction > 100:
                fraction = 100
            self.gauge.SetValue(fraction)

        if message is not None:
            self.text.SetLabel(message)
            self.text.Refresh()

        self.Refresh()
        self.Update()
        time.sleep(0.5)

    # -----------------------------------------------------------------------

    def close(self):
        """Close the progress box."""
        #self.DestroyFadeOut()
        self.Destroy()

# ----------------------------------------------------------------------------
# App to test
# ----------------------------------------------------------------------------


class TestApp(wx.App):

    def __init__(self):
        """Create a customized application."""
        # ensure the parent's __init__ is called with the args we want
        wx.App.__init__(self,
                        redirect=False,
                        filename=None,
                        useBestVisual=True,
                        clearSigInt=True)

        # Fix language and translation
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.__cfg = sppasAppConfig()
        self.settings = WxAppSettings()

        # create the frame
        self.frm = sppasDialog(None, title='Progress test', size=(128, 128), name="main")
        self.SetTopWindow(self.frm)

        # create a panel in the frame
        sizer = wx.BoxSizer()
        sizer.Add(wx.Button(self.frm, label="start"), 1, wx.EXPAND, 0)
        self.frm.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self._on_start)

        # show result
        self.frm.Show()

    def _on_start(self, event):
        wx.BeginBusyCursor()
        p = sppasAnnotProgressDialog()
        logging.debug('progress name={:s}'.format(p.GetName()))

        p.set_new()
        p.set_header("Annotation number 1")
        p.set_fraction(0)
        p.set_text("file one")
        time.sleep(1)
        p.set_fraction(34)
        p.set_text("file two")
        time.sleep(1)
        p.set_fraction(70)
        p.set_text("file three")
        time.sleep(1)
        p.set_fraction(100)

        p.set_new()
        p.set_header("Another annotation")
        p.set_fraction(0)
        p.set_text("one file")
        time.sleep(1)
        p.set_fraction(50)
        p.set_text("two files")
        time.sleep(1)
        p.set_fraction(100)

        p.close()
        wx.EndBusyCursor()

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()
