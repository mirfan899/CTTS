#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os.path
import shutil

from sppas.src.config import paths
from sppas.src.models.acm.acmodel import sppasAcModel
from sppas.src.models.acm.hmm import sppasHMM
from sppas.src.models.acm.modelmixer import sppasModelMixer
from ..acm.readwrite import sppasACMRW

# ---------------------------------------------------------------------------

MODELDIR = os.path.join(paths.resources, "models")

# ---------------------------------------------------------------------------


class TestModelMixer(unittest.TestCase):

    def setUp(self):
        # a French speaker reading an English text...
        self._model_L2dir = os.path.join(MODELDIR, "models-eng")
        self._model_L1dir = os.path.join(MODELDIR, "models-fra")

    def testMix(self):
        acmodel1 = sppasAcModel()
        hmm1 = sppasHMM()
        hmm1.create_proto(25)
        hmm1.set_name("y")
        acmodel1.append_hmm(hmm1)
        acmodel1.get_repllist().add("y", "j")

        acmodel2 = sppasAcModel()
        hmm2 = sppasHMM()
        hmm2.create_proto(25)
        hmm2.set_name("j")
        hmm3 = sppasHMM()
        hmm3.create_proto(25)
        hmm3.name = "y"
        acmodel2.get_hmms().append(hmm2)
        acmodel2.get_hmms().append(hmm3)
        acmodel2.get_repllist().add("y", "y")
        acmodel2.get_repllist().add("j", "j")

        modelmixer = sppasModelMixer()
        modelmixer.set_models(acmodel1, acmodel2)

        outputdir = os.path.join(MODELDIR, "models-test")
        modelmixer.mix(outputdir, gamma=1.)
        self.assertTrue(os.path.exists(outputdir))
        model = sppasACMRW(outputdir).read()
        shutil.rmtree(outputdir)

    def testMixData(self):
        modelmixer = sppasModelMixer()
        modelmixer.read(self._model_L2dir, self._model_L1dir)
        outputdir = os.path.join(MODELDIR, "models-eng-fra")
        modelmixer.mix(outputdir, gamma=0.5)
        self.assertTrue(os.path.exists(outputdir))
        acmodel1 = sppasACMRW(self._model_L2dir).read()
        acmodel1_mono = acmodel1.extract_monophones()
        acmodel2 = sppasACMRW(os.path.join(MODELDIR, "models-eng-fra")).read()
        shutil.rmtree(outputdir)
