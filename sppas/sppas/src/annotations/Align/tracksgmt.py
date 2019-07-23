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

    src.annotations.Align.tracksgmt.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import codecs

from sppas.src.config import sg
from sppas.src.config import info
from sppas.src.utils.makeunicode import sppasUnicode

from .aligners import sppasAligners

# ---------------------------------------------------------------------------


class TrackSegmenter(object):
    """Automatic segmentation of a unit of speech.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Speech segmentation of a unit of speech (IPU/utterance/sentence/segment)
    at phones and tokens levels.

    This class is mainly an interface with external automatic aligners.

    It is expected that all the following data were previously properly
    fixed:
        - audio file: 1 channel, 16000 Hz, 16 bits;
        - tokenization: UTF-8 encoding file (optional);
        - phonetization: UTF-8 encoding file;
        - acoustic model: HTK-ASCII (Julius or HVite expect this format);

    and that:
        - both the AC and phonetization are based on the same phone set
        - both the tokenization and phonetization contain the same nb of words

    """

    aligners = sppasAligners()
    DEFAULT_ALIGNER = aligners.default_aligner_name()

    # -----------------------------------------------------------------------

    def __init__(self, model=None, aligner_name=DEFAULT_ALIGNER):
        """Create a TrackSegmenter instance.

        :param model: (str) Name of the directory of the acoustic model.
        :param aligner_name: (str) The identifier name of the aligner.

        It is expected that the AC model contains at least a file with name
        "hmmdefs", and a file with name "monophones" for HVite command.
        It can also contain:
            - tiedlist file;
            - monophones.repl file;
            - config file.
        Any other file will be ignored.

        """
        # The acoustic model directory
        self._model_dir = None

        # The automatic alignment system, and the "basic".
        # The basic aligner is used:
        #   - when the track segment contains only one phoneme;
        #   - when the track segment does not contain phonemes.
        self._aligner = None
        self.set_aligner(aligner_name)

        self._basic_aligner = TrackSegmenter.aligners.instantiate(None)

        if model is not None:
            self.set_model(model)

    # -----------------------------------------------------------------------

    def set_model(self, model):
        """Fix an acoustic model to perform time-alignment.

        :param model: (str) Name of the directory of the acoustic model.

        """
        self._model_dir = model

        # re-instantiate the same aligner with the appropriate model
        self._instantiate_aligner(self._aligner.name())

    # -----------------------------------------------------------------------

    def set_aligner(self, aligner_name):
        """Fix the name of the aligner, one of aligners.ALIGNERS_TYPES.

        :param aligner_name: (str) Case-insensitive name of an aligner system.

        """
        self._instantiate_aligner(aligner_name)

    # -----------------------------------------------------------------------

    def get_aligner_name(self):
        """Return the name of the instantiated aligner."""
        return self._aligner.name()

    # -----------------------------------------------------------------------

    def get_aligner_ext(self):
        """Return the output file extension the aligner will use."""
        return self._aligner.get_outext()

    # -----------------------------------------------------------------------

    def set_aligner_ext(self, ext):
        """Fix the output file extension the aligner will use."""
        self._aligner.set_outext(ext)

    # -----------------------------------------------------------------------

    def get_model(self):
        """Return the model directory name."""
        return self._model_dir

    # -----------------------------------------------------------------------

    def segment(self, audio_filename, phon_name, token_name, align_name):
        """Call an aligner to perform speech segmentation and manage errors.

        :param audio_filename: (str) the audio file name of an IPU
        :param phon_name: (str) file name with the phonetization
        :param token_name: (str) file name with the tokenization
        :param align_name: (str) file name to save the result WITHOUT ext.

        :returns: A message of the aligner in case of any problem, or
        an empty string if success.

        """
        # Get the phonetization and tokenization strings to time-align.
        phones = ""
        tokens = ""

        if phon_name is not None:
            phones = self._readline(phon_name)
        self._aligner.set_phones(phones)
        self._basic_aligner.set_phones(phones)

        if token_name is not None:
            tokens = self._readline(token_name)
        self._aligner.set_tokens(tokens)
        self._basic_aligner.set_tokens(tokens)

        # Do not align nothing!
        if len(phones) == 0:
            self._basic_aligner.run_alignment(0., align_name)
            return info(1222, "annotations")

        # If no audio available...
        if os.path.exists(audio_filename) is False:
            ret = self._basic_aligner.run_alignment(1., align_name)

        else:
            # Do not align only one phoneme!
            if len(phones.split()) <= 1 and "-" not in phones:
                self._basic_aligner.run_alignment(audio_filename, align_name)
                return ""

            # Execute Alignment
            ret = self._aligner.check_data()
            ret += self._aligner.run_alignment(audio_filename, align_name)

        return ret

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def _instantiate_aligner(self, name):
        """Instantiate self._aligner to the appropriate Aligner system."""
        self._aligner = TrackSegmenter.aligners.instantiate(
            self._model_dir, name)

    # -----------------------------------------------------------------------

    def _readline(self, filename):
        """Return the first line of a file as a unicode formatted string."""
        line = ""
        try:
            with codecs.open(filename, 'r', sg.__encoding__) as fp:
                sp = sppasUnicode(fp.readline())
                line = sp.to_strip()
                fp.close()
        except:
            return ""

        return line
