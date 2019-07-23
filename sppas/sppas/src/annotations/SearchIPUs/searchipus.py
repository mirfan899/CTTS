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

    src.annotations.searchipus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from .silences import sppasSilences

# ---------------------------------------------------------------------------


class SearchIPUs(sppasSilences):
    """An automatic silence/tracks segmentation system.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Silence/tracks segmentation aims at finding IPUs.
    IPUs - Inter-Pausal Units are blocks of speech bounded by silent pauses
    of more than X ms, and time-aligned on the speech signal.

    """

    MIN_SIL_DUR = 0.06
    MIN_IPU_DUR = 0.06
    DEFAULT_MIN_SIL_DUR = 0.250
    DEFAULT_MIN_IPU_DUR = 0.300
    DEFAULT_VOL_THRESHOLD = 0
    DEFAULT_SHIFT_START = 0.02
    DEFAULT_SHIFT_END = 0.02

    def __init__(self, channel, win_len=0.02):
        """Create a new SearchIPUs instance.

        :param channel: (sppasChannel)

        """
        super(SearchIPUs, self).__init__(channel, win_len, win_len / 4.)

        self._win_length = win_len
        self._min_sil_dur = SearchIPUs.DEFAULT_MIN_SIL_DUR
        self._min_ipu_dur = SearchIPUs.DEFAULT_MIN_IPU_DUR
        self._vol_threshold = SearchIPUs.DEFAULT_VOL_THRESHOLD
        self._auto_threshold = SearchIPUs.DEFAULT_VOL_THRESHOLD
        self._shift_start = SearchIPUs.DEFAULT_SHIFT_START
        self._shift_end = SearchIPUs.DEFAULT_SHIFT_END

    # -----------------------------------------------------------------------
    # Manage Channel
    # -----------------------------------------------------------------------

    def get_track_data(self, tracks):
        """Return the audio data of tracks.

        :param tracks: List of tracks. A track is a tuple (start, end).
        :returns: List of audio data

        """
        return self.track_data(tracks)

    # -----------------------------------------------------------------------

    def get_channel(self):
        """Return the channel."""
        return self._channel

    # -----------------------------------------------------------------------
    # Getters for members
    # -----------------------------------------------------------------------

    def get_win_length(self):
        """Return the windows length used to estimate the RMS."""
        return self._win_length

    def get_vol_threshold(self):
        """Return the initial volume threshold used to search for silences."""
        return self._vol_threshold

    def get_effective_threshold(self):
        """Return the threshold volume estimated automatically to search for silences."""
        return self._auto_threshold

    def get_min_sil_dur(self):
        """Return the minimum duration of a silence."""
        return self._min_sil_dur

    def get_min_ipu_dur(self):
        """Return the minimum duration of a track."""
        return self._min_ipu_dur

    def get_shift_start(self):
        return self._shift_start

    def get_shift_end(self):
        return self._shift_end

    # -----------------------------------------------------------------------
    # Setters for members
    # -----------------------------------------------------------------------

    def set_win_length(self, w):
        """Set a new length of window for a estimation or volume values.

        TAKE CARE:
        it cancels any previous estimation of volume and silence search.

        :param w: (float) between 0.01 and 0.04.

        """
        self._win_length = max(float(w), 0.002)

        if self._channel is not None:
            self.set_channel(self._channel)

    # -----------------------------------------------------------------------

    def set_vol_threshold(self, vol_threshold):
        """Fix the default minimum volume value to find silences.

        It won't affect the current list of silence values. Use search_sil().

        :param vol_threshold: (int) RMS value

        """
        self._vol_threshold = int(vol_threshold)
        if self._vol_threshold < 0:
            self._vol_threshold = SearchIPUs.DEFAULT_VOL_THRESHOLD

    # -----------------------------------------------------------------------

    def set_min_sil(self, min_sil_dur):
        """Fix the default minimum duration of a silence.

        :param min_sil_dur: (float) Duration in seconds.

        """
        self._min_sil_dur = max(
            float(min_sil_dur),
            SearchIPUs.MIN_SIL_DUR
        )

    # -----------------------------------------------------------------------

    def set_min_ipu(self, min_ipu_dur):
        """Fix the default minimum duration of an IPU.

        :param min_ipu_dur: (float) Duration in seconds.

        """
        self._min_ipu_dur = max(
            float(min_ipu_dur),
            SearchIPUs.MIN_IPU_DUR
        )

    # -----------------------------------------------------------------------

    def set_shift_start(self, s):
        """Fix the default minimum boundary shift value.

        :param s: (float) Duration in seconds.

        """
        s = float(s)
        if -self._min_ipu_dur < s < self._min_sil_dur:
            self._shift_start = s

    # -----------------------------------------------------------------------

    def set_shift_end(self, s):
        """Fix the default minimum boundary shift value.

        :param s: (float) Duration in seconds.

        """
        s = float(s)
        if -self._min_ipu_dur < s < self._min_sil_dur:
            self._shift_end = s

    # -----------------------------------------------------------------------

    def min_channel_duration(self):
        """Return the minimum duration we expect for a channel."""
        d = max(self._min_sil_dur, self._min_ipu_dur)
        return d + self._shift_start + self._shift_end

    # -----------------------------------------------------------------------

    def get_rms_stats(self):
        """Return min, max, mean, median, stdev of the RMS."""
        vs = self.get_volstats()
        return [vs.min(), vs.max(), vs.mean(), vs.median(), vs.coefvariation()]

    # -----------------------------------------------------------------------
    # Silence/Speech segmentation
    # -----------------------------------------------------------------------

    def get_tracks(self, time_domain=False):
        """Return a list of tuples (from,to) of tracks.

        (from,to) values are converted, or not, into the time-domain.

        The tracks are found from the current list of silences, which is
        firstly filtered with the min_sil_dur.

        This methods requires the following members to be fixed:
            - the volume threshold
            - the minimum duration for a silence,
            - the minimum duration for a track,
            - the duration to remove to the start boundary,
            - the duration to add to the end boundary.

        :param time_domain: (bool) Convert from/to values in seconds
        :returns: (list of tuples) with (from,to) of the tracks

        """
        # Search for the silences, comparing each rms to the threshold
        self._auto_threshold = self.search_silences(self._vol_threshold)

        # Keep only silences during more than a given duration
        # remove silences first because we are interested in finding tracks
        self.filter_silences(self._auto_threshold, self._min_sil_dur)

        # Get the (from_pos, to_pos) of the tracks during more than
        # a given duration and shift these values (from-start; to+end)
        tracks = self.extract_tracks(self._min_ipu_dur,
                                     self._shift_start,
                                     self._shift_end)

        # Convert the (from_pos, to_pos) of tracks into (from_time, to_time)
        if time_domain is True:
            time_tracks = []
            for i, (from_pos, to_pos) in enumerate(tracks):
                f = float(from_pos) / float(self._channel.get_framerate())
                t = float(to_pos) / float(self._channel.get_framerate())
                time_tracks.append((f, t))
            return time_tracks

        return tracks
