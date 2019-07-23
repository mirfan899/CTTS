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

    src.annotations.tests.test_normalize.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Test the SPPAS implementation of TGA.

"""
import unittest
import os.path

from ..TGA import sppasTGA
from ..TGA import TimeGroupAnalysis
from sppas.src.anndata import sppasRW
from sppas.src.anndata import sppasTranscription
from sppas.src.anndata import sppasTier
from sppas.src.anndata import sppasTag
from sppas.src.anndata import sppasLabel
from sppas.src.anndata import sppasLocation, sppasInterval, sppasPoint

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# --------------------------------------------------------------------------


class TestTGA(unittest.TestCase):
    """Test of the class TimeGroupAnalysis.

    """
    def setUp(self):
        self.tg_dur = dict()
        self.tg_dur["tg1"] = [0.1, 0.2, 0.3]  # deceleration
        self.tg_dur["tg2"] = [0.1, 0.3, 0.2]  # deceleration then acceleration
        self.tg_dur["tg3"] = [0.3, 0.2, 0.1]  # acceleration

    # -----------------------------------------------------------------------

    def test_tga_estimator(self):
        ts = TimeGroupAnalysis(self.tg_dur)

        self.assertEqual(len(self.tg_dur), len(ts.len()))
        self.assertEqual(3, ts.len()["tg1"])  # nb of occurrences of tg1
        self.assertEqual(3, ts.len()["tg2"])
        self.assertEqual(3, ts.len()["tg3"])

        self.assertEqual(0.6, ts.total()["tg1"])  # total duration of tg1
        self.assertEqual(0.6, ts.total()["tg2"])
        self.assertEqual(0.6, ts.total()["tg3"])

        self.assertEqual(0.2, round(ts.mean()["tg1"], 2))  # mean duration of tg1
        self.assertEqual(0.2, round(ts.mean()["tg2"], 2))
        self.assertEqual(0.2, round(ts.mean()["tg3"], 2))

        self.assertEqual(0.2, round(ts.median()["tg1"], 2))  # median duration of tg1
        self.assertEqual(0.3, round(ts.median()["tg2"], 2))
        self.assertEqual(0.2, round(ts.median()["tg3"], 2))

        # stdev = sqrt(variance) ; variance = sum(value-mean)^2 / N
        # the use of N = for a population, not a sample (with N-1).
        self.assertEqual(0.0816, round(ts.stdev()["tg1"], 4))  # stdev duration of tg1
        self.assertEqual(0.0816, round(ts.stdev()["tg2"], 4))
        self.assertEqual(0.0816, round(ts.stdev()["tg3"], 4))

        # the higher value, the higher variability
        self.assertEqual(53, int(ts.nPVI()["tg1"]))
        self.assertEqual(70, int(ts.nPVI()["tg2"]))
        self.assertEqual(53, int(ts.nPVI()["tg3"]))

        # linear regression

        # original, x=rank of the syllable
        self.assertEqual(0.1, round(ts.intercept_slope_original()["tg1"][0], 2))  # intercept
        self.assertEqual(0.1, round(ts.intercept_slope_original()["tg1"][1], 2))  # slope
        self.assertEqual(0.15, round(ts.intercept_slope_original()["tg2"][0], 2))
        self.assertEqual(0.05, round(ts.intercept_slope_original()["tg2"][1], 2))
        self.assertEqual(0.3, round(ts.intercept_slope_original()["tg3"][0], 2))
        self.assertEqual(-0.1, round(ts.intercept_slope_original()["tg3"][1], 2))

        # annotationpro, x=timestamp of the syllable (first syll=0)
        self.assertEqual(0.11, round(ts.intercept_slope()["tg1"][0], 2))  # intercept
        self.assertEqual(0.64, round(ts.intercept_slope()["tg1"][1], 2))  # slope
        self.assertEqual(0.18, round(ts.intercept_slope()["tg2"][0], 2))
        self.assertEqual(0.12, round(ts.intercept_slope()["tg2"][1], 2))
        self.assertEqual(0.31, round(ts.intercept_slope()["tg3"][0], 2))
        self.assertEqual(-0.39, round(ts.intercept_slope()["tg3"][1], 2))

    # -----------------------------------------------------------------------

    def test_tier_tga(self):
        tier = sppasTier("tier")
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(0., 0.), sppasPoint(1., 0.0))),
                               sppasLabel(sppasTag('#')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(1., 0.), sppasPoint(2., 0.01))),
                               sppasLabel(sppasTag('toto')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(3., 0.01), sppasPoint(4., 0.01))),
                               sppasLabel(sppasTag('titi')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(4., 0.01), sppasPoint(5., 0.01))))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(5., 0.01), sppasPoint(6.5, 0.005))),
                               sppasLabel(sppasTag('toto')))
        tier.create_annotation(sppasLocation(sppasInterval(sppasPoint(6.5, 0.005), sppasPoint(9.5, 0.))),
                               sppasLabel(sppasTag('toto')))

        # test the timegroups tier
        tg = sppasTGA().syllables_to_timegroups(tier)
        self.assertEqual(3, len(tg))
        # to be tested:
        #  [1., 2.] tg_1
        #  [3.; 4.] tg_2
        #  [5.; 9.5] tg_3

        ts = sppasTGA().syllables_to_timesegments(tier)
        self.assertEqual(3, len(ts))
        # to be tested:
        #  [1., 2.] toto
        #  [3.; 4.] titi
        #  [5.; 9.5] toto toto

        tg_dur = sppasTGA().timegroups_to_durations(tier, tg)
        self.assertEqual(3, len(tg_dur))
        self.assertEqual([1.], tg_dur['tg_1'])
        self.assertEqual([1.], tg_dur['tg_2'])
        self.assertEqual([1.5, 3.0], tg_dur['tg_3'])

        tga = TimeGroupAnalysis(tg_dur)

        occurrences = tga.len()
        self.assertEqual(1, occurrences['tg_1'])
        self.assertEqual(1, occurrences['tg_2'])
        self.assertEqual(2, occurrences['tg_3'])

        total = tga.total()
        self.assertEqual(1.0, total['tg_1'])
        self.assertEqual(1.0, total['tg_2'])
        self.assertEqual(4.5, total['tg_3'])

        mean = tga.mean()
        self.assertEqual(1.0, mean['tg_1'])
        self.assertEqual(1.0, mean['tg_2'])
        self.assertEqual(2.25, mean['tg_3'])

    # -----------------------------------------------------------------------

    def test_TGA_on_sample(self):

        # This is one of the samples proposed in-line by Dafydd
        path = os.path.join(DATA, "tga.TextGrid")
        parser = sppasRW(path)
        trs = parser.read()
        tier = trs.find('Syllables')
        t = sppasTGA()

        timegroups = t.syllables_to_timegroups(tier)
        tg_dur = t.timegroups_to_durations(tier, timegroups)
        tga = TimeGroupAnalysis(tg_dur)

        occurrences = tga.len()
        self.assertEqual(34, len(occurrences))
        total = tga.total()
        mean = tga.mean()
        median = tga.median()
        stdev = tga.stdev()
        npvi = tga.nPVI()
        reglin = tga.intercept_slope_original()

        self.assertEqual(3,    occurrences['tg_1'])
        self.assertEqual(0.57, round(total['tg_1'], 2))
        self.assertEqual(0.19, round(mean['tg_1'], 2))
        self.assertEqual(0.14, round(median['tg_1'], 2))
        self.assertEqual(0.13928, round(stdev['tg_1'], 5))
        self.assertEqual(94, round(npvi['tg_1'], 0))
        i, s = reglin['tg_1']
        self.assertEqual(0.025, round(i, 3))
        self.assertEqual(0.165, round(s, 3))

        self.assertEqual(4, occurrences['tg_33'])
        self.assertEqual(0.78, round(total['tg_33'], 2))
        self.assertEqual(0.195, round(mean['tg_33'], 3))
        self.assertEqual(0.06062, round(stdev['tg_33'], 5))
        self.assertEqual(53, round(npvi['tg_33'], 0))
        i, s = reglin['tg_33']
        self.assertEqual(0.156, round(i, 3))
        self.assertEqual(0.026, round(s, 3))

        # do the job from a tier
        trs1 = t.convert(tier)
        t.set_intercept_slope_annotationpro(True)
        t.set_intercept_slope_original(False)
        self.assertEqual(10, len(trs1))

        # do the same from the file
        trs2 = t.run([path])
        self.assertEqual(10, len(trs2))

        # we should test the content of the TGA result!
