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

    src.anndata.tests.test_aio_phonedit
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the reader/writer of SPPAS for MRK files.

"""
import unittest
import os.path

from sppas.src.utils.makeunicode import u

from ..aio.phonedit import sppasBasePhonedit
from ..aio.phonedit import sppasMRK
from ..aio.phonedit import sppasSignaix

from ..ann.annlocation import sppasPoint

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------


class TestBasePhonedit(unittest.TestCase):
    """
    Base Phonedit is mainly made of utility methods.

    """
    def test_members(self):
        txt = sppasBasePhonedit()
        self.assertTrue(txt.multi_tiers_support())
        self.assertFalse(txt.no_tiers_support())
        self.assertFalse(txt.metadata_support())
        self.assertFalse(txt.ctrl_vocab_support())
        self.assertFalse(txt.media_support())
        self.assertFalse(txt.hierarchy_support())
        self.assertTrue(txt.point_support())
        self.assertTrue(txt.interval_support())
        self.assertFalse(txt.disjoint_support())
        self.assertFalse(txt.alternative_localization_support())
        self.assertFalse(txt.alternative_tag_support())
        self.assertFalse(txt.radius_support())
        self.assertTrue(txt.gaps_support())
        self.assertTrue(txt.overlaps_support())

# ---------------------------------------------------------------------------


class TestMRK(unittest.TestCase):
    """
    Test reader/writer of MRK files.

    """
    def test_detect(self):
        """Test the file format detection method."""

        for filename in os.listdir(DATA):
            f = os.path.join(DATA, filename)
            if filename.endswith('.mrk'):
                self.assertTrue(sppasMRK.detect(f))
            else:
                self.assertFalse(sppasMRK.detect(f))

    # -----------------------------------------------------------------

    def test_make_point(self):
        """Convert data into the appropriate digit type, or not."""

        self.assertEqual(sppasPoint(3., 0.0005), sppasMRK.make_point("3000."))
        self.assertEqual(sppasPoint(3., 0.0005), sppasMRK.make_point("3000."))
        self.assertEqual(sppasPoint(3), sppasMRK.make_point("3000"))
        with self.assertRaises(TypeError):
            sppasMRK.make_point("3a")

    # -----------------------------------------------------------------

    def test_read(self):
        """Sample mrk."""

        mrk = sppasMRK()
        mrk.read(os.path.join(DATA, "sample.mrk"))
        self.assertEqual(len(mrk), 2)
        self.assertEqual(len(mrk.get_media_list()), 0)
        self.assertEqual(mrk[0].get_name(), u("transcription"))
        self.assertEqual(mrk[1].get_name(), u("ipus"))
        self.assertEqual(len(mrk[0]), 11)
        self.assertEqual(len(mrk[1]), 11)
        for i, ann in enumerate(mrk[1]):
            if i % 2:
                ipu_index = int(i/2) + 1
                self.assertEqual(ann.get_labels()[0].get_best().get_content(),
                                 u("ipu_"+str(ipu_index)))
            else:
                self.assertEqual(ann.get_labels()[0].get_best().get_content(),
                                 u("#"))

# ---------------------------------------------------------------------------


class TestSignaix(unittest.TestCase):
    """
    Test reader/writer of MRK files.

    """
    def test_detect(self):
        """Test the file format detection method."""

        for filename in os.listdir(DATA):
            f = os.path.join(DATA, filename)
            if filename.endswith('.hz'):
                self.assertTrue(sppasSignaix.detect(f))
            else:
                self.assertFalse(sppasSignaix.detect(f))

    # -----------------------------------------------------------------------

    def test_members(self):

            txt = sppasSignaix()
            self.assertFalse(txt.multi_tiers_support())
            self.assertFalse(txt.no_tiers_support())
            self.assertFalse(txt.metadata_support())
            self.assertFalse(txt.ctrl_vocab_support())
            self.assertFalse(txt.media_support())
            self.assertFalse(txt.hierarchy_support())
            self.assertTrue(txt.point_support())
            self.assertFalse(txt.interval_support())
            self.assertFalse(txt.disjoint_support())
            self.assertFalse(txt.alternative_localization_support())
            self.assertFalse(txt.alternative_tag_support())
            self.assertFalse(txt.radius_support())
            self.assertFalse(txt.gaps_support())
            self.assertFalse(txt.overlaps_support())

    # -----------------------------------------------------------------------

    def test_read(self):
        """Test file reader."""

        hz = sppasSignaix()
        hz.read(os.path.join(DATA, "sample.hz"))
        self.assertEqual(len(hz), 1)
        self.assertEqual(len(hz.get_media_list()), 0)
        self.assertEqual(hz[0].get_name(), u("Pitch"))
        self.assertTrue(hz[0].is_point())
        self.assertTrue(hz[0].is_float())
