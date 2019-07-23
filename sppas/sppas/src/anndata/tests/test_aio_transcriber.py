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

    src.anndata.tests.test_aio_transcriber
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the class sppasTRS().

    To read files from Transcriber.

"""
import unittest
import os.path
import xml.etree.cElementTree as ET

from ..aio.transcriber import sppasTRS
from ..ann.annlocation import sppasPoint
from ..ann.annlabel import sppasTag
from ..ann.annlocation import sppasInterval
from ..ann.annlabel import sppasLabel
from ..ann.annlocation import sppasLocation

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------


class TestTranscriber(unittest.TestCase):
    """
    Base text is mainly made of utility methods.

    """
    def test_members(self):
        txt = sppasTRS()
        self.assertTrue(txt.multi_tiers_support())
        self.assertFalse(txt.no_tiers_support())
        self.assertTrue(txt.metadata_support())
        self.assertFalse(txt.ctrl_vocab_support())
        self.assertTrue(txt.media_support())
        self.assertTrue(txt.hierarchy_support())
        self.assertFalse(txt.point_support())
        self.assertTrue(txt.interval_support())
        self.assertFalse(txt.disjoint_support())
        self.assertFalse(txt.alternative_localization_support())
        self.assertFalse(txt.alternative_tag_support())
        self.assertFalse(txt.radius_support())
        self.assertFalse(txt.gaps_support())
        self.assertFalse(txt.overlaps_support())

    # -----------------------------------------------------------------

    def test_make_point(self):
        """Convert data into the appropriate digit type, or not."""

        self.assertEqual(sppasPoint(3., 0.005), sppasTRS.make_point("3.0"))
        self.assertEqual(sppasPoint(3., 0.005), sppasTRS.make_point("3."))
        self.assertEqual(sppasPoint(3., 0.005), sppasTRS.make_point("3"))
        with self.assertRaises(TypeError):
            sppasTRS.make_point("3a")

    # -----------------------------------------------------------------

    def test_parse_metadata(self):
        """Test metadata."""

        # All attributes filled
        trs_attribs = '<Trans scribe="Alice" ' \
                      'audio_filename="ESLO2_ENT_6" ' \
                      'version="28" ' \
                      'version_date="101129" ' \
                      'xml:lang = "fr" ' \
                      'elapsed_time="29" >' \
                      '<Episode></Episode>' \
                      '</Trans>'
        root = ET.fromstring(trs_attribs)
        trs = sppasTRS()
        trs._parse_metadata(root)
        # audio_filename ( --> Media)
        self.assertEqual(len(trs.get_media_list()), 1)
        # annotator
        self.assertTrue(trs.is_meta_key('annotator_name'))
        self.assertEqual(trs.get_meta('annotator_name'), "Alice")
        # version/date
        self.assertTrue(trs.is_meta_key('annotator_version'))
        self.assertEqual(trs.get_meta('annotator_version'), "28")
        self.assertTrue(trs.is_meta_key('annotator_version_date'))
        self.assertEqual(trs.get_meta('annotator_version_date'), "101129")
        # elapsed_time: not extracted
        self.assertFalse(trs.is_meta_key('elapsed_time'))

        # No attribute filled
        trs_attribs = '<Trans scribe="Alice"> '\
                      '</Trans>'
        root = ET.fromstring(trs_attribs)
        trs = sppasTRS()
        trs._parse_metadata(root)

    # -----------------------------------------------------------------

    def test_parse_speakers(self):
        """Test speakers."""

        spks = '<Speakers> <Speaker ' \
               'id = "spk1" ' \
               'name = "ch_NS3" ' \
               'check = "no" ' \
               'dialect = "native" ' \
               'accent = "" ' \
               'scope = "local" /> <Speaker ' \
               'id = "spk2" ' \
               'name = "OS6" ' \
               'check = "no" ' \
               'dialect = "native" ' \
               'accent = "" ' \
               'scope = "local" /> </Speakers>'

        root = ET.fromstring(spks)
        trs = sppasTRS()
        trs._parse_speakers(root)

        self.assertEqual(len(trs), 2)
        self.assertEqual(len(trs[0]), 0)
        self.assertEqual(len(trs[1]), 0)
        self.assertEqual(trs[0].get_name(), "Trans-spk1")
        self.assertEqual(trs[1].get_name(), "Trans-spk2")

        self.assertEqual(trs[0].get_meta('speaker_name'), "ch_NS3")
        self.assertEqual(trs[1].get_meta('speaker_name'), "OS6")
        self.assertEqual(trs[0].get_meta('speaker_check'), "no")
        self.assertEqual(trs[0].get_meta('speaker_dialect'), "native")
        self.assertEqual(trs[0].get_meta('speaker_accent'), "")
        self.assertEqual(trs[0].get_meta('speaker_scope'), "local")

    # -----------------------------------------------------------------

    def test_parse_topics(self):
        """Test Topics."""

        topics = '<Topics> '\
                 '<Topic id="to1" desc="S14"/> ' \
                 '<Topic id="to2" /> ' \
                 '</Topics>'

        root = ET.fromstring(topics)
        trs = sppasTRS()
        topics = trs.create_tier('Topics')
        sppasTRS._parse_topics(root, topics)

        ctrl = trs.get_ctrl_vocab_from_name("topics")
        self.assertEqual(topics.get_ctrl_vocab(), ctrl)
        self.assertTrue(ctrl.contains(sppasTag("to1")))
        self.assertTrue(ctrl.contains(sppasTag("to2")))
        self.assertFalse(ctrl.contains(sppasTag("to3")))
        self.assertEqual(ctrl.get_tag_description(sppasTag("to1")), "S14")
        self.assertEqual(ctrl.get_tag_description(sppasTag("to2")), "")

    # -----------------------------------------------------------------

    def test_parse_section(self):
        """Test Section."""

        sections = '<Episode> ' \
                   ' <Section type="report" startTime="0" endTime="32.114" topic="to1"> </Section>' \
                   ' <Section type="nontrans" startTime="34.736" endTime="39.609"> </Section>' \
                   ' <Section type="report" startTime="103.202" endTime="157.738"> </Section>' \
                   ' <Section type="filler" startTime="9.609" endTime="10.790"> </Section>' \
                   '</Episode> '

        root = ET.fromstring(sections)
        trs = sppasTRS()
        topics = trs.create_tier('Topics')
        sections = trs.create_tier('Sections')
        for section_root in root.iter('Section'):
            trs._parse_section_attributes(section_root, sections)

        self.assertEqual(len(trs), 2)
        self.assertIsNotNone(topics)
        self.assertTrue(len(topics), 1)
        self.assertTrue(len(sections), 4)

    # -----------------------------------------------------------------

    def test_parse_turn_attributes(self):
        """Test Turn."""

        turns = '<Section type="report" startTime="0" endTime="32.114" topic="to1"> ' \
                '<Turn speaker="spk1 spk2" startTime="0.000" endTime="0.387"> </Turn> '\
                '<Turn startTime="4.736" endTime="9.609" ' \
                ' mode="spontaneous" ' \
                ' fidelity="medium" ' \
                ' channel="studio"> </Turn> ' \
                '<Turn speaker="spk2" startTime="18.909" endTime="31.568"> </Turn> ' \
                '</Section>'

        root = ET.fromstring(turns)
        trs = sppasTRS()
        trs.create_tier('Trans-spk1')
        trs.create_tier('Trans-spk2')
        trs.create_tier('Topics')
        trs.create_tier('Turns')
        for turn_root in root.iter('Turn'):
            trs._parse_turn_attributes(turn_root)

        self.assertEqual(len(trs), 7)
        tier = trs.find('TurnChannel')
        self.assertIsNotNone(tier)
        self.assertEqual(len(tier), 1)
        self.assertEqual(tier[0].get_location(),
                         sppasLocation(sppasInterval(
                             sppasPoint(4.736, 0.005),
                             sppasPoint(9.609, 0.005))),
                         sppasLabel(sppasTag("studio")))
        tier = trs.find('TurnRecordingQuality')
        self.assertIsNotNone(tier)
        self.assertEqual(len(tier), 1)
        self.assertEqual(tier[0].get_location(),
                         sppasLocation(sppasInterval(
                             sppasPoint(4.736, 0.005),
                             sppasPoint(9.609, 0.005))),
                         sppasLabel(sppasTag("medium")))
        tier = trs.find('TurnElocutionMode')
        self.assertIsNotNone(tier)
        self.assertEqual(len(tier), 1)
        self.assertEqual(tier[0].get_location(),
                         sppasLocation(sppasInterval(
                             sppasPoint(4.736, 0.005),
                             sppasPoint(9.609, 0.005))),
                         sppasLabel(sppasTag("spontaneous")))

    # -----------------------------------------------------------------

    def test_parse_turn_emptied(self):
        """Test Turn."""

        turns = '<Section type="report" startTime="0" endTime="32.114" topic="to1"> ' \
                '<Turn speaker="spk1 spk2" startTime="0.000" endTime="0.387"> </Turn> '\
                '<Turn startTime="4.736" endTime="9.609" ' \
                ' mode="spontaneous" ' \
                ' fidelity="medium" ' \
                ' channel="studio"> </Turn> ' \
                '<Turn speaker="spk2" startTime="18.909" endTime="31.568"> </Turn> ' \
                '</Section>'

        root = ET.fromstring(turns)
        trs = sppasTRS()
        trs.create_tier('Trans-spk1')
        trs.create_tier('Trans-spk2')
        trs.create_tier('Topics')
        turns = trs.create_tier('Turns')
        for turn_root in root.iter('Turn'):
            trs._parse_turn(turn_root)

        self.assertEqual(len(turns), 3)

    # -----------------------------------------------------------------

    def test_parse_turn_filled(self):
        """Test Turn."""

        turns = '<Section type="report" startTime="0" endTime="32.114" topic="to1"> ' \
                '<Turn speaker="spk1 spk2" startTime="0.000" endTime="0.387"> </Turn> '\
                '<Turn startTime="4.736" endTime="9.609" ' \
                ' mode="spontaneous" ' \
                ' fidelity="medium" ' \
                ' channel="studio"> </Turn> ' \
                '<Turn speaker="spk2" startTime="18.909" endTime="31.568"> </Turn> ' \
                '</Section>'

        root = ET.fromstring(turns)
        trs = sppasTRS()

    # -----------------------------------------------------------------

    def test_read_demo(self):
        """Demo in the transcriber package ."""

        trs = sppasTRS()
        trs.read(os.path.join(DATA, "sample-demo.trs"))

        # One episode in the example
        episodes = trs.find('Episodes')
        self.assertIsNotNone(episodes)
        self.assertEqual(len(episodes), 1)

        # One topic
        topics = trs.find('Topics')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1)

        # Four sections
        sections = trs.find('Sections')
        self.assertIsNotNone(sections)
        self.assertEqual(len(sections), 4)

        # Five turns
        turns = trs.find('Turns')
        self.assertIsNotNone(turns)
        self.assertEqual(len(turns), 5)

        # Spk1
        spk1 = trs.find('Trans-sp1')
        self.assertEqual(len(spk1), 9)

        # Spk2
        spk2 = trs.find('Trans-sp2')
        self.assertEqual(len(spk2), 2)

        # No speaker
        spk0 = trs.find('Trans-NoSpeaker')
        self.assertEqual(len(spk0), 1)

    # -----------------------------------------------------------------

    def test_read_example(self):
        """Real-life file."""

        trs = sppasTRS()
        trs.read(os.path.join(DATA, "20000410_0930_1030_rfi_fm_dga.trs"))

        # One episode in the example
        episodes = trs.find('Episodes')
        self.assertIsNotNone(episodes)
        self.assertEqual(len(episodes), 1)

        # topic
        topics = trs.find('Topics')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 8)

        # sections
        sections = trs.find('Sections')
        self.assertIsNotNone(sections)
        self.assertEqual(len(sections), 15)

        # turns
        turns = trs.find('Turns')
        self.assertIsNotNone(turns)
        self.assertEqual(len(turns), 208)

        # No speaker
        spk0 = trs.find('Trans-NoSpeaker')
        self.assertEqual(len(spk0), 26)

