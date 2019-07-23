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
#                   Copyright (C) 2011-2016  Brigitte Bigi
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
# File: settings.py
# ----------------------------------------------------------------------------

import os
import wx
from wx.lib import stattext

from sppas.src.config import paths

from sppas.src.anndata.aio import extensions_out_multitiers as extensions_out
from sppas.src.ui.wxgui.dialogs.basedialog import spBaseDialog
from sppas.src.ui.wxgui.sp_icons import SETTINGS_ICON
from sppas.src.ui.wxgui.sp_icons import BG_COLOR_ICON
from sppas.src.ui.wxgui.sp_icons import FG_COLOR_ICON
from sppas.src.ui.wxgui.sp_icons import FONT_ICON
from sppas.src.ui.wxgui.cutils.imageutils import spBitmap


# ----------------------------------------------------------------------------
# class SettingsDialog
# ----------------------------------------------------------------------------

class SettingsDialog(spBaseDialog):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      develop@sppas.org
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      This class is used to fix all user's settings, with a Dialog.

    Dialog for the user to fix all preferences.

    """
    def __init__(self, parent, preferences):
        """
        Create a new dialog fo fix preferences, sorted in a notebook.

        @param parent is a wx window.
        @param preferences (Preferences)

        """
        spBaseDialog.__init__(self, parent, preferences, title=" - Settings")
        wx.GetApp().SetAppName( "settings" )

        titlebox   = self.CreateTitle(SETTINGS_ICON,"User settings")
        contentbox = self._create_content()
        buttonbox  = self._create_buttons()

        self.LayoutComponents( titlebox,
                               contentbox,
                               buttonbox )

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_buttons(self):
        btn_save   = self.CreateSaveButton("Save the settings.")
        btn_cancel = self.CreateCancelButton()
        btn_okay   = self.CreateOkayButton()
        self.Bind(wx.EVT_BUTTON, self._on_save, btn_save)
        return self.CreateButtonBox( [btn_save],[btn_cancel,btn_okay] )

    def _create_content(self):
        self.notebook = wx.Notebook(self)
        page1 = PrefsGeneralPanel(self.notebook, self.preferences)
        page2 = PrefsThemePanel(self.notebook, self.preferences)
        page3 = PrefsAnnotationPanel(self.notebook, self.preferences)
        # add the pages to the notebook with the label to show on the tab
        self.notebook.AddPage(page1, "General")
        self.notebook.AddPage(page2, "Icons Theme")
        self.notebook.AddPage(page3, "Annotation")
        return self.notebook

    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def _on_save(self, event):
        """Save preferences in a file."""

        self.preferences.Write()

    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def GetPreferences(self):
        """Return the preferences."""

        return self.preferences

# ----------------------------------------------------------------------------

class PrefsGeneralPanel( wx.Panel ):
    """
    Main Frame settings: background color, foreground color and font, etc.

    """
    def __init__(self, parent, prefsIO):
        """

        @param parent is a wx object.
        @param prefsIO (Preferences)

        """
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour( prefsIO.GetValue("M_BG_COLOUR") )
        self.preferences = prefsIO

        gbs = self.__create_sizer()

        self.UpdateUI()
        self.SetSizer(gbs)

    # ------------------------------------------------------------------------

    def __create_sizer(self):

        gbs = wx.GridBagSizer(hgap=5, vgap=5)

        # ---------- Background color

        txt_bg = wx.StaticText(self, -1, "Background color: ")
        gbs.Add(txt_bg, (0,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        self.btn_color_bg = wx.BitmapButton(self, -1, spBitmap( BG_COLOR_ICON, 24, theme=self.preferences.GetValue('M_ICON_THEME')))
        self.btn_color_bg.Bind(wx.EVT_BUTTON, self.onColorDlg, self.btn_color_bg)
        gbs.Add(self.btn_color_bg, (0,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        # ---------- Foreground color

        txt_fg = wx.StaticText(self, -1, "Foreground color: ")
        gbs.Add(txt_fg, (1,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        self.btn_color_fg = wx.BitmapButton(self, -1, spBitmap( FG_COLOR_ICON, 24, theme=self.preferences.GetValue('M_ICON_THEME') ))
        self.btn_color_fg.Bind(wx.EVT_BUTTON, self.onColorDlg, self.btn_color_fg)
        gbs.Add(self.btn_color_fg, (1,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        # ---------- Font

        txt_font = wx.StaticText(self, -1, "Font: ")
        gbs.Add(txt_font, (2,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        btn_font = wx.BitmapButton(self, -1, spBitmap( FONT_ICON, 24, theme=None ))
        self.Bind(wx.EVT_BUTTON, self.onSelectFont, btn_font)
        gbs.Add(btn_font, (2,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        # ---------- Sample text

        self.sampleText = stattext.GenStaticText(self, -1, u"  This is a sample text.?!§+={}[]#&$€%éèàù")
        self.sampleText.SetFont( self.preferences.GetValue('M_FONT') )
        self.sampleText.SetBackgroundColour( self.preferences.GetValue('M_BG_COLOUR') )
        self.sampleText.SetForegroundColour( self.preferences.GetValue('M_FG_COLOUR') )

        gbs.Add(self.sampleText, (3,0), (1,2), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)

        # ---------- tips

        txt_tips = wx.StaticText(self, -1, "Show tips at start-up: ")
        gbs.Add(txt_tips, (4,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        btn_tips = wx.CheckBox(self, -1, "")
        btn_tips.SetValue( self.preferences.GetValue('M_TIPS'))
        self.Bind(wx.EVT_CHECKBOX, self.onTipsChecked, btn_tips)
        gbs.Add(btn_tips, (4,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)

        # ----------

        gbs.AddGrowableCol(1)

        return gbs

    # ------------------------------------------------------------------------

    def UpdateUI(self):
        """
        Update the sample to look like the chosen decoration.

        """
        self.sampleText.SetFont( self.preferences.GetValue('M_FONT') )
        self.sampleText.SetForegroundColour( self.preferences.GetValue('M_FG_COLOUR') )
        self.sampleText.SetBackgroundColour( self.preferences.GetValue('M_BG_COLOUR') )

        self.Layout()

    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def onColorDlg(self, event):
        """
        Open a dialog to choose a color, then fix it.

        """
        # get the button that was clicked
        button = event.GetEventObject()

        # open the dialog
        dlg = wx.ColourDialog(self)

        # Ensure the full colour dialog is displayed,
        # not the abbreviated version.
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data  = dlg.GetColourData()
            color = data.GetColour()
            if button == self.btn_color_bg:
                self.preferences.SetValue( 'M_BG_COLOUR', 'wx.Colour', color )
            else:
                self.preferences.SetValue( 'M_FG_COLOUR', 'wx.Colour', color )
            self.UpdateUI()

        dlg.Destroy()

    #-------------------------------------------------------------------------

    def onSelectFont(self, event):
        """
        Open a dialog to choose a font, then fix it.

        """
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour( self.preferences.GetValue('M_FG_COLOUR') ) # set font colour
        data.SetInitialFont( self.preferences.GetValue('M_FONT') ) # set font

        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data   = dlg.GetFontData()
            font   = data.GetChosenFont()
            color  = data.GetColour()
            self.preferences.SetValue( 'M_FONT', 'wx.Font', font )
            self.preferences.SetValue( 'M_FG_COLOUR', 'wx.Colour', color )
            self.UpdateUI()

        dlg.Destroy()

    #-------------------------------------------------------------------------

    def onTipsChecked(self, event):
        """
        Tips at start-up.

        """
        self.preferences.SetValue( 'M_TIPS', 'bool', event.GetEventObject().GetValue() )

# ----------------------------------------------------------------------------

class PrefsAnnotationPanel( wx.Panel ):
    """
    Panel to fix prefs for annotations.

    """
    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour( prefsIO.GetValue("M_BG_COLOUR") )

        self.preferences = prefsIO

        # ---------- Annotations file extensions

        currentext = self.preferences.GetValue('M_OUTPUT_EXT')
        currentchoice = extensions_out.index(currentext)

        self.radiobox = wx.RadioBox(self, label="Annotations file format: ",
                                    choices=extensions_out, majorDimension=1) # majorDimension is the nb max of columns
        # check the current theme
        self.radiobox.SetSelection( currentchoice )
        # bind any theme change
        self.Bind(wx.EVT_RADIOBOX, self.onOutputFormat, self.radiobox)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.radiobox, 0, flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        self.SetSizer(s)

    # -------------------------------------------------------------------------

    def onOutputFormat(self, event):
        """
        File format of automatic annotations.

        """
        idx = self.radiobox.GetSelection()
        self.preferences.SetValue( 'M_OUTPUT_EXT', 'str', extensions_out[idx] )

# ----------------------------------------------------------------------------


class PrefsThemePanel( wx.Panel ):
    """
    Panel with a radiobox to choose the theme of the icons.

    """
    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(prefsIO.GetValue("M_BG_COLOUR"))

        self.preferences = prefsIO

        self.iconthemes = os.listdir(os.path.join(paths.etc, "icons"))
        currenttheme = self.preferences.GetValue('M_ICON_THEME')
        currentchoice = self.iconthemes.index(currenttheme)

        self.radiobox = wx.RadioBox(self,
                                    label="Theme of the icons: ",
                                    choices=self.iconthemes,
                                    majorDimension=1)
        # check the current theme
        self.radiobox.SetSelection(currentchoice)

        # bind any theme change
        self.Bind(wx.EVT_RADIOBOX, self.onIconThemeClick, self.radiobox)

        text = "To apply the theme change,\n" \
               "click on Save button, then Close and re-start SPPAS."
        txt = wx.StaticText(self, -1, text, style=wx.ALIGN_CENTER | wx.NO_BORDER)
        font = wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL)
        txt.SetFont(font)
        txt.SetForegroundColour(wx.RED)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.radiobox, 2, flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        s.Add(txt, 1, flag=wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(s)

    # -------------------------------------------------------------------------

    def onIconThemeClick(self, event):
        """
        Set the new theme.

        """
        idxtheme = self.radiobox.GetSelection()
        self.preferences.SetValue('M_ICON_THEME', 'str', self.iconthemes[idxtheme])
