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

    src.audiodata.tests.test_audioconvert.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest
import os

from sppas.src.config import paths
from ..aio import open as audio_open
from ..audioconvert import sppasAudioConverter

sample_1 = os.path.join(paths.samples, "samples-eng", "oriana1.wav")
sample_2 = os.path.join(paths.samples, "samples-fra", "F_F_B003-P9.wav")
sample_3 = os.path.join(paths.samples, "samples-eng", "oriana3.wave")

# ---------------------------------------------------------------------------


class TestAudioUtils(unittest.TestCase):

    def setUp(self):
        self._sample_1 = audio_open(sample_1)
        self._sample_2 = audio_open(sample_2)
        self._sample_3 = audio_open(sample_3)

    def tearDown(self):
        self._sample_1.close()
        self._sample_2.close()
        self._sample_3.close()

    def test_Samples2Frames(self):
        s1 = self._sample_1.read_samples(10)
        s2 = self._sample_2.read_samples(10)
        s3 = self._sample_3.read_samples(10)
        self._sample_1.rewind()
        self._sample_2.rewind()
        self._sample_3.rewind()
        f1 = sppasAudioConverter().samples2frames(s1, self._sample_1.get_sampwidth(), self._sample_1.get_nchannels())
        f2 = sppasAudioConverter().samples2frames(s2, self._sample_2.get_sampwidth(), self._sample_2.get_nchannels())
        f3 = sppasAudioConverter().samples2frames(s3, self._sample_3.get_sampwidth(), self._sample_3.get_nchannels())

        self.assertEqual(self._sample_1.read_frames(10), f1)
        self.assertEqual(self._sample_2.read_frames(10), f2)
        self.assertEqual(self._sample_3.read_frames(10), f3)

        self.assertEqual(s1, [[1, -1, 1, 1, 0, 0, -1, 1, -1, 1]])
        self.assertEqual(s2, [[82, 72, 51, 64, 57, 47, 53, 39, 6, 51]])
        self.assertEqual(s3, [[0, 1, 1, 0, 1, -2, 2, -1, 1, -2], [0, 1, -5, 5, -8, 14, -76, -169, -139, -149]])

    def test_Frames2Samples(self):
        f1 = self._sample_1.read_frames(10)
        self._sample_1.rewind()
        f2 = self._sample_2.read_frames(10)
        self._sample_2.rewind()
        f3 = self._sample_3.read_frames(10)
        self._sample_3.rewind()
        s1 = sppasAudioConverter().unpack_data(f1, self._sample_1.get_sampwidth(), self._sample_1.get_nchannels())
        s2 = sppasAudioConverter().unpack_data(f2, self._sample_2.get_sampwidth(), self._sample_2.get_nchannels())
        s3 = sppasAudioConverter().unpack_data(f3, self._sample_2.get_sampwidth(), self._sample_3.get_nchannels())

        self.assertEqual(s1, [[1, -1, 1, 1, 0, 0, -1, 1, -1, 1]])
        self.assertEqual(s2, [[82, 72, 51, 64, 57, 47, 53, 39, 6, 51]])
        self.assertEqual(s3, [[0, 1, 1, 0, 1, -2, 2, -1, 1, -2], [0, 1, -5, 5, -8, 14, -76, -169, -139, -149]])

    def test_frames_and_samples(self):
        f1 = self._sample_1.read_frames(10)
        self._sample_1.rewind()
        f2 = self._sample_2.read_frames(10)
        self._sample_2.rewind()
        f3 = self._sample_3.read_frames(10)
        self._sample_3.rewind()

        s1 = sppasAudioConverter().unpack_data(f1, self._sample_1.get_sampwidth(), self._sample_1.get_nchannels())
        s2 = sppasAudioConverter().unpack_data(f2, self._sample_2.get_sampwidth(), self._sample_2.get_nchannels())
        s3 = sppasAudioConverter().unpack_data(f3, self._sample_2.get_sampwidth(), self._sample_3.get_nchannels())
        f1c = sppasAudioConverter().samples2frames(s1, self._sample_1.get_sampwidth(), self._sample_1.get_nchannels())
        f2c = sppasAudioConverter().samples2frames(s2, self._sample_2.get_sampwidth(), self._sample_2.get_nchannels())
        f3c = sppasAudioConverter().samples2frames(s3, self._sample_3.get_sampwidth(), self._sample_3.get_nchannels())

        self.assertEqual(f1, f1c)
        self.assertEqual(f2, f2c)
        self.assertEqual(f3, f3c)

    def test_db(self):
        """Test amp2db."""
        self.assertEqual(70, sppasAudioConverter().amp2db(3162))
        self.assertEqual(46.02, sppasAudioConverter().amp2db(200))
        self.assertEqual(40, sppasAudioConverter().amp2db(100))
        self.assertEqual(10, sppasAudioConverter().amp2db(3.162))
        self.assertEqual(9.54, sppasAudioConverter().amp2db(3))
        self.assertEqual(0., sppasAudioConverter().amp2db(2))

    def test_mel(self):
        """Test hz2mel/mel2hz."""
        hz = 200
        mel = sppasAudioConverter().hz2mel(hz)
        rehz = sppasAudioConverter().mel2hz(mel)
        self.assertEqual(hz, rehz)
