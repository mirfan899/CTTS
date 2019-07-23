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
# File: sndplayer.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx
import logging
import wx.media

from sppas.src.ui.wxgui.sp_images import PLAYER_BACKGROUND

from sppas.src.ui.wxgui.sp_icons import PLAYER_INFO
from sppas.src.ui.wxgui.sp_icons import PLAYER_INFO_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_EJECT
from sppas.src.ui.wxgui.sp_icons import PLAYER_EJECT_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_NEXT
from sppas.src.ui.wxgui.sp_icons import PLAYER_NEXT_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_REWIND
from sppas.src.ui.wxgui.sp_icons import PLAYER_REWIND_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_PLAY
from sppas.src.ui.wxgui.sp_icons import PLAYER_PLAY_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_REPLAY
from sppas.src.ui.wxgui.sp_icons import PLAYER_REPLAY_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_PAUSE
from sppas.src.ui.wxgui.sp_icons import PLAYER_PAUSE_DISABLED
from sppas.src.ui.wxgui.sp_icons import PLAYER_STOP
from sppas.src.ui.wxgui.sp_icons import PLAYER_STOP_DISABLED

from sppas.src.ui.wxgui.ui.CustomEvents import FileWanderEvent
import sppas.src.ui.wxgui.ui.KnobCtrl as KC

from sppas.src.ui.wxgui.structs.prefs import Preferences
from sppas.src.ui.wxgui.structs.theme import sppasTheme

from sppas.src.ui.wxgui.cutils.ctrlutils import CreateButton
from sppas.src.ui.wxgui.cutils.imageutils import spBitmap

from sppas.src.ui.wxgui.dialogs.sndinfodialog import ShowAudioInfo
from sppas.src.ui.wxgui.dialogs.msgdialogs import ShowInformation

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TIMER_STEP = 10    # timer step event (in milliseconds)
FORWARD_STEP = 1000  # forward step (in milliseconds)
BACKWARD_STEP = 1000  # backward step (in milliseconds)

# ---------------------------------------------------------------------------


class SndPlayer(wx.Panel):
    """
    @author:  Brigitte Bigi
    @contact: develop@sppas.org
    @license: GPL, version 3
    @summary: This class is a generic Sound Player.
    """

    def __init__(self, parent, orient=wx.VERTICAL, refreshtimer=TIMER_STEP, prefsIO=None):
        """
        Creates a new SndPlayer instance.

        @param refreshtimer (int) Timer refresh value in milliseconds. The timer is used to update the playing state.
        @param prefsIO (PreferencesIO) Fix preferences for colors, fonts, etc. and for the list of buttons to display.

        """
        wx.Panel.__init__(self, parent)

        # members
        self._prefs          = self._check_prefs(prefsIO)
        self._filename       = None
        self._mediaplayer    = None
        self._showpanel      = None    # panel to show information (clock, peakmeter, signal, ...)
        self._playbackSlider = None    # slider (to change the position with the mouse)
        self._knob           = None    # volume control
        self._offsets        = (0, 0)  # from/to offsets
        self._autoreplay     = False

        self._init_buttons()

        # create the audio bar
        if orient == wx.VERTICAL:
            sizer = self._build_audioadvanced()
        else:
            sizer = self._build_audiosimple()

        # events
        self.Bind(wx.EVT_SLIDER, self.onSeek)

        # timer, used to update the playing state
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self._refreshTimer = refreshtimer

        self.SetBackgroundColour(self._prefs.GetValue("M_BG_COLOUR"))
        self.SetForegroundColour(self._prefs.GetValue("M_FG_COLOUR"))
        self.SetFont(self._prefs.GetValue("M_FONT"))

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Layout()

    # -----------------------------------------------------------------------
    # Build and check methods (private)
    # -----------------------------------------------------------------------

    def _init_buttons(self):
        """
        Initialize members for audio button creations.

        """
        self._buttons = {}
        self._dict_buttons_enable = {}
        self._dict_buttons_disable = {}

        __theme = self._prefs.GetValue('M_ICON_THEME')
        _tbsize = self._prefs.GetValue('M_TOOLBAR_ICONSIZE')
        self.BMP_PLAYER_INFO            = spBitmap(PLAYER_INFO,           _tbsize, theme=__theme)
        self.BMP_PLAYER_INFO_DISABLED   = spBitmap(PLAYER_INFO_DISABLED,  _tbsize, theme=__theme)
        self.BMP_PLAYER_EJECT           = spBitmap(PLAYER_EJECT,          _tbsize, theme=__theme)
        self.BMP_PLAYER_EJECT_DISABLED  = spBitmap(PLAYER_EJECT_DISABLED, _tbsize, theme=__theme)
        self.BMP_PLAYER_NEXT            = spBitmap(PLAYER_NEXT,           _tbsize, theme=__theme)
        self.BMP_PLAYER_NEXT_DISABLED   = spBitmap(PLAYER_NEXT_DISABLED,  _tbsize, theme=__theme)
        self.BMP_PLAYER_REWIND          = spBitmap(PLAYER_REWIND,         _tbsize, theme=__theme)
        self.BMP_PLAYER_REWIND_DISABLED = spBitmap(PLAYER_REWIND_DISABLED,_tbsize, theme=__theme)
        self.BMP_PLAYER_PLAY            = spBitmap(PLAYER_PLAY,           _tbsize, theme=__theme)
        self.BMP_PLAYER_PLAY_DISABLED   = spBitmap(PLAYER_PLAY_DISABLED,  _tbsize, theme=__theme)
        self.BMP_PLAYER_REPLAY          = spBitmap(PLAYER_REPLAY,         _tbsize, theme=__theme)
        self.BMP_PLAYER_REPLAY_DISABLED = spBitmap(PLAYER_REPLAY_DISABLED,_tbsize, theme=__theme)
        self.BMP_PLAYER_PAUSE           = spBitmap(PLAYER_PAUSE,          _tbsize, theme=__theme)
        self.BMP_PLAYER_PAUSE_DISABLED  = spBitmap(PLAYER_PAUSE_DISABLED, _tbsize, theme=__theme)
        self.BMP_PLAYER_STOP            = spBitmap(PLAYER_STOP,           _tbsize, theme=__theme)
        self.BMP_PLAYER_STOP_DISABLED   = spBitmap(PLAYER_STOP_DISABLED,  _tbsize, theme=__theme)

    # -----------------------------------------------------------------------

    def __create_audio_button(self, name, preftag, bmpe, bmpd, method, sizer):
        """
        Build an audio button, iff prefs is set to True for that preftag.

        """
        bgcolour = self._prefs.GetValue('M_BG_COLOUR')
        try:
            info = self._prefs.GetValue(preftag)
        except Exception:
            info = False
        if info is True:
            #logging.info(' ... Sndplayer: create button: %s'%(name))
            self._buttons[name] = CreateButton(self, bmpd, method, sizer, colour=bgcolour)
            self._dict_buttons_enable[self._buttons[name]]  = bmpe
            self._dict_buttons_disable[self._buttons[name]] = bmpd
        #else:
        #    logging.info(' ... Sndplayer: ignore button: %s'%(name))

    # -----------------------------------------------------------------------

    def _build_showpanel(self, wave):
        """
        Build or change the show panel.

        """
        # a showpanel is already existing
        if self._showpanel is not None:
            self._showpanel.Destroy()

        if wave is None:
            # no wav: show a nice picture
            self._showpanel = wx.Panel(self, size=(320,120))
            img  = wx.Image(PLAYER_BACKGROUND, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self._showpanel, wx.ID_ANY, wx.BitmapFromImage(img))
        else:
            # a wave is given: show dynamic information while playing (clock, peakmeter, ...)
            # TO DO
            self._showpanel = wx.Panel(self, size=(320,120))
            img  = wx.Image(PLAYER_BACKGROUND, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self._showpanel, wx.ID_ANY, wx.BitmapFromImage(img))


    def _build_audioadvanced(self):
        """
        Build an advanced audio controls sizer.

        """
        # create the main sizer.
        sizer = wx.GridBagSizer(4, 4)

        # 1st column
        self.__create_audio_button('eject',  'SND_EJECT',  self.BMP_PLAYER_EJECT,  self.BMP_PLAYER_EJECT_DISABLED, self.onEject, sizer)
        self.__create_audio_button('next',   'SND_NEXT',   self.BMP_PLAYER_NEXT,   self.BMP_PLAYER_NEXT_DISABLED, self.onNext, sizer)
        self.__create_audio_button('rewind', 'SND_REWIND', self.BMP_PLAYER_REWIND, self.BMP_PLAYER_REWIND_DISABLED, self.onRewind, sizer)

        # 2nd column
        self._build_showpanel(None)

        # 3rd column
        self.__create_audio_button('play',   'SND_PLAY',   self.BMP_PLAYER_PLAY, self.BMP_PLAYER_PLAY_DISABLED, self.onNormalPlay, sizer)
        self.__create_audio_button('stop',   'SND_STOP',   self.BMP_PLAYER_STOP,   self.BMP_PLAYER_STOP_DISABLED, self.onStop, sizer)
        self.__create_audio_button('pause',  'SND_PAUSE',  self.BMP_PLAYER_PAUSE,  self.BMP_PLAYER_PAUSE_DISABLED, self.onPause, sizer)

        # 4th column
        minvalue = 0
        maxvalue = 101
        therange = 5
        self._knob = KC.KnobCtrl(self, -1, size=(80, 80))
        self._knob.SetTags(range(minvalue, maxvalue+1, therange))
        self._knob.SetAngularRange(-45, 225)
        self._knob.SetValue(int((minvalue+maxvalue+1)/2))
        tickrange = range(minvalue, maxvalue+1, therange)
        self._knob.SetTags(tickrange)
        self.Bind(KC.KC_EVENT_ANGLE_CHANGED, self.onAngleChanged, self._knob)
        self._knobtracker = wx.StaticText(self, -1, "Volume = %d" % int((minvalue+maxvalue)/2))

        # create playback slider
        self._playbackSlider = wx.Slider(self, wx.ID_ANY, size=wx.DefaultSize, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)

        # sizer
        if 'eject'  in self._buttons.keys(): sizer.Add(self._buttons['eject'],  (0,0), flag=wx.ALL, border=4)
        if 'next'   in self._buttons.keys(): sizer.Add(self._buttons['next'],   (1,0), flag=wx.ALL, border=4)
        if 'rewind' in self._buttons.keys(): sizer.Add(self._buttons['rewind'], (2,0), flag=wx.ALL, border=4)
        if 'play'   in self._buttons.keys(): sizer.Add(self._buttons['play'],   (0,2), flag=wx.ALL, border=4)
        if 'stop'   in self._buttons.keys(): sizer.Add(self._buttons['stop'],   (1,2), flag=wx.ALL, border=4)
        if 'pause'  in self._buttons.keys(): sizer.Add(self._buttons['pause'],  (2,2), flag=wx.ALL, border=4)

        sizer.Add(self._showpanel,      (0,1), (3,1), flag=wx.EXPAND|wx.ALL, border=4)
        sizer.Add(self._knob,           (0,3), (2,1), flag=wx.EXPAND|wx.TOP, border=4)
        sizer.Add(self._knobtracker,    (2,3), flag=wx.TOP, border=4)
        sizer.Add(self._playbackSlider, (3,0), (1,4), flag=wx.ALL|wx.EXPAND, border=4)

        return sizer

    #----------------------------------------------------------------------

    def _build_audiosimple(self):
        """
        Build a simple audio controls sizer.

        """
        self._showpanel      = None
        self._playbackSlider = None
        self._knob           = None
        self._knobtracker    = None

        # create the main sizer.
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.__create_audio_button('info',   'SND_INFO',   self.BMP_PLAYER_INFO, self.BMP_PLAYER_INFO_DISABLED, self.onInfo, sizer)
        self.__create_audio_button('play',   'SND_PLAY',   self.BMP_PLAYER_PLAY, self.BMP_PLAYER_PLAY_DISABLED, self.onNormalPlay, sizer)
        self.__create_audio_button('replay', 'SND_AUTOREPLAY', self.BMP_PLAYER_REPLAY, self.BMP_PLAYER_REPLAY_DISABLED, self.onAutoPlay, sizer)
        self.__create_audio_button('pause',  'SND_PAUSE',  self.BMP_PLAYER_PAUSE,  self.BMP_PLAYER_PAUSE_DISABLED, self.onPause, sizer)
        self.__create_audio_button('stop',   'SND_STOP',   self.BMP_PLAYER_STOP,   self.BMP_PLAYER_STOP_DISABLED, self.onStop, sizer)
        self.__create_audio_button('next',   'SND_NEXT',   self.BMP_PLAYER_NEXT,   self.BMP_PLAYER_NEXT_DISABLED, self.onNext, sizer)
        self.__create_audio_button('rewind', 'SND_REWIND', self.BMP_PLAYER_REWIND, self.BMP_PLAYER_REWIND_DISABLED, self.onRewind, sizer)
        self.__create_audio_button('eject',  'SND_EJECT', self.BMP_PLAYER_EJECT, self.BMP_PLAYER_EJECT_DISABLED, self.onEject, sizer)

        if 'info'   in self._buttons.keys(): sizer.Add(self._buttons['info'],   1, flag=wx.ALL, border=0)
        if 'play'   in self._buttons.keys(): sizer.Add(self._buttons['play'],   1, flag=wx.ALL, border=0)
        if 'replay' in self._buttons.keys(): sizer.Add(self._buttons['replay'], 1, flag=wx.ALL, border=0)
        if 'pause'  in self._buttons.keys(): sizer.Add(self._buttons['pause'],  1, flag=wx.ALL, border=0)
        if 'stop'   in self._buttons.keys(): sizer.Add(self._buttons['stop'],   1, flag=wx.ALL, border=0)
        if 'next'   in self._buttons.keys(): sizer.Add(self._buttons['next'],   1, flag=wx.ALL, border=0)
        if 'rewind' in self._buttons.keys(): sizer.Add(self._buttons['rewind'], 1, flag=wx.ALL, border=0)
        if 'eject'  in self._buttons.keys(): sizer.Add(self._buttons['eject'],  1, flag=wx.ALL, border=0)

        return sizer

    #-------------------------------------------------------------------------

    def _check_prefs(self, prefs):
        """
        Check if preferences are set properly.
        Set new ones if required.
        Return the new version.
        """
        if prefs is None:
            prefs = Preferences(sppasTheme())

        else:
            try:
                prefs.GetValue('M_BG_COLOUR')
                prefs.GetValue('M_FG_COLOUR')
                prefs.GetValue('M_FONT')
                prefs.GetValue('M_ICON_THEME')
            except Exception:
                self._prefsIO.SetTheme(sppasTheme())
        return prefs

    # -----------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------

    def FileSelected(self, filename):
        """
        Set a sound file.

        @param filename (string) is an audio file name (a wave is expected).

        """
        # we already opened the same file
        if filename == self._filename and self._mediaplayer is not None:
            logging.info(' ... SndPlayer: file %s was already opened. [WARNING]' % (filename))
            return

        try:
            m = wx.media.MediaCtrl(self, style=wx.NO_BORDER)
            m.Load(filename)
            self._length = m.Length()
            if self._length == 0: # **** BUG of the MediaPlayer! ****
                import wave
                w = wave.Wave_read(filename)
                self._length = int(1000 * float(w.getnframes())/float(w.getframerate()))
            logging.info(" ... File %s successfully loaded. [  OK  ]" % (filename))
        except Exception as e:
            logging.info(" ... File %s not loaded.  [ ERROR ]" % (filename))
            ShowInformation(self, self._prefs, 'Error loading: '+filename+': '+str(e), style=wx.ICON_ERROR)
            return False

        # set mediaplayer with the new one
        self._filename = filename
        self._mediaplayer = m
        self.ActivateButtons(True)
        self._offsets = (0,self._length)
        if self._playbackSlider is not None:
            self._playbackSlider.SetRange(0, self._length)
            self._playbackSlider.SetTickFreq(int(self._length/10), 1)

        self._timer.Start(self._refreshTimer)
        self.Refresh()

    # -----------------------------------------------------------------------

    def FileDeSelected(self):
        """
        Reset information.

        """
        # take care... the current mediaplayer can be playing. Unset properly!!
        if self._mediaplayer is not None and self._mediaplayer.GetState() != wx.media.MEDIASTATE_STOPPED :
            self.onStop(None)

        if self._showpanel is not None:
            self._build_showpanel(None)
        if self._mediaplayer is not None:
            self._mediaplayer.Destroy()

        self._filename    = None
        self._mediaplayer = None
        self._offsets = (0,0)
        if self._playbackSlider is not None:
            self._playbackSlider.SetRange(0, 0)

        self.ActivateButtons(False)
        self.EnableButtons(False)

        self._timer.Stop()

        self.Layout()
        self.Refresh()

    # -----------------------------------------------------------------------

    def SetOffsetPeriod(self, start, end):
        """
        Fix a start position and a end position to play the sound.

        """
        if self._mediaplayer is not None and self._mediaplayer.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.onStop(None)

        if self._mediaplayer is not None and end > self._length:
            end = self._length

        self._offsets = (start,end)
        if self._playbackSlider is not None:
            self._playbackSlider.SetRange(start,end)

    # ----------------------------------------------------------------------
    # Callbacks
    # ----------------------------------------------------------------------

    def onInfo(self, event):
        """
        Display information about the selected Wave.

        """
        if self._mediaplayer is None: return

        try:
            ShowAudioInfo(self, self._prefs, self._filename)
        except Exception as e:
            ShowInformation(self, self._prefs, 'No information available: %s'%str(e), style=wx.ICON_ERROR)

    # -------------------------------------------------------------------------

    def onSeek(self,event):
        """
        Seeks the media file according to the amount the slider has been adjusted.

        """
        if self._mediaplayer is None: return

        if self._playbackSlider is not None:
            offset = self._playbackSlider.GetValue()
        else:
            offset = self._offsets[0]

        self._mediaplayer.Seek(offset, mode=wx.FromStart)

    # ----------------------------------------------------------------------

    def onEject(self, event):
        """
        Eject the music.

        """
        if self._mediaplayer is None: return

        evt = FileWanderEvent(filename=self._filename,status=False)
        evt.SetEventObject(self)
        wx.PostEvent(self.GetParent(), evt)

        self.FileDeSelected()

    # ----------------------------------------------------------------------

    def onNext(self, event):
        """
        Go forward in the music.

        """
        if self._mediaplayer is None: return

        offset = self._mediaplayer.Tell()
        forward = offset + FORWARD_STEP
        (omin,omax) = self._offsets
        if forward > omax:
            forward = omin # come back at the beginning!

        if self._playbackSlider is not None:
            self._playbackSlider.SetValue(forward)

        self._mediaplayer.Seek(forward, mode=wx.FromStart)

    # ----------------------------------------------------------------------

    def onRewind(self, event):
        """
        Go backward in the music.

        """
        if self._mediaplayer is None:
            return

        offset = self._mediaplayer.Tell()
        backward = offset - BACKWARD_STEP
        (omin, omax) = self._offsets
        if backward < omin:
            backward = omax  # loop

        if self._playbackSlider is not None:
            self._playbackSlider.SetValue(backward)

        self._mediaplayer.Seek(backward, mode=wx.FromStart)

    # ----------------------------------------------------------------------

    def onPause(self, event):
        """
        Pauses the music.

        """
        if self._mediaplayer is None: return

        logging.debug(' PAUSE EVENT RECEIVED ')

        state = self._mediaplayer.GetState()

        if state == wx.media.MEDIASTATE_PLAYING:
            self._mediaplayer.Pause()
            if 'pause' in self._buttons.keys(): self._buttons['pause'].SetBitmapLabel(self._dict_buttons_disable[self._buttons['pause']])

        elif state == wx.media.MEDIASTATE_PAUSED:
            self.onPlay(event)
            if 'play'  in self._buttons.keys(): self._buttons['play'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['play']])
            if 'pause' in self._buttons.keys(): self._buttons['pause'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['pause']])

    # ----------------------------------------------------------------------

    def onAutoPlay(self, event):
        """
        Plays the music and re-play from the beginning.

        """
        offset = self._mediaplayer.Tell()
        self._autoreplay = True
        self.onPlay(event)

    # ----------------------------------------------------------------------

    def onNormalPlay(self, event):
        """
        Plays the music once.

        """
        self._autoreplay = False
        self.onPlay(event)

    # ----------------------------------------------------------------------

    def onPlay(self, event):
        """
        Plays the music.

        """
        if self._mediaplayer is None:
            logging.debug('onPlay. Unable to play: No media player.')
            return
        if self._mediaplayer.GetState() == wx.media.MEDIASTATE_PLAYING:
            logging.debug('onPlay. Unable to play: already playing!')
            return

        # save current position
        offset = self._mediaplayer.Tell()
        omin, omax = self._offsets
        if self._playbackSlider is not None:
            offset = self._playbackSlider.GetValue()
        elif (offset < omin or offset > omax):
            offset = omin

        if not self._mediaplayer.Play():
            logging.debug('onPlay. Unable to play. offset=%d'%offset)
            ShowInformation(self, self._prefs, "Unable to Play. Offset=%d"%offset, style=wx.ICON_ERROR)
            return

        # force to play at the good position
        self._mediaplayer.Seek(offset, mode=wx.FromStart) # required!

        if self._knob is not None:
            self._mediaplayer.SetVolume(float(self._knob.GetValue())/100.0)

        if 'play'  in self._buttons.keys(): self._buttons['play'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['play']])
        if 'pause' in self._buttons.keys(): self._buttons['pause'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['pause']])

        self.Refresh()

    # ----------------------------------------------------------------------

    def onStop(self, event):
        """
        Stops the music and resets the play button.

        """
        if self._mediaplayer is None:
            return

        try:
            self._mediaplayer.Stop()
            s, e = self._offsets
            self._mediaplayer.Seek(s)
            if self._playbackSlider is not None:
                self._playbackSlider.SetValue(s)
        except Exception:
            # provide errors like:"ressource temporairement indisponible"
            pass

        if 'play'  in self._buttons.keys(): self._buttons['play'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['play']])
        if 'pause' in self._buttons.keys(): self._buttons['pause'].SetBitmapLabel(self._dict_buttons_enable[self._buttons['pause']])
        self._autoreplay = False

    # ----------------------------------------------------------------------

    def onAngleChanged(self, event):
        """Change the volume value."""

        value = event.GetValue()
        self._knobtracker.SetLabel("Volume = " + str(value))
        if self._mediaplayer:
            self._mediaplayer.SetVolume(float(value)/100.0)

    # ----------------------------------------------------------------------

    def onTimer(self, event):
        """Keeps the player slider updated."""

        if self._mediaplayer is None: return

        offset = self._mediaplayer.Tell()
        # On MacOS, it seems that offset is not so precise we could expect...
        # It can be + or - 3 compared to the expected value!

        if self._mediaplayer.GetState() == wx.media.MEDIASTATE_PLAYING and self._playbackSlider is not None:
            self._playbackSlider.SetValue(offset)

        omin, omax = self._offsets
        if self._mediaplayer.GetState() == wx.media.MEDIASTATE_PLAYING and (offset < omin-3 or offset > omax+3):
            offset = self._mediaplayer.Tell()
            replay = self._autoreplay
            self.onStop(event)
            if replay is True:
                offset = self._mediaplayer.Tell()
                self.onAutoPlay(event)

    # ----------------------------------------------------------------------

    def onClose(self, event):
        """
        Close (destructor).

        """
        self._timer.Stop()
        self.Destroy()

    # -----------------------------------------------------------------------
    # GUI
    # -----------------------------------------------------------------------

    def SetPreferences(self, prefs):
        """
        Set new preferences.
        Do not consider changing buttons!!!

        """
        self._prefs = prefs
        self.SetBackgroundColour(self._prefs.GetValue("M_BG_COLOUR"))
        self.SetForegroundColour(self._prefs.GetValue("M_FG_COLOUR"))
        self.SetFont(self._prefs.GetValue("M_FONT"))
        # apply bg on all buttons...
        for b in self._buttons.keys():
            self._buttons[b].SetBackgroundColour(self._prefs.GetValue("M_BG_COLOUR"))

    #-------------------------------------------------------------------------


    def SetFont(self, font):
        """
        Change font of all texts.

        """
        wx.Window.SetFont(self,font)
        if self._knobtracker is not None:
            self._knobtracker.SetFont(font)

    # -----------------------------------------------------------------------

    def SetBackgroundColour(self, colour):
        """
        Change the background color of all objects.

        """
        wx.Window.SetBackgroundColour(self,colour)

        for b in self._buttons:
            self._buttons[b].SetBackgroundColour(colour)

        if self._showpanel is not None:
            self._showpanel.SetBackgroundColour(colour)
        if self._knobtracker is not None:
            self._knobtracker.SetBackgroundColour(colour)
        if self._playbackSlider is not None:
            self._playbackSlider.SetBackgroundColour(colour)

        self.Refresh()

    # -----------------------------------------------------------------------

    def SetForegroundColour(self, colour):
        """
        Change the foreground color of all objects.

        """
        wx.Window.SetForegroundColour(self,colour)

        for b in self._buttons:
            self._buttons[b].SetForegroundColour(colour)

        if self._showpanel is not None:
            self._showpanel.SetForegroundColour(colour)
        if self._knobtracker is not None:
            self._knobtracker.SetForegroundColour(colour)
        if self._playbackSlider is not None:
            self._playbackSlider.SetForegroundColour(colour)

        self.Refresh()

    # -----------------------------------------------------------------------

    def ActivateButtons(self, value=True):
        """
        Activates and enables all buttons.

        """

        self.EnableButtons(False)
        if value is True:
            for b in self._buttons:
                self._buttons[b].SetBitmapLabel(self._dict_buttons_enable[self._buttons[b]])
        else:
            for b in self._buttons:
                self._buttons[b].SetBitmapLabel(self._dict_buttons_disable[self._buttons[b]])

    # -----------------------------------------------------------------------

    def EnableButtons(self, value=True):
        """
        Enables or disables all buttons.

        """
        for b in self._buttons:
            self._buttons[b].Enable(not value)

# ----------------------------------------------------------------------------
