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

    src.anndata.tests.test_aio_audacity
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the reader of SPPAS for Audacity files.

"""
import unittest
import os.path
import xml.etree.cElementTree as ET

from ..aio.audacity import sppasAudacity
from ..ann.annlocation import sppasPoint
from ..ann.annlabel import sppasTag

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------


class TestAudacity(unittest.TestCase):
    """
    Test reader of Audacity project files.

    """
    def test_members(self):
        txt = sppasAudacity()
        self.assertTrue(txt.multi_tiers_support())
        self.assertTrue(txt.no_tiers_support())
        self.assertTrue(txt.metadata_support())
        self.assertFalse(txt.ctrl_vocab_support())
        self.assertTrue(txt.media_support())
        self.assertFalse(txt.hierarchy_support())
        self.assertTrue(txt.point_support())
        self.assertTrue(txt.interval_support())
        self.assertFalse(txt.disjoint_support())
        self.assertFalse(txt.alternative_localization_support())
        self.assertFalse(txt.alternative_tag_support())
        self.assertFalse(txt.radius_support())
        self.assertTrue(txt.gaps_support())
        self.assertTrue(txt.overlaps_support())

    # -----------------------------------------------------------------------

    def test_detect(self):
        """Test the file format detection method."""

        for filename in os.listdir(DATA):
            f = os.path.join(DATA, filename)
            if filename.endswith('.aup'):
                self.assertTrue(sppasAudacity.detect(f))
            else:
                self.assertFalse(sppasAudacity.detect(f))

    # -----------------------------------------------------------------------

    def test_make_point(self):
        """Convert data into the appropriate digit type, or not."""

        self.assertEqual(sppasPoint(3., 0.0005), sppasAudacity.make_point("3.0"))
        self.assertEqual(sppasPoint(3., 0.0005), sppasAudacity.make_point("3."))
        self.assertEqual(sppasPoint(3., 0.0005), sppasAudacity.make_point("3"))
        with self.assertRaises(TypeError):
            sppasAudacity.make_point("3a")

    # -----------------------------------------------------------------------

    def test_parse_metadata(self):
        """Test metadata."""

        # All attributes filled
        trs_attribs = '<project xmlns="http://audacity.sourceforge.net/xml/" ' \
                'projname="AC track_0379_data" '\
                'version="1.3.0" '\
                'audacityversion="2.1.2" '\
                'sel0="0.5688525050" '\
                'sel1="0.5688525050" '\
                'vpos="0" '\
                'h="0.0000000000" '\
                'zoom="430.6916078473" '\
                'rate="16000.0" '\
                'snapto="off" '\
                'selectionformat="hh:mm:ss + milliseconds" frequencyformat="Hz" bandwidthformat="octaves"> </project>'
        root = ET.fromstring(trs_attribs)
        trs = sppasAudacity()
        trs._parse_metadata(root)

        # not implemented method

    # -----------------------------------------------------------------------

    def test_parse_tags(self):
        """Test tags."""

        # not implemented method
        pass

    # -----------------------------------------------------------------------

    def test_parse_labeltrack_intervals(self):
        """Test tier creation from a labeltrack."""

        label = '<labeltrack name="Piste de marqueurs" numlabels="3" height="73" minimized="0" isSelected="0"> ' \
                '<label t="0.6013583624" t1="0.8799799975" title="label1"/> ' \
                '<label t="0.8799799975" t1="1.6206491775" title="label2"/> ' \
                '<label t="1.4883039008" t1="1.9805354561" title="label3"/> ' \
                '</labeltrack>'
        root = ET.fromstring(label)
        trs = sppasAudacity()
        trs._parse_labeltrack(root)
        self.assertEqual(len(trs), 1)
        self.assertEqual(len(trs[0]), 3)
        self.assertEqual(trs[0][0].get_labels()[0].get_best(), sppasTag('label1'))
        self.assertEqual(trs[0][1].get_labels()[0].get_best(), sppasTag('label2'))
        self.assertEqual(trs[0][2].get_labels()[0].get_best(), sppasTag('label3'))
        self.assertTrue(trs[0].is_interval())

    # -----------------------------------------------------------------------

    def test_parse_labeltrack_points(self):
        """Test tier creation from a labeltrack."""

        label = '<labeltrack name="Piste de marqueurs" numlabels="3" height="73" minimized="0" isSelected="0"> ' \
                '<label t="0.6013583624" t1="0.6013583624" title="label1"/> ' \
                '<label t="0.8799799975" t1="0.8799799975" title="label2"/> ' \
                '<label t="1.4883039008" t1="1.4883039008" title="label3"/> ' \
                '</labeltrack>'
        root = ET.fromstring(label)
        trs = sppasAudacity()
        trs._parse_labeltrack(root)
        self.assertEqual(len(trs), 1)
        self.assertEqual(len(trs[0]), 3)
        self.assertEqual(trs[0][0].get_labels()[0].get_best(), sppasTag('label1'))
        self.assertEqual(trs[0][1].get_labels()[0].get_best(), sppasTag('label2'))
        self.assertEqual(trs[0][2].get_labels()[0].get_best(), sppasTag('label3'))
        self.assertTrue(trs[0].is_point())

    # -----------------------------------------------------------------------

    def test_parse_labeltrack_mixed(self):
        """Test tier creation from a labeltrack."""

        label = '<labeltrack name="Piste de marqueurs" numlabels="3" height="73" minimized="0" isSelected="0"> ' \
                '<label t="0.6013583624" t1="0.6013583624" title="label1"/> ' \
                '<label t="0.8799799975" t1="1.8799799975" title="label2"/> ' \
                '<label t="1.4883039008" t1="1.4883039008" title="label3"/> ' \
                '</labeltrack>'
        root = ET.fromstring(label)
        trs = sppasAudacity()
        trs._parse_labeltrack(root)
        self.assertEqual(len(trs), 2)
        self.assertEqual(len(trs[1]), 2)
        self.assertEqual(len(trs[0]), 1)
        self.assertEqual(trs[1][0].get_labels()[0].get_best(), sppasTag('label1'))
        self.assertEqual(trs[1][1].get_labels()[0].get_best(), sppasTag('label3'))
        self.assertEqual(trs[0][0].get_labels()[0].get_best(), sppasTag('label2'))
        self.assertTrue(trs[1].is_point())
        self.assertTrue(trs[0].is_interval())

    # -----------------------------------------------------------------------

    def test_parse_wavetrack(self):
        """Test tier creation from a labeltrack."""

        # not implemented method
        pass

    # -----------------------------------------------------------------------

    def test_parse_timetrack(self):
        """Test tier creation from a labeltrack."""

        # not implemented method
        pass

    # -----------------------------------------------------------------------

    def test_read(self):
        """Test reader of a .aup file."""

        trs = sppasAudacity()
        trs.read(os.path.join(DATA, "sample.aup"))
        self.assertEqual(len(trs), 3)
        self.assertTrue(trs[0].is_interval())
        self.assertTrue(trs[1].is_interval())
        self.assertEqual(len(trs[0]), 3)
        self.assertEqual(len(trs[1]), 1)
        self.assertEqual(len(trs[1]), 1)
