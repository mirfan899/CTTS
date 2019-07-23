# -*- coding:utf-8 -*-
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

    src.calculus.tests.test_stats.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..stats.central import fsum, fmult, fmin, fmax, fmean, fgeometricmean, fharmonicmean
from ..stats.frequency import freq, percent, percentile, quantile
from ..stats.linregress import tga_linear_regression, tansey_linear_regression
from ..stats.linregress import gradient_descent, gradient_descent_linear_regression, compute_error_for_line_given_points

# TODO: test the followings: lmoment, lvariation, lskew, lkurtosis, lvariance, lstdev, lz, rPVI, nPVI
# from ..stats.moment import lmoment, lvariation, lskew, lkurtosis
# from ..stats.variability import lvariance, lstdev, lz, rPVI, nPVI

# ---------------------------------------------------------------------------


class TestStats(unittest.TestCase):

    def test_central(self):
        l = [x * x for x in range(1, 500)]
        self.assertEqual(34246.72072, round(fgeometricmean(l), 5))
        self.assertEqual(303.72528, round(fharmonicmean(l), 5))
        self.assertEqual(fmean(l), 83250.0)
        self.assertEqual(fmin(l), 1)
        self.assertEqual(fmax(l), 249001)

        l = [x for x in range(1, 20, 2)]
        self.assertEqual(fsum(l), 100)
        self.assertEqual(fmult(l), 654729075)

    def test_freq(self):
        l = ['a']*3 + ['b']*5 + ['c']*8 + ['d']*4
        self.assertEqual(freq(l, 'a'), 0.15)
        self.assertEqual(freq(l, 'a'), 0.15)
        self.assertEqual(percent(l, 'a'), 15.)
        self.assertEqual(percent(l, 'z'), 0.)
        mylist = [15, 20, 40, 35, 50]
        per = percentile(mylist, p=40)
        self.assertEqual(round(per, 2), 26.0)
        qua = quantile(mylist, q=0.4)
        self.assertEqual(round(qua, 2), 26.0)

    def test_moment(self):
        pass

    def test_variability(self):
        pass

    def test_linear_regression(self):
        points = list()
        points.append((32.502345269453031, 31.70700584656992))
        points.append((53.426804033275019, 68.77759598163891))
        points.append((61.530358025636438, 62.562382297945803))
        points.append((47.475639634786098, 71.546632233567777))
        points.append((59.813207869512318, 87.230925133687393))
        points.append((55.142188413943821, 78.211518270799232))
        points.append((52.211796692214001, 79.64197304980874))
        points.append((39.299566694317065, 59.171489321869508))
        points.append((48.105041691768250, 75.331242297063056))
        points.append((52.550014442733818, 71.300879886850353))
        points.append((45.419730144973755, 55.165677145959123))
        points.append((54.351634881228918, 82.478846757497919))
        points.append((44.164049496773352, 62.008923245725825))
        points.append((58.168470716857790, 75.392870425994957))
        points.append((56.727208057096611, 81.43619215887864))
        points.append((48.955888566093719, 60.723602440673965))
        points.append((44.687196231480904, 82.892503731453715))
        points.append((60.297326851333466, 97.379896862166078))
        points.append((45.618643772955828, 48.847153317355072))
        points.append((38.816817537445637, 56.877213186268506))
        points.append((66.189816606752601, 83.878564664602763))
        points.append((65.416051745134070, 118.59121730252249))
        points.append((47.481208607867870, 57.251819462268969))
        points.append((41.575642617487020, 51.391744079832307))
        points.append((51.845186905639430, 75.380651665312357))
        points.append((59.370822011089523, 74.765564032151374))
        points.append((57.310003438348090, 95.455052922574737))
        points.append((63.615561251453308, 95.229366017555307))
        points.append((46.737619407976972, 79.052406169565586))
        points.append((50.556760148547767, 83.432071421323712))
        points.append((52.223996085553047, 63.358790317497878))
        points.append((35.567830047746632, 41.412885303700563))
        points.append((42.436476944055642, 76.617341280074044))
        points.append((58.164540110192860, 96.769566426108199))
        points.append((57.504447615341789, 74.084130116602523))
        points.append((45.440530725319981, 66.588144414228594))
        points.append((61.896222680291260, 77.768482417793024))
        points.append((33.093831736163963, 50.719588912312084))
        points.append((36.436009511386871, 62.124570818071781))
        points.append((37.675654860850742, 60.810246649902211))
        points.append((44.555608383275356, 52.682983366387781))
        points.append((43.318282631865721, 58.569824717692867))
        points.append((50.073145632289034, 82.905981485070512))
        points.append((43.870612645218372, 61.424709804339123))
        points.append((62.997480747553091, 115.24415280079529))
        points.append((32.669043763467187, 45.570588823376085))
        points.append((40.166899008703702, 54.084054796223612))
        points.append((53.575077531673656, 87.994452758110413))
        points.append((33.864214971778239, 52.725494375900425))
        points.append((64.707138666121296, 93.576118692658241))
        points.append((38.119824026822805, 80.166275447370964))
        points.append((44.502538064645101, 65.101711570560326))
        points.append((40.599538384552318, 65.562301260400375))
        points.append((41.720676356341293, 65.280886920822823))
        points.append((51.088634678336796, 73.434641546324301))
        points.append((55.078095904923202, 71.13972785861894))
        points.append((41.377726534895203, 79.102829683549857))
        points.append((62.494697427269791, 86.520538440347153))
        points.append((49.203887540826003, 84.742697807826218))
        points.append((41.102685187349664, 59.358850248624933))
        points.append((41.182016105169822, 61.684037524833627))
        points.append((50.186389494880601, 69.847604158249183))
        points.append((52.378446219236217, 86.098291205774103))
        points.append((50.135485486286122, 59.108839267699643))
        points.append((33.644706006191782, 69.89968164362763))
        points.append((39.557901222906828, 44.862490711164398))
        points.append((56.130388816875467, 85.498067778840223))
        points.append((57.362052133238237, 95.536686846467219))
        points.append((60.269214393997906, 70.251934419771587))
        points.append((35.678093889410732, 52.721734964774988))
        points.append((31.588116998132829, 50.392670135079896))
        points.append((53.660932261673040, 63.642398775657753))
        points.append((46.682228649471917, 72.247251068662365))
        points.append((43.107820219102464, 57.812512976181402))
        points.append((70.346075615049330, 104.25710158543822))
        points.append((44.492855880854073, 86.642020318822006))
        points.append((57.504533303268410, 91.486778000110135))
        points.append((36.930076609191808, 55.231660886212836))
        points.append((55.805733357942742, 79.550436678507609))
        points.append((38.954769073377065, 44.847124242467601))
        points.append((56.901214702247074, 80.207523139682763))
        points.append((56.868900661384046, 83.14274979204346))
        points.append((34.333124704216090, 55.723489260543914))
        points.append((59.049741214666810, 77.634182511677864))
        points.append((57.788223993230673, 99.051414841748269))
        points.append((54.282328705967409, 79.120646274680027))
        points.append((51.088719898979143, 69.588897851118475))
        points.append((50.282836348230731, 69.510503311494389))
        points.append((44.211741752090113, 73.687564318317285))
        points.append((38.005488008060688, 61.366904537240131))
        points.append((32.940479942618296, 67.170655768995118))
        points.append((53.691639571070056, 85.668203145001542))
        points.append((68.765734269621660, 114.85387123391394))
        points.append((46.230966498310252, 90.123572069967423))
        points.append((68.319360818255362, 97.919821035242848))
        points.append((50.030174340312143, 81.536990783015028))
        points.append((49.239765342753763, 72.111832469615663))
        points.append((50.039575939875988, 85.232007342325673))
        points.append((48.149858891028863, 66.224957888054632))
        points.append((25.128484647772304, 53.454394214850524))

        b, m = gradient_descent_linear_regression(points, num_iterations=50000)
        self.assertEqual(round(b, 4), 2.5319)
        self.assertEqual(round(m, 4), 1.4297)
        b, m = gradient_descent_linear_regression(points, num_iterations=100000)
        self.assertEqual(round(b, 4), 4.248)
        self.assertEqual(round(m, 4), 1.396)
        b, m = gradient_descent_linear_regression(points, num_iterations=200000)
        self.assertEqual(round(b, 4), 6.2314)
        self.assertEqual(round(m, 4), 1.3570)
        e = compute_error_for_line_given_points(b, m, points)
        self.assertEqual(round(e, 4), 110.3743)

        b, m = tga_linear_regression(points)
        self.assertEqual(round(b, 4), 7.9910)
        self.assertEqual(round(m, 4), 1.3224)

        b, m = tansey_linear_regression(points)
        self.assertEqual(round(b, 4), 7.9910)
        self.assertEqual(round(m, 4), 1.3224)

        b, m = gradient_descent(points, b, m, learning_rate=0.0001, num_iterations=50000)
        self.assertEqual(round(b, 4), 7.9910)
        self.assertEqual(round(m, 4), 1.3224)
