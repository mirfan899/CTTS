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

    src.annotations.tests.test_syllabify.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the SPPAS Syllabification.

"""
import unittest
import os.path

from sppas.src.config import paths
from sppas.src.anndata.anndataexc import AioEncodingError
from sppas.src.anndata import sppasTier
from sppas.src.anndata import sppasLocation
from sppas.src.anndata import sppasInterval
from sppas.src.anndata import sppasPoint
from sppas.src.anndata import sppasLabel
from sppas.src.anndata import sppasTag
from sppas.src.anndata import sppasRW

from ..Syll.syllabify import Syllabifier
from ..Syll.sppassyll import sppasSyll


# -------------------------------------------------------------------------

POL_SYLL = os.path.join(paths.resources, "syll", "syllConfig-pol.txt")
FRA_SYLL = os.path.join(paths.resources, "syll", "syllConfig-fra.txt")

# -------------------------------------------------------------------------


class TestSyllabifier(unittest.TestCase):
    """Syllabification of a list of phonemes."""

    def setUp(self):
        self.syll_pol = Syllabifier(POL_SYLL)
        self.syll_fra = Syllabifier(FRA_SYLL)

    # -----------------------------------------------------------------------

    def test_find_next_vowel(self):
        """... Search of the next vowel in classes."""

        c = ['L', 'V', 'P', 'P', 'V', 'F', 'V', 'L']
        self.assertEqual(1, Syllabifier._find_next_vowel(c, 0))
        self.assertEqual(1, Syllabifier._find_next_vowel(c, 1))
        self.assertEqual(4, Syllabifier._find_next_vowel(c, 2))
        self.assertEqual(4, Syllabifier._find_next_vowel(c, 3))
        self.assertEqual(4, Syllabifier._find_next_vowel(c, 4))
        self.assertEqual(6, Syllabifier._find_next_vowel(c, 5))
        self.assertEqual(6, Syllabifier._find_next_vowel(c, 6))
        self.assertEqual(-1, Syllabifier._find_next_vowel(c, 7))
        self.assertEqual(-1, Syllabifier._find_next_vowel(c, 8))

    # -----------------------------------------------------------------------

    def test_find_next_break(self):
        """... Search of the next break in classes."""

        c = ['L', 'V', 'P', 'P', 'V', 'F', 'V', 'L']
        self.assertEqual(-1, Syllabifier._find_next_break(c, 0))
        self.assertEqual(-1, Syllabifier._find_next_break(c, 6))

        c = ['L', 'V', 'P', 'P', 'V', '#', 'F', 'V', 'L']
        self.assertEqual(5, Syllabifier._find_next_break(c, 0))

    # -----------------------------------------------------------------------

    def test_fix_nucleus(self):
        """... Search for the next nucleus of a syllable."""

        self.assertEqual(-1, Syllabifier._fix_nucleus([], 0))
        self.assertEqual(-1, Syllabifier._fix_nucleus(['#'], 0))
        self.assertEqual(0, Syllabifier._fix_nucleus(['V'], 0))
        self.assertEqual(1, Syllabifier._fix_nucleus(['#', 'V'], 0))
        self.assertEqual(1, Syllabifier._fix_nucleus(['#', 'V'], 1))

        c = ['L', 'V', 'P', 'P', 'V', '#', 'F', 'V', 'L']
        self.assertEqual(1, Syllabifier._fix_nucleus(c, 0))
        self.assertEqual(1, Syllabifier._fix_nucleus(c, 1))
        self.assertEqual(4, Syllabifier._fix_nucleus(c, 2))
        self.assertEqual(4, Syllabifier._fix_nucleus(c, 3))
        self.assertEqual(4, Syllabifier._fix_nucleus(c, 4))
        self.assertEqual(7, Syllabifier._fix_nucleus(c, 5))

        c = ['L', 'V', 'P', '#', 'V', '#', 'P', 'V', '#', '#', 'F', 'V', 'V', 'L']
        self.assertEqual(1, Syllabifier._fix_nucleus(c, 0))
        self.assertEqual(1, Syllabifier._fix_nucleus(c, 1))
        self.assertEqual(4, Syllabifier._fix_nucleus(c, 2))
        self.assertEqual(7, Syllabifier._fix_nucleus(c, 5))

    # -----------------------------------------------------------------------

    def test_fix_start_syll(self):
        """... Search for the index of the first phoneme of the syllable."""

        c = ['L', 'V', 'P', '#', 'V', '#', 'P', 'V', '#', '#', 'F', 'V', 'V', 'L']

        self.assertEqual(0, Syllabifier._fix_start_syll(c, -1, 1))
        self.assertEqual(4, Syllabifier._fix_start_syll(c, 2, 4))
        self.assertEqual(6, Syllabifier._fix_start_syll(c, 4, 7))
        self.assertEqual(10, Syllabifier._fix_start_syll(c, 7, 11))
        self.assertEqual(12, Syllabifier._fix_start_syll(c, 11, 12))

        c = ['V', 'N', 'P', 'V']
        self.assertEqual(2, Syllabifier._fix_start_syll(c, 1, 3))

    # -----------------------------------------------------------------------

    def test_apply_class_rules(self):
        """... Apply the syllabification rules between v1 and v2."""

        # from classes
        c = ['L', 'V', 'P', 'P', 'V', 'F', 'V', 'L']
        self.assertEqual(2, self.syll_fra._apply_class_rules(c, 1, 4))
        self.assertEqual(4, self.syll_fra._apply_class_rules(c, 4, 6))

        # from phonemes
        p = ['l', '@', 'p', 't', 'i', 'S', 'A/', 'l']
        self.assertEqual(1, self.syll_fra._apply_phon_rules(p, 2, 1, 4))
        self.assertEqual(4, self.syll_fra._apply_phon_rules(p, 4, 4, 6))

    # -----------------------------------------------------------------------

    def test_annotate(self):
        """... Test creation of the syllable boundaries from a sequence of phonemes """

        # no syllable

        self.assertEqual([], self.syll_pol.annotate([]))
        self.assertEqual([], self.syll_pol.annotate(['#']))
        self.assertEqual([], self.syll_pol.annotate(['#', "#"]))
        self.assertEqual([], self.syll_pol.annotate(['m']))
        self.assertEqual([], self.syll_pol.annotate(['m', 'm']))
        self.assertEqual([], self.syll_pol.annotate(["#", 'm', 'm']))
        self.assertEqual([], self.syll_pol.annotate(["#", 'm', 'm', '#']))

        # Test situations when 1 syllable is returned.

        self.assertEqual([(0, 0)], self.syll_fra.annotate(['a']))
        self.assertEqual([(0, 0)], self.syll_fra.annotate(['a', '#']))
        self.assertEqual([(1, 1)], self.syll_fra.annotate(['#', 'a']))
        self.assertEqual([(1, 1)], self.syll_fra.annotate(['UNK', 'a']))
        self.assertEqual([(1, 1)], self.syll_fra.annotate(['UNK', 'a', '#']))

        # test VV rule

        phonemes = (['a', 'a'])
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 1)], syllables)

        phonemes = (['a', '#', 'a'])
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (2, 2)], syllables)

        # test VCV rule

        phonemes = (['a', 'b', 'a'])
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 2)], syllables)  # a.ba

        # test VCCV rules

        # VCCV general rule
        phonemes = ['a', 'n', 'c', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 1), (2, 3)], syllables)  # an.ca

        # VCCV exception rule
        phonemes = ['a', 'g', 'j', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 3)], syllables)  # a.gja

        # VCCV specific (shift to left)
        phonemes = ['a', 'd', 'g', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 3)], syllables)  # a.dga

        # VCCV do not apply the previous specific rule if not VdgV
        phonemes = ['a', 'x', 'd', 'g', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 1), (2, 4)], syllables)  # ax.dga

        # VCCV specific (shift to right)
        phonemes = ['a', 'z', 'Z', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 1), (2, 3)], syllables)  # az.Za

        # test VCCCV rule s

        # VCCCV general rule
        phonemes = ['a', 'm', 'm', 'n', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 1), (2, 4)], syllables)  # am.mna
        #
        phonemes = ['g', 'j', 'i', 't', "@"]
        syllables = self.syll_fra.annotate(phonemes)
        self.assertEqual([(0, 2), (3, 4)], syllables)  # gji.t@
        #
        phonemes = ['g', 'j', 'i', 't']
        syllables = self.syll_fra.annotate(phonemes)
        self.assertEqual([(0, 3)], syllables)  # gjit

        # VCCCV exception rule
        phonemes = ['a', 'dz', 'v', 'j', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 4)], syllables)  # a.dzvja

        # VCCCV specific (shift to left)
        phonemes = ['a', 'b', 'z', 'n', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 4)], syllables)  # a.bzna

        # VCCCV specific (shift to right)
        phonemes = ['a', 'r', 'w', 'S', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 2), (3, 4)], syllables)  # arw.Sa

        # test VCCCCV rule

        phonemes = ['a', 'b', 'r', 'v', 'j', 'a']
        syllables = self.syll_pol.annotate(phonemes)
        self.assertEqual([(0, 0), (1, 5)], syllables)  # a.brvja

        # test VCCCCCV rule

        # ... French sentence: à parce que moi.
        phonemes = ['a', 'p', 's', 'k', 'm', 'w', 'a']
        syllables = self.syll_fra.annotate(phonemes)
        self.assertEqual([(0, 3), (4, 6)], syllables)  # apsk.mwa

        # Test the limits (do not forget 't', 't-p', etc).

        self.assertEqual([(0, 3)], self.syll_fra.annotate(['g', 'j', 'i', 't']))
        self.assertEqual([(0, 4)], self.syll_fra.annotate(['g', 'j', 'i', 't', 'p']))
        self.assertEqual([(0, 4)], self.syll_fra.annotate(['g', 'j', 'i', 't', 'p', '#']))

    # -----------------------------------------------------------------------

    def test_phonetize_syllables(self):
        phonemes = ['a', 'p', 's', 'k', 'm', 'w', 'a']
        syllables = self.syll_fra.annotate(phonemes)
        self.assertEqual("a-p-s-k.m-w-a", Syllabifier.phonetize_syllables(phonemes, syllables))

# -------------------------------------------------------------------------


class TestsppasSyll(unittest.TestCase):
    """Syllabification of a tier with time-aligned phonemes."""

    def setUp(self):
        self.syll = sppasSyll()
        self.syll.load_resources(FRA_SYLL)
        tier = sppasTier('PhonAlign')
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(1), sppasPoint(2))),
                               sppasLabel(sppasTag('l')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(2), sppasPoint(3))),
                               sppasLabel(sppasTag('@')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(3), sppasPoint(4))),
                               sppasLabel(sppasTag('#')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(4), sppasPoint(5))),
                               sppasLabel(sppasTag('S')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(5), sppasPoint(6))),
                               sppasLabel(sppasTag('A/')))
        # hole [6,7]
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(7), sppasPoint(8))),
                               sppasLabel(sppasTag('#')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(8), sppasPoint(9))),
                               sppasLabel(sppasTag('e')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(9), sppasPoint(10))),
                               sppasLabel(sppasTag('#')))
        # hole [10,11]
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(11), sppasPoint(12))),
                               sppasLabel(sppasTag('k')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(12), sppasPoint(13))),
                               sppasLabel(sppasTag('2')))
        # hole [13,14]
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(14), sppasPoint(15))),
                               sppasLabel(sppasTag('p')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(15), sppasPoint(16))),
                               sppasLabel(sppasTag('U~/')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(16), sppasPoint(17))),
                               sppasLabel(sppasTag('#')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(17), sppasPoint(18))),
                               sppasLabel(sppasTag('E')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(18), sppasPoint(19))),
                               sppasLabel(sppasTag('o')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(19), sppasPoint(20))),
                               sppasLabel(sppasTag('#')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(20), sppasPoint(21))),
                               sppasLabel(sppasTag('g')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(21), sppasPoint(22))),
                               sppasLabel(sppasTag('j')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(22), sppasPoint(23))),
                               sppasLabel(sppasTag('i')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(23), sppasPoint(24))),
                               sppasLabel(sppasTag('t')))

        self.tier = tier

    # -----------------------------------------------------------------------

    def test_phon_to_intervals(self):
        """... Create the intervals to be syllabified."""

        test_tier = self.tier.copy()

        expected = sppasTier('Expected')
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(1), sppasPoint(3))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(4), sppasPoint(6))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(8), sppasPoint(9))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(11), sppasPoint(13))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(14), sppasPoint(16))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(17), sppasPoint(19))))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(20), sppasPoint(24))))

        intervals = sppasSyll._phon_to_intervals(test_tier)
        self.assertEqual(len(expected), len(intervals))
        for a1, a2 in zip(expected, intervals):
            self.assertEqual(a1, a2)

        # add en empty interval at start
        test_tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(0), sppasPoint(1))))
        intervals = sppasSyll._phon_to_intervals(test_tier)
        self.assertEqual(len(expected), len(intervals))
        for a1, a2 in zip(expected, intervals):
            self.assertEqual(a1, a2)

        # add en empty interval at end
        test_tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(24), sppasPoint(25))))
        intervals = sppasSyll._phon_to_intervals(test_tier)
        self.assertEqual(len(expected), len(intervals))
        for a1, a2 in zip(expected, intervals):
            self.assertEqual(a1, a2)

        # silence at start
        test_tier[0].append_label(sppasLabel(sppasTag('#')))
        intervals = sppasSyll._phon_to_intervals(test_tier)
        self.assertEqual(len(expected), len(intervals))
        for a1, a2 in zip(expected, intervals):
            self.assertEqual(a1, a2)

        # silence at end
        test_tier[-1].append_label(sppasLabel(sppasTag('#')))
        intervals = sppasSyll._phon_to_intervals(test_tier)
        self.assertEqual(len(expected), len(intervals))
        for a1, a2 in zip(expected, intervals):
            self.assertEqual(a1, a2)

    # -----------------------------------------------------------------------

    def test_syllabify_interval(self):
        """... Perform the syllabification of one interval."""

        expected = sppasTier('Expected')
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(1), sppasPoint(3))),
                                   sppasLabel(sppasTag('l-@')))

        syllables = sppasTier('SyllAlign')
        self.syll.syllabify_interval(self.tier, 0, 1, syllables)
        self.assertEqual(len(expected), len(syllables))
        for a1, a2 in zip(expected, syllables):
            self.assertEqual(a1, a2)

        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(17), sppasPoint(18))),
                                   sppasLabel(sppasTag('E')))
        expected.create_annotation(sppasLocation(sppasInterval(sppasPoint(18), sppasPoint(19))),
                                   sppasLabel(sppasTag('o')))
        self.syll.syllabify_interval(self.tier, 13, 15, syllables)
        self.assertEqual(len(expected), len(syllables))
        for a1, a2 in zip(expected, syllables):
            self.assertEqual(a1, a2)

    # -----------------------------------------------------------------------

    def test_convert(self):
        """... [TO DO] Syllabify labels of a time-aligned phones tier."""

        s = self.syll.convert(self.tier)

    # -----------------------------------------------------------------------

    def test_run(self):
        """... [TO DO] Test on real-life data."""

        pass

    # -----------------------------------------------------------------------

    def test_samples(self):
        """... Compare the current result is the same as the existing one."""

        # the place where are the samples to be tested.
        samples_path = os.path.join(paths.samples, "annotation-results")

        # each samples folder is tested
        for samples_folder in os.listdir(samples_path):
            if samples_folder.startswith("samples-") is False:
                continue

            # Create a Syllabifier for the given set of samples of the given language
            lang = samples_folder[-3:]
            rules_file = os.path.join(paths.resources, "syll", "syllConfig-"+lang+".txt")
            if os.path.exists(rules_file) is False:
                continue

            tn = sppasSyll()
            tn.load_resources(rules_file)

            # Apply Syllabification on each sample
            for filename in os.listdir(os.path.join(samples_path, samples_folder)):
                if filename.endswith("-palign.xra") is False:
                    continue

                # Get the expected result
                expected_result_filename = os.path.join(samples_path, samples_folder,
                                                        filename[:-11] + "-salign.xra")
                if os.path.exists(expected_result_filename) is False:
                    print("no match palign/salign for: {:s}".format(filename))
                    continue
                try:
                    parser = sppasRW(expected_result_filename)
                    expected_result = parser.read()
                except AioEncodingError:
                    continue

                # Estimate the result and check if it's like expected.
                input_file = os.path.join(samples_path, samples_folder, filename)
                result = tn.run([input_file])

                expected_tier_syll = expected_result.find('SyllAlign')
                if expected_tier_syll is not None:
                    self.compare_tiers(expected_tier_syll, result.find('SyllAlign'))

    # -----------------------------------------------------------------------

    def compare_tiers(self, expected, result):
        self.assertEqual(len(expected), len(result))
        for a1, a2 in zip(expected, result):
            self.assertEqual(a1, a2)
            for key in a1.get_meta_keys():
                if key != 'id':
                    self.assertEqual(a1.get_meta(key), a2.get_meta(key))
        for key in expected.get_meta_keys():
            if key != 'id':
                self.assertEqual(expected.get_meta(key), result.get_meta(key))
