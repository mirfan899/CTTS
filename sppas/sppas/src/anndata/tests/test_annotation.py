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

    src.anndata.tests.test_annotation.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the sppasAnnotation instance.

"""

import unittest

from sppas.src.config import symbols
from ..ann.annlocation import sppasLocation
from ..ann.annlocation import sppasInterval
from ..ann.annlocation import sppasPoint
from ..ann.annlabel import sppasTag
from ..ann.annlabel import sppasLabel
from ..ann.annotation import sppasAnnotation

# ---------------------------------------------------------------------------

SIL_PHON = list(symbols.phone.keys())[list(symbols.phone.values()).index("silence")]
SIL_ORTHO = list(symbols.ortho.keys())[list(symbols.ortho.values()).index("silence")]

# ---------------------------------------------------------------------------


class TestAnnotation(unittest.TestCase):
    """sppasAnnotation() is a container for:

        - a sppasLocation()
        - a list of sppasLabel()

    """
    def setUp(self):
        self.p1 = sppasPoint(1)
        self.p2 = sppasPoint(2)
        self.p3 = sppasPoint(3)
        self.it = sppasInterval(self.p1, self.p2)
        self.annotationI = sppasAnnotation(sppasLocation(self.it),
                                           sppasLabel(
                                               sppasTag(" \t\t  être être   être  \n ")))
        self.annotationP = sppasAnnotation(sppasLocation(self.p1),
                                           sppasLabel(
                                               sppasTag("mark")))

    # -----------------------------------------------------------------------

    def test_init(self):

        # Initialize without label
        ann = sppasAnnotation(sppasLocation(self.it))
        self.assertEqual(len(ann.get_meta_keys()), 1)
        self.assertTrue(ann.is_meta_key("id"))

    # -----------------------------------------------------------------------

    def test_get_labels(self):
        """Return the list of sppasLabel() instances."""

        # Initialize without label
        ann = sppasAnnotation(sppasLocation(self.it))
        self.assertEqual(len(ann.get_labels()), 0)

        # Initialize with one label
        ann = sppasAnnotation(sppasLocation(self.it),
                              [sppasLabel(sppasTag(''))])
        self.assertEqual(len(ann.get_labels()), 1)

        # Initialize with 2 labels
        ann = sppasAnnotation(sppasLocation(self.it),
                              [sppasLabel(sppasTag('')),
                               sppasLabel(sppasTag('a'))])
        self.assertEqual(len(ann.get_labels()), 2)

    # -----------------------------------------------------------------------

    def test_set_labels(self):
        """Fix a new list of labels for this annotation."""

        # Initialize without label
        ann = sppasAnnotation(sppasLocation(self.it))

        # Do not store None as label!
        ann.set_labels(None)
        self.assertEqual(len(ann.get_labels()), 0)

        ann.set_labels(sppasLabel(sppasTag('')))
        self.assertEqual(len(ann.get_labels()), 1)
        tag, score = ann.get_labels()[0][0]
        self.assertEqual(sppasTag(''), tag)

        ann.set_labels()
        self.assertEqual(len(ann.get_labels()), 0)

        ann.set_labels([sppasLabel(sppasTag('')), sppasLabel(sppasTag(""))])
        self.assertEqual(len(ann.get_labels()), 2)
        tag1, score1 = ann.get_labels()[0][0]  # first tag of the first label
        self.assertEqual(sppasTag(''), tag1)
        tag2, score2 = ann.get_labels()[1][0]  # first tag of the second label
        self.assertEqual(sppasTag(''), tag2)

    # -----------------------------------------------------------------------

    def test_copy(self):
        """Return a full copy of the annotation."""

        a = sppasAnnotation(sppasLocation(self.it), sppasLabel(sppasTag("#")))
        clone = a.copy()
        self.assertTrue(clone == a)
        self.assertEqual(clone, a)

    # -----------------------------------------------------------------------

    def test_is_silence(self):
        self.assertFalse(self.annotationP.get_best_tag().is_silence())
        self.assertFalse(self.annotationI.get_best_tag().is_silence())

        self.annotationI.get_best_tag().set(sppasTag(SIL_ORTHO))
        self.annotationP.get_best_tag().set(sppasTag(SIL_PHON))
        self.assertTrue(self.annotationI.get_best_tag().is_silence())
        self.assertTrue(self.annotationP.get_best_tag().is_silence())

    # -----------------------------------------------------------------------
    # location
    # -----------------------------------------------------------------------

    def test_get_begin(self):
        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_begin()

    # -----------------------------------------------------------------------

    def test_set_begin(self):
        with self.assertRaises(ValueError):
            self.annotationI.get_location().get_best().set_begin(self.p3)

        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_best().set_begin(self.p2)

    # -----------------------------------------------------------------------

    def test_get_begin_value(self):
        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_best().get_begin().get_content()

        with self.assertRaises(ValueError):
            self.annotationI.get_location().get_best().set_begin(sppasPoint(4))

        # *** SHOULD BE FORBIDDEN... but in the long long long "to do" list
        self.annotationI.get_location().get_best().get_begin().set_midpoint(4)

    # -----------------------------------------------------------------------

    def test_get_end(self):
        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_best().get_end()

    # -----------------------------------------------------------------------

    def test_get_end_value(self):
        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_best().get_end().set_midpoint()

    # -----------------------------------------------------------------------

    def test_set_end(self):
        with self.assertRaises(ValueError):
            self.annotationI.get_location().get_best().set_end(self.p1)

        with self.assertRaises(AttributeError):
            self.annotationP.get_location().get_best().set_end(self.p2)

    # -----------------------------------------------------------------------

    def test_get_point(self):
        with self.assertRaises(AttributeError):
            self.annotationI.get_location().get_best().get_point()

    # -----------------------------------------------------------------------

    def test_get_point_value(self):
        with self.assertRaises(AttributeError):
            self.annotationI.get_location().get_best().get_point().get_content()

    # -----------------------------------------------------------------------

    def test_set_point(self):
        with self.assertRaises(AttributeError):
            self.annotationI.get_location().get_best().set_point(self.p3)

    # -----------------------------------------------------------------------

    def test_is_point(self):
        self.assertFalse(self.annotationI.get_location().get_best().is_point())
        self.assertTrue(self.annotationP.get_location().get_best().is_point())

    # -----------------------------------------------------------------------

    def test_is_interval(self):
        self.assertTrue(self.annotationI.get_location().get_best().is_interval())
        self.assertFalse(self.annotationP.get_location().get_best().is_interval())

    # -----------------------------------------------------------------------

    def test_contains(self):
        self.assertTrue(self.annotationI.contains_localization(sppasPoint(1)))
        self.assertFalse(self.annotationI.contains_localization(sppasPoint(10)))

    # -----------------------------------------------------------------------

    def test_get_highest_localization(self):
        p1 = sppasPoint(1)
        p2 = sppasPoint(2)
        p3 = sppasPoint(3)
        it = sppasLocation([sppasInterval(p1, p2), sppasInterval(p1, p3)])
        a = sppasAnnotation(it)
        highest = a.get_highest_localization()
        self.assertEqual(highest, p3)
        # get_highest_localization returns a copy so we won't change the point!
        a.get_highest_localization().set(sppasPoint(4.))
        self.assertEqual(a.get_highest_localization(), highest)

