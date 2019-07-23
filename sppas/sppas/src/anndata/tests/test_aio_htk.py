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

    src.anndata.tests.test_aio_htk
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test for reading and writing HTK files.

"""
import unittest
import os.path

from ..aio.htk import sppasBaseHTK
from ..aio.htk import sppasLab

from ..ann.annlocation import sppasInterval
from ..ann.annlocation import sppasPoint
from ..ann.annlabel import sppasTag
from ..ann.annlabel import sppasLabel
from ..ann.annotation import sppasAnnotation
from ..ann.annlocation import sppasLocation

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------


class TestBaseHTK(unittest.TestCase):
    """
    Base text is mainly made of utility methods.

    """
    def test_members(self):
        txt = sppasBaseHTK()
        self.assertFalse(txt.multi_tiers_support())
        self.assertTrue(txt.no_tiers_support())
        self.assertFalse(txt.metadata_support())
        self.assertFalse(txt.ctrl_vocab_support())
        self.assertFalse(txt.media_support())
        self.assertFalse(txt.hierarchy_support())
        self.assertFalse(txt.point_support())
        self.assertTrue(txt.interval_support())
        self.assertFalse(txt.disjoint_support())
        self.assertFalse(txt.alternative_localization_support())
        self.assertFalse(txt.alternative_tag_support())
        self.assertFalse(txt.radius_support())
        self.assertTrue(txt.gaps_support())
        self.assertFalse(txt.overlaps_support())

    # -----------------------------------------------------------------

    def test_make_point(self):
        """Convert data into the appropriate digit type, or not."""

        self.assertEqual(sppasPoint(3., 0.005), sppasBaseHTK.make_point("30000000"))
        with self.assertRaises(ValueError):
            sppasBaseHTK.make_point("3a")

    # -----------------------------------------------------------------

    def test_serialize_annotation(self):
        """Test annotation -> lines in lab file."""

        # No label
        a1 = sppasAnnotation(sppasLocation(sppasInterval(sppasPoint(1.), sppasPoint(3.5))))
        self.assertEqual(sppasBaseHTK._serialize_annotation(a1), "")

        # Empty tag
        a1 = sppasAnnotation(sppasLocation(sppasInterval(sppasPoint(1.), sppasPoint(3.5))),
                             sppasLabel(sppasTag("")))
        self.assertEqual(sppasBaseHTK._serialize_annotation(a1), "")

        # Localization is points
        a1 = sppasAnnotation(sppasLocation(sppasPoint(1.)), sppasLabel(sppasTag('a')))
        with self.assertRaises(TypeError):
            sppasBaseHTK._serialize_annotation(a1)

        # Normal situations
        a = sppasAnnotation(sppasLocation(sppasInterval(sppasPoint(1.), sppasPoint(3.5))),
                            sppasLabel(sppasTag('a')))
        self.assertEqual(sppasBaseHTK._serialize_annotation(a), "10000000 35000000 a\n")
        a1 = sppasAnnotation(sppasLocation(sppasInterval(sppasPoint(1.), sppasPoint(3.5))),
                             sppasLabel(sppasTag('a b c')))
        self.assertEqual(sppasBaseHTK._serialize_annotation(a1), "10000000 a\nb\nc\n")

# ---------------------------------------------------------------------


class TestLab(unittest.TestCase):
    """
    Represents a lab file reader/writer.

    """
    def test_read(self):
        """Test of reading a LAB sample file."""

        txt = sppasLab()
        txt.read(os.path.join(DATA, "sample.lab"))
        self.assertEqual(len(txt), 1)
        self.assertEqual(len(txt[0]), 6)
        # location
        self.assertEqual(sppasPoint(0.), txt[0].get_first_point())
        self.assertEqual(sppasPoint(0.82, 0.005), txt[0].get_last_point())
        # labels
        self.assertEqual(sppasTag("ay"), txt[0][0].get_best_tag())
        self.assertEqual(sppasTag("s"), txt[0][1].get_best_tag())
        self.assertEqual(sppasTag("k"), txt[0][2].get_best_tag())
        self.assertEqual(sppasTag("r"), txt[0][3].get_best_tag())
        self.assertEqual(sppasTag("iy"), txt[0][4].get_best_tag())
        self.assertEqual(sppasTag("m"), txt[0][5].get_best_tag())
        l = txt[0][4].get_labels()[0]
        self.assertEqual(0.45, l.get_score(l.get_best()))
