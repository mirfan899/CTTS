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

    src.audiodata.tests.test_channelformatter.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest
import os.path

from sppas.src.config import paths
from ..aio import open as audio_open
from ..channelformatter import sppasChannelFormatter

# ---------------------------------------------------------------------------

sample_1 = os.path.join(paths.samples, "samples-eng", "oriana1.wav")  # mono; 16000Hz; 16bits
sample_2 = os.path.join(paths.samples, "samples-fra", "F_F_B003-P9.wav")  # mono; 44100Hz; 32bits

# ---------------------------------------------------------------------------


class TestChannelFormatter(unittest.TestCase):

    def setUp(self):
        self._sample_1 = audio_open(sample_1)
        self._sample_2 = audio_open(sample_2)

    def tearDown(self):
        self._sample_1.close()
        self._sample_2.close()

    def test_Sync(self):
        self._sample_1.extract_channel(0)
        self._sample_2.extract_channel(0)

        channel = self._sample_1.get_channel(0)

        formatter = sppasChannelFormatter(self._sample_2.get_channel(0))
        formatter.sync(channel)

        self.assertEqual(channel.get_framerate(), formatter.get_channel().get_framerate())
        self.assertEqual(channel.get_sampwidth(), formatter.get_channel().get_sampwidth())
