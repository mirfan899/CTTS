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

    src.ui.phoenix.dialogs.messages.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import logging
import wx

from sppas.src.config import ui_translation

from ..windows import sppasMessageText
from ..windows import sppasPanel
from ..windows import sppasDialog

# ----------------------------------------------------------------------------

MSG_HEADER_ERROR = ui_translation.gettext("Error")
MSG_HEADER_WARNING = ui_translation.gettext("Warning")
MSG_HEADER_QUESTION = ui_translation.gettext("Question")
MSG_HEADER_INFO = ui_translation.gettext("Information")

# ----------------------------------------------------------------------------


class sppasBaseMessageDialog(sppasDialog):
    """Base class to create message dialogs.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    """

    def __init__(self, parent, message, title=None, style=wx.ICON_INFORMATION):
        """Create a dialog with a message.

        :param parent: (wx.Window)
        :param message: (str) the file to display in this frame.
        :param title: (str) a title to display in the header. Default is the icon one.
        :param style: ONE of wx.ICON_INFORMATION, wx.ICON_ERROR, wx.ICON_EXCLAMATION, wx.YES_NO

        """
        super(sppasBaseMessageDialog, self).__init__(
            parent=parent,
            title="Message",
            style=wx.FRAME_TOOL_WINDOW | wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.STAY_ON_TOP)  # | wx.DIALOG_NO_PARENT)

        self._create_header(style, title)
        self._create_content(message)
        self._create_buttons()

        # Fix frame properties
        self.SetMinSize(wx.Size(sppasDialog.fix_size(256),
                                sppasDialog.fix_size(164)))
        self.LayoutComponents()
        self.CenterOnParent()
        self.GetSizer().Fit(self)
        self.FadeIn(deltaN=-10)

    # -----------------------------------------------------------------------

    def _create_header(self, style, title):
        """Create the header of the message dialog."""
        # Create the header
        if style == wx.ICON_ERROR:
            icon = "error"
            if title is None:
                title = MSG_HEADER_ERROR

        elif style == wx.ICON_WARNING:
            icon = "warning"
            if title is None:
                title = MSG_HEADER_WARNING

        elif style == wx.YES_NO:
            icon = "question"
            if title is None:
                title = MSG_HEADER_QUESTION

        else:
            icon = "information"
            if title is None:
                title = MSG_HEADER_INFO

        self.CreateHeader(title, icon_name=icon)

    # -----------------------------------------------------------------------

    def _create_content(self, message):
        """Create the content of the message dialog."""
        p = sppasPanel(self)
        s = wx.BoxSizer(wx.HORIZONTAL)
        txt = sppasMessageText(p, message)
        s.Add(txt, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        p.SetSizer(s)
        p.SetName("content")
        p.SetMinSize(wx.Size(-1, sppasDialog.fix_size(96)))

    # -----------------------------------------------------------------------

    def _create_buttons(self):
        """Override to create the buttons and bind events."""
        raise NotImplementedError

# ---------------------------------------------------------------------------
# Message dialogs
# ---------------------------------------------------------------------------


class sppasYesNoDialog(sppasBaseMessageDialog):
    """Create a message in a wx.Dialog with a yes-no question.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    wx.ID_YES or wx.ID_NO is returned if a button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    >>> dialog = sppasYesNoDialog("Really exit?")
    >>> response = dialog.ShowModal()
    >>> dialog.Destroy()
    >>> if response == wx.ID_YES:
    >>>     # do something here

    """

    def __init__(self, message):
        super(sppasYesNoDialog, self).__init__(
            parent=None,
            message=message,
            style=wx.YES_NO)

    # -----------------------------------------------------------------------

    def _create_buttons(self):
        self.CreateActions([wx.ID_NO, wx.ID_YES])
        self.Bind(wx.EVT_BUTTON, self._process_event)
        self.SetAffirmativeId(wx.ID_YES)

    # -----------------------------------------------------------------------

    def _process_event(self, event):
        """Process any kind of events.

        :param event: (wx.Event)

        """
        event_obj = event.GetEventObject()
        event_id = event_obj.GetId()
        if event_id == wx.ID_NO:
            self.EndModal(wx.ID_NO)
        else:
            event.Skip()

# ---------------------------------------------------------------------------


class sppasConfirm(sppasBaseMessageDialog):
    """Create a message in a wx.Dialog to confirm an action after an error.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    wx.ID_YES is returned if 'yes' is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed or cancel is clicked.

    >>> dialog = sppasConfirm("Confirm..."))
    >>> response = dialog.ShowModal()
    >>> dialog.Destroy()
    >>> if response == wx.ID_YES:
    >>>     # do something here

    """

    def __init__(self, message, title=None):
        super(sppasConfirm, self).__init__(
            parent=None,
            message=message,
            title=title,
            style=wx.ICON_ERROR)

    # -----------------------------------------------------------------------

    def _create_buttons(self):
        self.CreateActions([wx.ID_CANCEL, wx.ID_YES])
        self.Bind(wx.EVT_BUTTON, self._process_event)
        self.SetAffirmativeId(wx.ID_YES)

    # -----------------------------------------------------------------------

    def _process_event(self, event):
        """Process any kind of events.

        :param event: (wx.Event)

        """
        event_obj = event.GetEventObject()
        event_id = event_obj.GetId()
        if event_id == wx.ID_CANCEL:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()

# ---------------------------------------------------------------------------


class sppasInformationDialog(sppasBaseMessageDialog):
    """Create a message in a wx.Dialog with an information.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    wx.ID_OK is returned if the button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    >>> dialog = sppasInformationDialog("you are here")
    >>> dialog.ShowModal()
    >>> dialog.Destroy()

    """

    def __init__(self, message):
        super(sppasInformationDialog, self).__init__(
            parent=None,
            message=message,
            style=wx.ICON_INFORMATION)

    # -----------------------------------------------------------------------

    def _create_buttons(self):
        self.CreateActions([wx.ID_OK])
        self.SetAffirmativeId(wx.ID_OK)

# ---------------------------------------------------------------------------


class sppasErrorDialog(sppasBaseMessageDialog):
    """Create a message in a wx.Dialog with a error message.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    wx.ID_OK is returned if the button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    >>> dialog = sppasErrorDialog("an error occurred")
    >>> dialog.ShowModal()
    >>> dialog.Destroy()

    """

    def __init__(self, message, title=None):
        super(sppasErrorDialog, self).__init__(
            parent=None,
            message=message,
            title=title,
            style=wx.ICON_ERROR)

    # -----------------------------------------------------------------------

    def _create_buttons(self):
        self.CreateActions([wx.ID_OK])
        self.SetAffirmativeId(wx.ID_OK)

# ---------------------------------------------------------------------------
# Ready-to-use functions to display messages
# ---------------------------------------------------------------------------


def YesNoQuestion(message):
    """Display a yes-no question.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    :param message: (str) The question to ask
    :returns: the response

    wx.ID_YES or wx.ID_NO is returned if a button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    """
    logging.info(message)
    dialog = sppasYesNoDialog(message)
    response = dialog.ShowModal()
    dialog.Destroy()
    logging.info("User clicked yes" if response == wx.ID_YES else "User clicked no")
    return response


def Confirm(message, title=None):
    """Display a confirmation after an error.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    :param message: (str) The error and confirmation question
    :param title: (str) Title of the dialog window
    :returns: the response

    wx.ID_YES if ok button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed or cancel clicked.

    """
    logging.error(message)
    dialog = sppasConfirm(message, title)
    response = dialog.ShowModal()
    dialog.Destroy()
    logging.info("Confirmed by user." if response == wx.ID_YES else "User cancelled.")
    return response


def Error(message, title=None):
    """Display a error.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    :param message: (str) The question to ask
    :returns: the response

    wx.ID_OK is returned if a button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    """
    logging.error(message)
    dialog = sppasErrorDialog(message, title=None)
    response = dialog.ShowModal()
    dialog.Destroy()
    return response


def Information(message):
    """Display an information.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    :param message: (str) The question to ask
    :returns: the response

    wx.ID_OK is returned if a button is clicked.
    wx.ID_CANCEL is returned if the dialog is destroyed.

    """
    logging.info(message)
    dialog = sppasInformationDialog(message)
    response = dialog.ShowModal()
    dialog.Destroy()
    return response
