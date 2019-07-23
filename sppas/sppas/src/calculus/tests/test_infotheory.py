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

    src.calculus.tests.test_infotheory.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from ..infotheory.entropy import sppasEntropy
from ..infotheory.kullbackleibler import sppasKullbackLeibler
from ..infotheory.perplexity import sppasPerplexity

# ---------------------------------------------------------------------------


class TestInformationTheory(unittest.TestCase):

    def test_entropy(self):
        entropy = sppasEntropy(list("1223334444"))

        self.assertEqual(round(entropy.eval(), 5), 1.84644)
        entropy.set_symbols(list("0000000000"))
        self.assertEqual(round(entropy.eval(), 5), 0.)
        entropy.set_symbols(list("1000000000"))
        self.assertEqual(round(entropy.eval(), 5), 0.469)
        entropy.set_symbols(list("1100000000"))
        self.assertEqual(round(entropy.eval(), 5), 0.72193)
        entropy.set_symbols(list("1110000000"))
        self.assertEqual(round(entropy.eval(), 5), 0.88129)
        entropy.set_symbols(list("1111000000"))
        self.assertEqual(round(entropy.eval(), 5), 0.97095)
        entropy.set_symbols(list("1111100000"))
        self.assertEqual(round(entropy.eval(), 5), 1.)
        entropy.set_symbols(list("1111111111"))
        self.assertEqual(round(entropy.eval(), 5), 0.)
        entropy.set_symbols(list("1111000000"))
        entropy.set_ngram(1)
        self.assertEqual(round(entropy.eval(), 5), 0.97095)
        entropy.set_ngram(2)
        self.assertEqual(round(entropy.eval(), 5), 1.35164)
        entropy.set_symbols(list("1010101010"))
        self.assertEqual(round(entropy.eval(), 5), 0.99108)
        entropy.set_symbols(list("1111100000"))
        self.assertEqual(round(entropy.eval(), 5), 1.39215)

    def test_perplexity(self):
        model = dict()
        model["peer"] = 0.1
        model["pineapple"] = 0.2
        model["tomato"] = 0.3
        model["apple"] = 0.4
        pp = sppasPerplexity(model)
        observed = ['apple', 'pineapple', 'apple', 'peer']
        self.assertEqual(round(pp.eval_pp(observed), 5), 3.61531)
        observed = ['apple', 'pineapple', 'apple', 'tomato']
        self.assertEqual(round(pp.eval_pp(observed), 5), 4.12107)
        observed = ['apple', 'grapefruit', 'apple', 'peer']
        self.assertEqual(round(pp.eval_pp(observed), 5), 2.62034)

    def test_kl1(self):
        data = list('00000011000101010000100101000101000001000100000001100000')
        kl = sppasKullbackLeibler()
        kl.set_epsilon(1.0 / (10.*len(data)))
        kl.set_model_from_data(data)
        kl.set_observations(list('000'))
        self.assertEqual(2.06851, round(kl.eval_kld(), 5))
        kl.set_observations(list('010'))
        self.assertEqual(0.06409, round(kl.eval_kld(), 5))
        kl.set_observations(list('011'))
        self.assertEqual(1.65549, round(kl.eval_kld(), 5))
        kl.set_observations(list('111'))
        self.assertEqual(10.97067, round(kl.eval_kld(), 5))

    def test_kl2(self):
        modell = dict()
        modell["a"] = 0.80
        modell["b"] = 0.08
        modell["c"] = 0.08
        modell["d"] = 0.04
        kll = sppasKullbackLeibler(modell)
        kll.set_epsilon(1. / 1000.)
        observation = list()
        observation.append("a")
        observation.append("a")
        kll.set_observations(observation)
        self.assertEqual(round(kll.eval_kld(), 5), 1.33276)
        observation.pop(0)
        observation.append("b")
        self.assertEqual(round(kll.eval_kld(), 5), 2.01852)
        observation.pop(0)
        observation.append("d")
        self.assertEqual(round(kll.eval_kld(), 5), 10.98264)

        model = dict()
        model[(0, 0)] = 0.80
        model[(0, 1)] = 0.08
        model[(1, 0)] = 0.08
        model[(1, 1)] = 0.04
        kl = sppasKullbackLeibler(model)
        kl.set_epsilon(1. / 1000.)
        observation = list()
        observation.append((0, 0))
        observation.append((0, 0))
        kl.set_observations(observation)
        self.assertEqual(round(kl.eval_kld(), 5), 1.33276)
        observation.pop(0)
        observation.append((0, 1))
        self.assertEqual(round(kl.eval_kld(), 5), 2.01852)
        observation.pop(0)
        observation.append((1, 1))
        self.assertEqual(round(kl.eval_kld(), 5), 10.98264)
