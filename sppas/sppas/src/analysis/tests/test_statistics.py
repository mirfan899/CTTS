#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from sppas.src.anndata import sppasAnnotation
from sppas.src.anndata import sppasLabel, sppasTag
from sppas.src.anndata import sppasLocation
from sppas.src.anndata import sppasInterval
from sppas.src.anndata import sppasPoint
from sppas.src.anndata import sppasTier

from ..tierstats import sppasTierStats

# ---------------------------------------------------------------------------


class TestStatistics(unittest.TestCase):
    """Estimate descriptive statistics of annotations of a tier."""

    def setUp(self):
        self.x = sppasAnnotation(
            sppasLocation(sppasInterval(sppasPoint(1., 0.),
                                        sppasPoint(2., 0.01))),
            sppasLabel(sppasTag('toto')))
        self.y = sppasAnnotation(
            sppasLocation(sppasInterval(sppasPoint(3., 0.01),
                                        sppasPoint(4., 0.01))),
            sppasLabel(sppasTag('titi')))
        self.a = sppasAnnotation(
            sppasLocation(sppasInterval(sppasPoint(5., 0.01),
                                        sppasPoint(6.5, 0.005))),
            sppasLabel(sppasTag('toto')))
        self.b = sppasAnnotation(
            sppasLocation(sppasInterval(sppasPoint(6.5, 0.005),
                                        sppasPoint(9.5, 0.))),
            sppasLabel(sppasTag('toto')))
        self.tier = sppasTier()
        self.tier.append(self.x)
        self.tier.append(self.y)
        self.tier.append(self.a)
        self.tier.append(self.b)

    # -----------------------------------------------------------------------

    def test_TierStats(self):
        t = sppasTierStats(self.tier)
        ds = t.ds()

        occurrences = ds.len()
        self.assertEqual(3, occurrences['toto'])
        self.assertEqual(1, occurrences['titi'])

        total = ds.total()
        self.assertEqual(5.5, total['toto'])
        self.assertEqual(1.0, total['titi'])

        mean = ds.mean()
        self.assertEqual(1.833, round(mean['toto'], 3))
        self.assertEqual(1.0, mean['titi'])

        median = ds.median()
        self.assertEqual(1.5, median['toto'])
        self.assertEqual(1.0, median['titi'])

        variance = ds.variance()
        self.assertEqual(0.722, round(variance['toto'], 3))

        stdev = ds.stdev()
        self.assertEqual(0.85, round(stdev['toto'], 2))

        #coefvariation = ds.coefvariation()
        #self.assertEqual(56.773, round(coefvariation['toto'],3))
