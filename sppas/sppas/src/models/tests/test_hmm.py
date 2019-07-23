# -*- coding:utf-8 -*-

import unittest
import os

from sppas.src.utils.compare import sppasCompare

from ..acm.hmm import sppasHMM, HMMInterpolation
from ..acm.acmodelhtkio import sppasHtkIO

# ---------------------------------------------------------------------------

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------


class TestHMMModel(unittest.TestCase):

    def test_init(self):
        model = sppasHMM()
        self.assertEqual(model.name, sppasHMM.DEFAULT_NAME)
        self.assertEqual(model.definition['state_count'], 0)
        self.assertEqual(len(model.definition['states']), 0)
        self.assertEqual(len(model.definition['transition']), 0)

    def test_name(self):
        model = sppasHMM()
        model.name = "test0"
        self.assertEqual(model.name, "test0")
        model.set_name("test1")
        self.assertEqual(model.name, "test1")
        with self.assertRaises(TypeError):
            model.name = 123

    def test_definition(self):
        model = sppasHMM()
        model.definition['toto'] = "N'importe quoi"

    def test_sp(self):
        model = sppasHMM()
        model.create_sp()
        self.assertEqual(model.get_vecsize(), 0)
        # ... because state is the macro "silst".

    def test_proto(self):
        model = sppasHMM()
        model.create_proto(25)
        self.assertEqual(25, model.get_vecsize())
        model.create_proto(39)
        self.assertEqual(model.get_vecsize(), 39)

    def test_create(self):
        pass

    def test_get_state(self):
        model = sppasHMM()
        model.create_proto(25)
        self.assertIsNone(model.get_state(0))
        self.assertIsNone(model.get_state(1))
        s2 = model.get_state(2)
        s3 = model.get_state(3)
        s4 = model.get_state(4)
        self.assertEqual(s2, s3)
        self.assertEqual(s2, s4)

# ---------------------------------------------------------------------------


class TestHMMinterpolation(unittest.TestCase):

    def setUp(self):
        self.vec1 = [0, 0.2, 0.8, 0]
        self.vec2 = [0, 0.4, 0.6, 0]
        self.lin = HMMInterpolation()

    def test_interpolate_vector(self):
        v = self.lin.linear_interpolate_vectors([self.vec1, self.vec2], [1, 0])
        self.assertEqual(v, self.vec1)
        v = self.lin.linear_interpolate_vectors([self.vec1, self.vec2], [0, 1])
        self.assertEqual(v, self.vec2)
        v = self.lin.linear_interpolate_vectors([self.vec1, self.vec2], [0.5, 0.5])
        v = [round(value, 1) for value in v]
        self.assertEqual(v, [0, 0.3, 0.7, 0])

    def test_interpolate_matrix(self):
        mat1 = [self.vec1, self.vec1]
        mat2 = [self.vec2, self.vec2]
        m = self.lin.linear_interpolate_matrix([mat1, mat2], [1, 0])
        self.assertEqual(m, mat1)
        m = self.lin.linear_interpolate_matrix([mat1, mat2], [0, 1])
        self.assertEqual(m, mat2)
        m = self.lin.linear_interpolate_matrix([mat1, mat2], [0.5, 0.5])
        m[0] = [round(value, 1) for value in m[0]]
        m[1] = [round(value, 1) for value in m[1]]
        self.assertEqual(m, [[0, 0.3, 0.7, 0], [0, 0.3, 0.7, 0]])

    def test_interpolate_hmm(self):

        acmodel1 = sppasHtkIO()
        acmodel1.read_macros_hmms([os.path.join(DATA, "1-hmmdefs")])
        acmodel2 = sppasHtkIO()
        acmodel2.read_macros_hmms([os.path.join(DATA, "2-hmmdefs")])
        ahmm1 = acmodel1.get_hmm('a')
        ahmm2 = acmodel2.get_hmm('a')
        sp = sppasCompare()

        # transitions
        # (notice that the transition of 'a' in acmodel1 is in a macro.)
        a1transition = [macro["transition"] for macro in acmodel1.get_macros() if macro.get('transition', None)][0]
        transitions = [a1transition['definition'], ahmm2.definition['transition']]
        trs = self.lin.linear_transitions(transitions, [1, 0])
        sp.equals(trs, a1transition['definition'])
        self.assertTrue(sp.equals(trs, a1transition['definition']))

        acmodel1.fill_hmms()

        transitions = [ahmm1.definition['transition'], ahmm2.definition['transition']]
        trs = self.lin.linear_transitions(transitions, [1, 0])
        self.assertTrue(sp.equals(trs, ahmm1.definition['transition']))

        trs = self.lin.linear_transitions(transitions, [0, 1])
        self.assertTrue(sp.equals(trs, ahmm2.definition['transition']))

        # states
        # (notice that the state 2 of 'a' in acmodel1 is in a macro.)
        states = [ahmm1.definition['states'], ahmm2.definition['states']]
        sts = self.lin.linear_states(states, [1, 0])
        self.assertTrue(sp.equals(sts, ahmm1.definition['states']))
        sts = self.lin.linear_states(states, [0, 1])
        self.assertTrue(sp.equals(sts, ahmm2.definition['states']))
