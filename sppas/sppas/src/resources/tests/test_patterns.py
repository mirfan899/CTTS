# -*- coding: utf8 -*-
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

    src.resources.tests.test_patterns.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..patterns import sppasPatterns

# ---------------------------------------------------------------------------


class TestsppasPatterns(unittest.TestCase):

    def setUp(self):
        self._patterns = sppasPatterns()

    def test_set_score(self):
        self.assertEqual(self._patterns.get_score(), 1.)
        self._patterns.set_score(0.9)
        self.assertEqual(self._patterns.get_score(), 0.9)
        with self.assertRaises(ValueError):
            self._patterns.set_score(-1.)
            self._patterns.set_score(2.)

    def test_set_ngram(self):
        self.assertEqual(self._patterns.get_ngram(), 3)
        self._patterns.set_ngram(2)
        self.assertEqual(self._patterns.get_ngram(), 2)
        with self.assertRaises(ValueError):
            self._patterns.set_score(0)
            self._patterns.set_score(5)

    def test_set_gap(self):
        self.assertEqual(self._patterns.get_gap(), 2)
        self._patterns.set_gap(1)
        self.assertEqual(self._patterns.get_gap(), 1)
        with self.assertRaises(ValueError):
            self._patterns.set_gap(-1)
            self._patterns.set_gap(5)

    def test_ngram_alignments(self):
        ref = ["w0", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10", "w11", "w12"]
        hyp = [("w0", 0.8), ("w1", 1), ("w2", 0.7), ("wX", 0.9), ("w3", 1), ("w5", 0.4), ("w6", 0.95), ("wX", 1), ("w9", 1)]

        self._patterns.set_ngram(3)
        self._patterns.set_gap(1)
        self.assertEqual([(0, 0), (1, 1), (2, 2)], self._patterns.ngram_alignments(ref, hyp))

        self._patterns.set_ngram(2)
        self._patterns.set_gap(1)
        self.assertEqual([(0, 0), (1, 1), (2, 2), (5, 5), (6, 6)], self._patterns.ngram_alignments(ref, hyp))

        self._patterns.set_ngram(1)
        self._patterns.set_score(0.9)

        self._patterns.set_gap(0)
        self.assertEqual([(1, 1), (6, 6)], self._patterns.ngram_alignments(ref, hyp))
        self._patterns.set_gap(1)
        self.assertEqual([(1, 1), (3, 4), (6, 6), (9, 8)], self._patterns.ngram_alignments(ref, hyp))
        self._patterns.set_gap(2)
        self.assertEqual([(1, 1), (3, 4), (6, 6), (9, 8)], self._patterns.ngram_alignments(ref, hyp))

        self._patterns.set_score(0.5)
        self._patterns.set_gap(1)
        self.assertEqual([(0,0), (1,1), (2,2), (3,4), (6,6), (9,8)], self._patterns.ngram_alignments(ref, hyp))

    def test_ngram_alignments_repeats(self):
        ref = ["喀", "早晨", "係", "係", "係", "喀", "我"]
        hyp = [("兩", 0.207), ("兩", 0.369), ("兩", 0.536), ("係", 0.165), ("係", 0.201), ("係", 0.193), ("係", 0.172), ("係", 0.182)]

        self._patterns.set_gap(2)
        self._patterns.set_ngram(3)
        # print self._patterns.ngram_alignments(ref,hyp)
        self._patterns.set_ngram(2)
        # print self._patterns.ngram_alignments(ref,hyp)

    def test_ngram_matches(self):
        ref = ["wa", "wb", "w0", "wa", "wX", "w0", "w1", "w2", "w3", "w4", "w5", "w6", "w7",  "w8", "w9", "w10", "w11", "w12", "wX", "wX"]
        hyp = [("w0", 0.8), ("w1", 1), ("w2", 0.7), ("wX", 0.9), ("w3", 1), ("w5", 0.4), ("w6", 0.95), ("wX", 1), ("w9", 1)]

        self.assertEqual([(5, 0), (6, 1), (7, 2)], self._patterns.ngram_matches(ref, hyp))
