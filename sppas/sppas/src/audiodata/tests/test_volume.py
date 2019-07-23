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

    src.audiodata.tests.test_volume.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest
import os.path

from sppas.src.config import paths
from ..aio import open as audio_open
from ..channelvolume import sppasChannelVolume
from ..audiovolume import sppasAudioVolume

# ---------------------------------------------------------------------------

sample_1 = os.path.join(paths.samples, "samples-eng", "oriana1.wav")  # mono; 16000Hz; 16bits

# ---------------------------------------------------------------------------


class TestVolume(unittest.TestCase):

    def test_rms(self):
        audio = audio_open(sample_1)
        cidx = audio.extract_channel(0)
        channel = audio.get_channel(cidx)

        chanvol = sppasChannelVolume(channel)
        audiovol = sppasAudioVolume(audio)

        self.assertEqual(chanvol.volume(), channel.rms())
        self.assertEqual(audiovol.volume(), audio.rms())
        self.assertEqual(chanvol.len(), int(channel.get_duration()/0.01) + 1)
        self.assertEqual(chanvol.min(), audiovol.min())
        self.assertEqual(chanvol.max(), audiovol.max())
        self.assertEqual(int(chanvol.mean()), int(audiovol.mean()))
        self.assertEqual(int(chanvol.variance()), int(audiovol.variance()))
        self.assertEqual(int(chanvol.stdev()), int(audiovol.stdev()))
