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

    wxgui.views.singlefilter.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import wx
import re

from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.sp_icons import FILTER_SINGLE
from sppas.src.ui.wxgui.sp_icons import APPLY_ICON
from sppas.src.ui.wxgui.sp_icons import FILTER_ADD_LABEL
from sppas.src.ui.wxgui.sp_icons import FILTER_ADD_DURATION
from sppas.src.ui.wxgui.sp_icons import FILTER_ADD_TIME
from sppas.src.ui.wxgui.sp_icons import FILTER_REMOVE
from sppas.src.ui.wxgui.panels.mainbuttons import MainToolbarPanel
from sppas.src.ui.wxgui.cutils.textutils import TextValidator
from sppas.src.ui.wxgui.ui.CustomListCtrl import CheckListCtrl

try:
    from agw import floatspin as FS
except ImportError:
    import wx.lib.agw.floatspin as FS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ID_ADD_LABEL = wx.NewId()
ID_ADD_TIME = wx.NewId()
ID_ADD_DURATION = wx.NewId()
ID_CLEAR = wx.NewId()

DEFAULT_TIERNAME = "Filtered tier"
DEFAULT_LABEL = "tag1, tag2..."

# ---------------------------------------------------------------------------


class SingleFilterDialog(spBaseDialog):
    """Dialog for the user to fix a set of filters to be applied to a tier.
    
    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL, v3

    """

    def __init__(self, parent, preferences):
        """Create a new dialog."""
        spBaseDialog.__init__(self,
                              parent,
                              preferences,
                              title=" - SingleFilter")
        wx.GetApp().SetAppName("singlefilter")

        # Members
        self.match_all = False

        titlebox = self.CreateTitle(FILTER_SINGLE,
                                    "Filter annotations of a tier")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                              contentbox,
                              buttonbox)
        self.SetMinSize((540, 460))

    # -----------------------------------------------------------------------
    # Create the GUI
    # -----------------------------------------------------------------------

    def _create_buttons(self):
        btn_cancel = self.CreateCancelButton()
        btn_applyany = self.CreateButton(APPLY_ICON,
                                         "Apply - OR", btnid=wx.ID_OK)
        btn_applyall = self.CreateButton(APPLY_ICON,
                                         "Apply - AND", btnid=wx.ID_OK)
        self.SetAffirmativeId(wx.ID_OK)
        btn_applyall.SetDefault()
        btn_applyall.Bind(wx.EVT_BUTTON, self._on_button_all, btn_applyall)
        return self.CreateButtonBox([btn_cancel], [btn_applyany, btn_applyall])

    def _create_content(self):
        self.filterpanel = SingleFilterPanel(self, self.preferences)

        self.tiername_layout = wx.BoxSizer(wx.HORIZONTAL)
        title_tiername = wx.StaticText(self,
                                       label="Name of filtered tier: ",
                                       style=wx.ALIGN_CENTER)
        title_tiername.SetFont(self.preferences.GetValue('M_FONT'))

        self.text_tiername = wx.TextCtrl(self, size=(250, -1),
                                         validator=TextValidator())
        self.text_tiername.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_tiername.SetForegroundColour(wx.Colour(128, 128, 128))
        self.text_tiername.SetValue(DEFAULT_TIERNAME)
        self.text_tiername.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.text_tiername.Bind(wx.EVT_SET_FOCUS, self.OnTextClick)

        self.tiername_layout.Add(title_tiername,
                                 flag=wx.ALL | wx.wx.ALIGN_CENTER_VERTICAL,
                                 border=5)
        self.tiername_layout.Add(self.text_tiername,
                                 flag=wx.EXPAND | wx.ALL | wx.wx.ALIGN_CENTER_VERTICAL,
                                 border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.filterpanel, 1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox.Add(self.tiername_layout, 0, flag=wx.ALL | wx.EXPAND, border=0)
        return vbox

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def _on_button_all(self, event):
        self.match_all = True
        event.Skip()

    def OnTextClick(self, event):
        self.text_tiername.SetForegroundColour(wx.BLACK)
        if self.text_tiername.GetValue().strip() == "":
            self.OnTextErase(event)
        event.Skip()

    def OnTextChanged(self, event):
        self.text_tiername.SetFocus()
        self.text_tiername.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_tiername.Refresh()

    def OnTextErase(self, event):
        self.text_tiername.SetValue('')
        self.text_tiername.SetFocus()
        self.text_tiername.SetBackgroundColour(wx.Colour(245, 220, 240))
        self.text_tiername.Refresh()

    # -------------------------------------------------------------------------
    # Getters...
    # -------------------------------------------------------------------------

    def GetSelectedData(self):
        """Convert the content in a list into filters and return it."""
        return self.filterpanel.GetSelectedData()

    def GetFiltererdTierName(self):
        """Return the future name for the filtered tier."""
        return self.text_tiername.GetValue().strip()

    def GetMatchAll(self):
        """Return True if all predicates must match (i.e. AND operator)."""
        return self.match_all

    def GetAnnotationFormat(self):
        return self.filterpanel.opt.GetValue()

# ----------------------------------------------------------------------------


class SingleFilterPanel(wx.Panel):
    """Panel to fix the filters to be used.

    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL

    """

    def __init__(self, parent, prefsIO):
        wx.Panel.__init__(self, parent, size=(580, 320))
        self.SetBackgroundColour(prefsIO.GetValue('M_BG_COLOUR'))

        # Members
        self.preferences = prefsIO
        self.data = []

        self._create_toolbar()
        self._create_filterlist()
        self.Bind(wx.EVT_BUTTON, self.ProcessEvent)

        self.opt = wx.CheckBox(self, label='Replace tag of annotations '
                                           'by the filter name.')
        self.opt.SetBackgroundColour(prefsIO.GetValue('M_BG_COLOUR'))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toolbar,
                  proportion=0,
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
                  border=4)

        sizer.Add(self.filterlist,
                  proportion=1,
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
                  border=4)

        sizer.Add(self.opt,
                  proportion=0,
                  flag=wx.EXPAND | wx.TOP,
                  border=5)

        self.SetSizer(sizer)
        self.SetMinSize((380, 280))
        self.SetAutoLayout(True)
        self.Center()

    # -------------------------------------------------------------------------

    def _create_toolbar(self):

        self.toolbar = MainToolbarPanel(self, self.preferences)

        self.toolbar.AddButton(ID_ADD_LABEL,
                               FILTER_ADD_LABEL,
                               "+ Tag",
                               tooltip="Add a filter on the content of "
                                       "each annotation of the tier.")

        self.toolbar.AddButton(ID_ADD_TIME,
                               FILTER_ADD_TIME,
                               "+ Loc",
                               tooltip="Add a localization to start or "
                                       "to end filtering.")

        self.toolbar.AddButton(ID_ADD_DURATION,
                               FILTER_ADD_DURATION,
                               "+ Dur",
                               tooltip="Add a filter on the duration of "
                                       "each annotations of the tier.")

        self.toolbar.AddSpacer()

        self.toolbar.AddButton(ID_CLEAR,
                               FILTER_REMOVE,
                               "- Remove",
                               tooltip="Remove checked filters of the list.")

    # -------------------------------------------------------------------------

    def _create_filterlist(self):

        self.filterlist = CheckListCtrl(self, -1,
                                        style=wx.LC_REPORT | wx.BORDER_NONE)
        self.filterlist.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))
        self.filterlist.SetFont(self.preferences.GetValue('M_FONT'))

        cols = ("Filter", "Function", "Value")
        for i, col in enumerate(cols):
            self.filterlist.InsertColumn(i, col)
        self.filterlist.SetColumnWidth(1, 120)
        self.filterlist.SetFocus()

    # ------------------------------------------------------------------------
    # Callbacks to any kind of event
    # ------------------------------------------------------------------------

    def ProcessEvent(self, event):
        """Process an event.

        Processes an event., searching event tables and calling zero or more
        suitable event handler function(s).  Note that the ProcessEvent
        method is called from the wxPython docview framework directly since
        wxPython does not have a virtual ProcessEvent function.

        """
        pid = event.GetId()

        if pid == ID_ADD_LABEL:
            self.OnAddLabel(event)
            return True

        elif pid == ID_ADD_TIME:
            self.OnAddTime(event)
            return True

        elif pid == ID_ADD_DURATION:
            self.OnAddDuration(event)
            return True

        elif pid == ID_CLEAR:
            self.OnRemove(event)
            return True

        return wx.GetApp().ProcessEvent(event)

    # ----------------------------------------------------------------------
    # Callbacks
    # ----------------------------------------------------------------------

    def OnAddLabel(self, event):
        dlg = LabelFilterDialog(self, self.preferences)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetData()
            self._add_filter(data)
            self.data.append(data)
        dlg.Destroy()

    def OnAddTime(self, event):
        dlg = TimeFilterDialog(self, self.preferences)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetData()
            self._add_filter(data)
            self.data.append(data)
        dlg.Destroy()

    def OnAddDuration(self, event):
        dlg = DurationFilterDialog(self, self.preferences)
        dlg.Show()
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetData()
            self._add_filter(data)
            self.data.append(data)
        dlg.Destroy()

    def OnRemove(self, event):
        # fix a list of selected idem indexes
        selected = []
        currentf = self.filterlist.GetFirstSelected()
        while currentf != -1:
            nextf = self.filterlist.GetNextSelected(currentf)
            selected.append(currentf)
            currentf = nextf

        # remove selected items (starting from end!)
        for index in reversed(selected):
            self.data.pop(index)
            self.filterlist.DeleteItem(index)

    # ----------------------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------------------

    def GetSelectedData(self):
        """Return list of the selected data defined in the notebook."""

        all_data = list()
        sel_list = self.filterlist.GetFirstSelected()
        while sel_list != -1:
            all_data.append(self.data[sel_list])
            sel_list = self.filterlist.GetNextSelected(sel_list)

        return all_data

    # ----------------------------------------------------------------------
    # Private methods
    # ----------------------------------------------------------------------

    def _add_filter(self, data):
        """Add a filter in the list."""

        index = self.filterlist.GetItemCount()

        self.filterlist.InsertStringItem(index, data[0])
        self.filterlist.SetStringItem(index, 1, data[1])
        self.filterlist.SetStringItem(index, 2, str(data[2]))
        self.filterlist.Select(index, on=True)

# --------------------------------------------------------------------------


class LabelFilterDialog(spBaseDialog):
    """Open a frame to fix the list of patterns and mode to filter tags.

    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL, v3

    """
    choices = (
               ("exact", "exact"),
               ("not exact", "exact"),
               ("contains", "contains"),
               ("not contains", "contains"),
               ("starts with", "startswith"),
               ("not starts with", "startswith"),
               ("ends with", "endswith"),
               ("not ends with", "endswith"),
               ("match (regexp)", "regexp"),
               ("not match", "regexp")
              )

    def __init__(self, parent, preferences):
        """Constructor."""
        spBaseDialog.__init__(self, parent, preferences,
                              title=" - Tag filter")
        wx.GetApp().SetAppName("tagfilter")

        titlebox = self.CreateTitle(FILTER_ADD_LABEL, "Tag-based single filter")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                              contentbox,
                              buttonbox)

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_cancel = self.CreateCancelButton()
        btn_okay = self.CreateOkayButton()
        return self.CreateButtonBox([btn_cancel],[btn_okay])

    def _create_content(self):
        self.notebook = wx.Notebook(self)
        self.notebook.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))

        page1 = LabelString(self.notebook, self.preferences)
        page2 = LabelNumber(self.notebook, self.preferences)
        page3 = LabelBoolean(self.notebook, self.preferences)
        # add the pages to the notebook with the label to show on the tab
        self.notebook.AddPage(page1, "  String  ")
        self.notebook.AddPage(page2, "  Number  ")
        self.notebook.AddPage(page3, "  Boolean ")

        return self.notebook

    # -----------------------------------------------------------------------

    def GetData(self):
        """Get the data.

        :returns: (tuple) with:

               - "tag"
               - function (str): one of the methods in TagCompare
               - values (list): patterns to find
        """
        page_idx = self.notebook.GetSelection()
        data = self.notebook.GetPage(page_idx).GetData()
        return data

# ---------------------------------------------------------------------------


class LabelString(wx.Panel):
    """Search into a label of type string."""

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        self.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))

        # Widgets
        msg = "Patterns to find (separated by commas):"
        self.label = wx.StaticText(self, label=msg)
        self.text = wx.TextCtrl(self,
                                value=DEFAULT_LABEL,
                                validator=TextValidator())
        self.text.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))

        choices = [row[0] for row in LabelFilterDialog.choices]
        self.radiobox = wx.RadioBox(self,
                                    label="Functions",
                                    choices=choices,
                                    majorDimension=2)
        self.checkbox = wx.CheckBox(self, label="Case Sensitive")
        self.checkbox.SetValue(True)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, flag=wx.EXPAND | wx.ALL, border=4)
        sizer.Add(self.text, flag=wx.EXPAND | wx.ALL, border=4)
        sizer.Add(self.radiobox, flag=wx.EXPAND | wx.ALL, border=4)
        sizer.Add(self.checkbox, flag=wx.EXPAND | wx.ALL, border=4)

        self.SetSizer(sizer)

    # ------------------------------------------------------------------------

    def OnTextClick(self, event):
        self.text.SetForegroundColour(wx.BLACK)
        if self.text.GetValue() == DEFAULT_LABEL:
            self.OnTextErase(event)
        event.Skip()
        #self.text.SetFocus()

    def OnTextChanged(self, event):
        self.text.SetFocus()
        self.text.Refresh()

    def OnTextErase(self, event):
        self.text.SetValue('')
        self.text.SetFocus()
        self.text.Refresh()

    # -----------------------------------------------------------------------

    def GetData(self):
        """Return the data defined by the user.

        Returns: (tuple) with:

               - "tag"
               - function (str): one of the methods in TagCompare (strings)
               - values (list): patterns to find separated by commas

        """
        idx = self.radiobox.GetSelection()
        given_fct = LabelFilterDialog.choices[idx][1]

        # Fill the resulting dict
        prepend_fct = ""

        if given_fct != "regexp":
            # prepend "not_" if reverse
            if (idx % 2) != 0:
                prepend_fct += "not_"
            # prepend "i" if case-insensitive
            if self.checkbox.GetValue() is False:
                prepend_fct += "i"

            # fix the value to find (one or several with the same function)
            values = re.split(',', self.text.GetValue())
            values = [" ".join(p.split()) for p in values]
        else:
            values = [self.text.GetValue()]

        return "tag", prepend_fct+given_fct, values

# ---------------------------------------------------------------------------


class LabelNumber(wx.Panel):
    """Search into a label of type number."""

    choices = (
               (" is equal to...",     "equal"),
               (" is greater than...", "greater"),
               (" is less than...",    "lower"),
             )

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        self.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))

        # Widgets
        label = wx.StaticText(self, label="... this value: ")
        choices = [choice[0] for choice in LabelNumber.choices]
        self.radiobox = wx.RadioBox(self,
                                    label="The tag ",
                                    choices=choices,
                                    majorDimension=1,
                                    style=wx.RA_SPECIFY_COLS)
        self.ctrl = FS.FloatSpin(self,
                                 min_val=0.0,
                                 increment=0.01,
                                 value=0,
                                 digits=3)

        # Layout
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.radiobox, 1, flag=wx.EXPAND | wx.ALL, border=4)
        sizer.Add(hbox, 0, flag=wx.EXPAND | wx.ALL, border=4)
        self.SetSizer(sizer)

    # -----------------------------------------------------------------------

    def GetData(self):
        """Return the data defined by the user.

        Returns: (tuple) with:

               - "tag"
               - function (str): one of the methods in TagCompare (numbers)
               - values (list): number to be compared with (but of 'str' type)

        """
        idx = self.radiobox.GetSelection()
        given_fct = LabelNumber.choices[idx][1]
        value = self.ctrl.GetValue()

        return "tag", given_fct, [value]

# ---------------------------------------------------------------------------


class LabelBoolean(wx.Panel):
    """Search into a label of type boolean."""

    choices = (
               (" is False", "bool"),
               (" is True",  "bool"),
             )

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        self.SetBackgroundColour(self.preferences.GetValue('M_BG_COLOUR'))

        choices = [choice[0] for choice in LabelBoolean.choices]
        self.radiobox = wx.RadioBox(self,
                                    label="The tag ",
                                    choices=choices,
                                    majorDimension=1,
                                    style=wx.RA_SPECIFY_COLS)

    # -----------------------------------------------------------------------

    def GetData(self):
        """Return the data defined by the user.

        Returns: (tuple) with:

               - "tag"
               - function (str): "bool"
               - values (list): True or False

        """
        idx = self.radiobox.GetSelection()
        return "tag", "bool", [bool(idx)]

# ---------------------------------------------------------------------------


class TimeFilterDialog(spBaseDialog):
    """Open a frame to fix the list of modes and values to filter time(s).

    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL, v3

    """
    choices = (
               (" is starting at...", "rangefrom"),
               (" is ending at...",   "rangeto")
              )

    def __init__(self, parent, preferences):
        """Constructor."""
        spBaseDialog.__init__(self, parent, preferences,
                              title=" - Localization filter")
        wx.GetApp().SetAppName("locfilter")

        titlebox = self.CreateTitle(FILTER_ADD_TIME,
                                    "Localization-based filter")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                              contentbox,
                              buttonbox)

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_cancel = self.CreateCancelButton()
        btn_okay = self.CreateOkayButton()
        return self.CreateButtonBox([btn_cancel], [btn_okay])

    def _create_content(self):
        # Widgets
        label = wx.StaticText(self, label="... this time value in seconds: ")
        choices = [choice[0] for choice in TimeFilterDialog.choices]
        self.radiobox = wx.RadioBox(self,
                                    label="The time ",
                                    choices=choices,
                                    majorDimension=1)
        self.ctrl = FS.FloatSpin(self, min_val=0.0,
                                 increment=0.001,
                                 value=0,
                                 digits=3)
        # Layout
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        content_layout = wx.BoxSizer(wx.VERTICAL)
        content_layout.Add(self.radiobox, 1, flag=wx.EXPAND | wx.ALL, border=0)
        content_layout.Add(hbox, 0, flag=wx.EXPAND | wx.ALL, border=0)
        return content_layout

    # -----------------------------------------------------------------------

    def GetData(self):
        """Return the data defined by the user.

        Returns: (tuple) with
               type (str): loc
               function (str): "rangefrom" or "rangeto"
               values (list): time value (represented by a 'str')

        """
        idx = self.radiobox.GetSelection()
        given_fct = TimeFilterDialog.choices[idx][1]
        value = self.ctrl.GetValue()

        return "loc", given_fct, [value]

# ---------------------------------------------------------------------------


class DurationFilterDialog(spBaseDialog):
    """Open a frame to fix the list of modes and values to filter duration(s).

    :author:  Brigitte Bigi
    :contact: develop@sppas.org
    :license: GPL, v3

    """
    choices = (
               (" is equal to...", "eq"),
               (" is not equal to...", "ne"),
               (" is greater than...", "gt"),
               (" is less than...", "lt"),
               (" is greater or equal to...", "ge"),
               (" is lesser or equal to...", "le")
             )

    def __init__(self, parent, preferences):
        """Constructor."""
        spBaseDialog.__init__(self, parent, preferences,
                              title=" - Duration Filter")
        wx.GetApp().SetAppName("durfilter")

        titlebox = self.CreateTitle(FILTER_ADD_DURATION, "Duration-based single filter")
        contentbox = self._create_content()
        buttonbox = self._create_buttons()

        self.LayoutComponents(titlebox,
                              contentbox,
                              buttonbox)

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_cancel = self.CreateCancelButton()
        btn_okay   = self.CreateOkayButton()
        return self.CreateButtonBox([btn_cancel],[btn_okay])

    def _create_content(self):
        # Widgets
        label = wx.StaticText(self, label="... this value in seconds: ")
        choices = [choice[0] for choice in DurationFilterDialog.choices]
        self.radiobox = wx.RadioBox(self,
                                    label="The duration",
                                    choices=choices,
                                    majorDimension=1)
        self.ctrl = FS.FloatSpin(self,
                                 min_val=0.0,
                                 increment=0.01,
                                 value=0,
                                 digits=3)
        # Layout
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        content_layout = wx.BoxSizer(wx.VERTICAL)
        content_layout.Add(self.radiobox, 1, flag=wx.EXPAND | wx.ALL, border=0)
        content_layout.Add(hbox, 0, flag=wx.EXPAND | wx.ALL, border=0)
        return content_layout

    # -----------------------------------------------------------------------

    def GetData(self):
        """Return the data defined by the user.

        Returns: (tuple) with
               type (str): dur
               function (str): one of the choices
               values (list): time value (represented by a 'str')

        """
        idx = self.radiobox.GetSelection()
        given_fct = DurationFilterDialog.choices[idx][1]
        value = self.ctrl.GetValue()
        return "dur", given_fct, [value]
