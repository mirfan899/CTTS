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

    src.annotations.FillIPUs.fillipus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from sppas.src.config import symbols

from ..SearchIPUs.searchipus import SearchIPUs

# ---------------------------------------------------------------------------

SIL_ORTHO = list(symbols.ortho.keys())[list(symbols.ortho.values()).index("silence")]

# ---------------------------------------------------------------------------


class FillIPUs(SearchIPUs):
    """Search for IPUs and fill in the IPUs with a transcription.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self, channel, units):
        """Instantiate.

        :param channel: (sppasChannel)
        :param units: (list of str) All units to fill.

        The given units can be either ipus+silences or ipus only.

        """
        super(FillIPUs, self).__init__(channel)
        self._units = units
        self._nb_ipus = len([u for u in self._units if u != SIL_ORTHO])

    # -----------------------------------------------------------------------

    def __check_boundaries(self, tracks):
        """Check if silences at start and end are as expected.

        :param tracks:
        :returns: (bool)

        """
        if len(self._units) == 0:
            return False
        if self._channel is None:
            return False

        first_from_pos = tracks[0][0]
        last_to_pos = tracks[-1][1]

        # If I expected a silence at start... and I've found a track
        if self._units[0] == SIL_ORTHO and \
                first_from_pos < 10:
            return False

        # If I expected a silence at end... and I've found a track
        if self._units[-1] == SIL_ORTHO and \
                last_to_pos > (self._channel.get_nframes()-10):
            return False

        return True

    # -----------------------------------------------------------------------

    def _split_into_vol(self):
        """Try various volume values when estimating silences.

        This method expect to find the right number of ipus and silences.
        It automatically adjusts the member vol_threshold.

        :returns: number of ipus really found

        """
        if self._channel is None:
            return 0

        vol_stats = self.get_volstats()
        # Min volume in the recorded channel
        vmin = vol_stats.min()
        # Max is set to the mean
        vmax = vol_stats.mean()
        # A volume step is necessary to not exaggerate a detailed search!
        # vstep is set to 5% of the volume between min and mean.
        vstep = int((vmax - vmin) / 20.0)
        # Min and max are adjusted
        vmin += vstep
        vmax -= vstep

        # First Test
        self._vol_threshold = vmin
        tracks = self.get_tracks(vmin)
        n = len(tracks)
        b = self.__check_boundaries(tracks)

        while n != self._nb_ipus or b is False:
            # We would never be done anyway.
            if (vmax == vmin) or (vmax-vmin) < vstep:
                return n

            # Try with the middle volume value
            vmid = int(vmin + (vmax - vmin) / 2.0)
            if n > self._nb_ipus:
                # We split too often. Need to consider less as silence.
                vmax = vmid
            elif n < self._nb_ipus:
                # We split too seldom. Need to consider more as silence.
                vmin = vmid
            else:
                # We did not find start/end silence.
                vmin += vstep

            # Find silences with these parameters
            self._vol_threshold = int(vmid)
            tracks = self.get_tracks(vmid)
            n = len(tracks)
            b = self.__check_boundaries(tracks)

        return n

    # -----------------------------------------------------------------------

    def fix_threshold_durations(self):
        """Search appropriate parameters to match the units and the channel.

        Try various volume values, pause durations and silence duration to
        search silences then tracks. Stops when the number of tracks
        automatically found is matching the number of given units.

        :returns: tracks

        """
        if self._channel is None:
            raise Exception('No audio data.')

        # Search tracks with default parameters
        self._vol_threshold = self.fix_threshold_vol()

        tracks = self.get_tracks(self._vol_threshold)
        n = len(tracks)
        b = self.__check_boundaries(tracks)
        if n == self._nb_ipus and b is True:
            return n

        # Search by changing only the volume threshold
        n = self._split_into_vol()

        if n > self._nb_ipus:
            # We split too often.
            # Search with higher minimum duration of silences and ipus
            while n > self._nb_ipus:
                self._min_sil_dur += self._win_length
                self._min_ipu_dur += self._win_length
                n = self._split_into_vol()

        elif n < self._nb_ipus:
            # We split too seldom.
            # Search with smaller minimum duration of silences and ipus
            p = self._min_sil_dur
            m = self._min_ipu_dur
            while n < self._nb_ipus and \
                    self._min_sil_dur > SearchIPUs.MIN_SIL_DUR:
                self._min_sil_dur -= self._win_length
                n = self._split_into_vol()

            # we failed... try with shorter' values of ipus
            if n < self._nb_ipus:
                self._min_sil_dur = p
                while n < self._nb_ipus and \
                        self._min_ipu_dur > SearchIPUs.MIN_IPU_DUR:
                    self._min_ipu_dur -= self._win_length
                    n = self._split_into_vol()

                # we failed... try with shorter' values of both sil/ipus
                if n < self._nb_ipus:
                    self._min_ipu_dur = m
                    while n < self._nb_ipus and \
                            self._min_sil_dur > SearchIPUs.MIN_SIL_DUR and \
                            self._min_ipu_dur > SearchIPUs.MIN_IPU_DUR:
                        self._min_ipu_dur -= self._win_length
                        self._min_sil_dur -= self._win_length
                        n = self._split_into_vol()

        return n
