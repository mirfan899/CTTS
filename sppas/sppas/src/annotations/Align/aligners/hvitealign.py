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

    src.annotations.Align.aligners.hvitealign.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://htk.eng.cam.ac.uk/links/asr_tool.shtml

"""
import os
import codecs
from subprocess import Popen, PIPE, STDOUT

from sppas.src.config import sg
from sppas.src.resources.dictpron import sppasDictPron

from .basealigner import BaseAligner

# ----------------------------------------------------------------------------


class HviteAligner(BaseAligner):
    """HVite automatic alignment system.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self, model_dir=None):
        """Create a HViteAligner instance.

        This class allows to align one inter-pausal unit with with the
        external segmentation tool HVite.

        HVite is able to align one audio segment that can be:
            - an inter-pausal unit,
            - an utterance,
            - a sentence,
            - a paragraph...
        no longer than a few seconds.

        :param model_dir: (str) Name of the directory of the acoustic model

        """
        super(HviteAligner, self).__init__(model_dir)

        self._extensions = ["mlf"]
        self._outext = self._extensions[0]
        self._name = "hvite"

    # -----------------------------------------------------------------------

    def gen_dependencies(self, grammar_name, dict_name):
        """Generate the dependencies (grammar, dictionary) for HVite.

        :param grammar_name: (str) the file name of the tokens
        :param dict_name: (str) the dictionary file name

        """
        dictpron = sppasDictPron()

        with codecs.open(grammar_name, 'w', sg.__encoding__) as flab:

            for token, pron in zip(self._tokens.split(), self._phones.split()):

                # dictionary:
                for variant in pron.split("|"):
                    dictpron.add_pron(token, variant.replace("-", " "))
                    # if self._infersp is True:
                    #     variant = variant + '-sil'
                    #     dictpron.add_pron(token, variant.replace("-", " "))

                # lab file (one token per line)
                flab.write(token+"\n")

        dictpron.save_as_ascii(dict_name)

    # -----------------------------------------------------------------------

    def run_hvite(self, inputwav, outputalign):
        """Perform the speech segmentation.

        Call the system command `HVite`.

        Given audio file must match the ones we used to train the acoustic
        model: PCM-WAV 16000 Hz, 16 bits

        :param inputwav: (str) audio input file name
        :param outputalign: (str) the output file name

        """
        if self._model is None:
            raise IOError('HVite aligner requires an acoustic model')

        base_name = os.path.splitext(inputwav)[0]
        dict_name = base_name + ".dict"
        grammar_name = base_name + ".lab"
        self.gen_dependencies(grammar_name, dict_name)

        # Example of use with triphones:
        #
        # HVite
        #   -A                             # print command line arguments
        #   -D                             # display configuration variables
        #   -T 1                           # set trace flags to N
        #   -l '*'                         # dir to store label/lattice files
        #   -a                             # align from label file
        #   -b SENT-END                    # *** TO NOT USE for FA ***
        #   -m                             # output model alignment
        #   -C models-EN/config            # model config !IMPORTANT!
        #   -H models-EN/macros
        #   -H models-EN/hmmdefs
        #   -t 250.0 150.0 1000.0
        #   -i aligned.out
        #   -y lab
        #   dict/EN.dict
        #   models-EN/tiedlist
        #   file.wav
        #
        # Replace the tiedlist by the list of phonemes for a monophone model

        hmmdefs = os.path.join(self._model, "hmmdefs")
        macros = os.path.join(self._model, "macros")
        config = os.path.join(self._model, "config")
        graph = os.path.join(self._model, "tiedlist")
        if os.path.isfile(graph) is False:
            graph = os.path.join(self._model, "monophones")

        # Program name
        command = "HVite "
        command += " -T 1 "
        command += " -l '*' "
        command += " -a "
        command += " -m "
        command += ' -C "' + config.replace('"', '\\"') + '" '
        command += ' -H "' + hmmdefs.replace('"', '\\"') + '" '
        if os.path.isfile(macros):
            command += ' -H "' + macros.replace('"', '\\"') + '" '
        command += " -t 250.0 150.0 1000.0 "
        command += ' -i "' + outputalign.replace('"', '\\"') + '" '
        command += ' -y lab'
        command += ' "' + dict_name.replace('"', '\\"') + '" '
        command += ' "' + graph.replace('"', '\\"') + '" '
        command += inputwav

        # Execute command
        p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        p.wait()
        line = p.communicate()

        if len(line[0]) > 0 and line[0].find("not found") > -1:
            raise OSError("HVite is not properly installed. "
                          "See installation instructions for details.")

        if len(line[0]) > 0 and line[0].find("ERROR [") > -1:
            raise OSError("HVite command failed: {:s}".format(line[0]))

        # Check output file
        if os.path.isfile(outputalign) is False:
            raise Exception('HVite did not created an alignment file.')

        return line[0]

    # -----------------------------------------------------------------------

    def run_alignment(self, input_wav, output_align):
        """Execute the external program `HVite` to align.

        Given audio file must match the ones we used to train the acoustic
        model: PCM-WAV 16000 Hz, 16 bits

        :param input_wav: (str) audio input file name
        :param output_align: (str) the output file name

        :returns: (str) An empty string.

        """
        output_align = output_align + "." + self._outext

        message = self.run_hvite(input_wav, output_align)

        if os.path.isfile(output_align):
            with codecs.open(output_align, 'r', sg.__encoding__) as f:
                lines = f.readlines()
                f.close()

            if len(lines) == 1:
                raise IOError(message + "\n" + lines[0])

        return ""
