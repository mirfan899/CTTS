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

    annotations.Align.aligners.basealigner.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import shutil
import random
from datetime import date

from sppas.src.models.acm.tiedlist import sppasTiedList
from sppas.src.utils.makeunicode import sppasUnicode

# ---------------------------------------------------------------------------


class BaseAligner(object):
    """Base class for any automatic alignment system.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Base class for a system to perform phonetic speech segmentation.

    """

    def __init__(self, model_dir=None):
        """Create a BaseAligner instance.

        :param model_dir: (str) the acoustic model directory name

        """
        if model_dir is not None:
            if os.path.exists(model_dir) is False:
                raise IOError("{:s} is not a valid acoustic model directory."
                              "".format(model_dir))

        # members
        self._model = model_dir
        self._name = ""
        self._extensions = list()

        # alignment options
        self._outext = ""       # output file name extension
        self._phones = ""       # string of the phonemes to time-align
        self._tokens = ""       # string of the tokens to time-align

    # ------------------------------------------------------------------------
    # members
    # ------------------------------------------------------------------------

    def extensions(self):
        """Return the list of supported file name extensions."""
        return self._extensions

    # -----------------------------------------------------------------------

    def name(self):
        """Return the identifier name of the aligner."""
        return self._name

    # -----------------------------------------------------------------------

    def outext(self):
        """Return the extension of output files."""
        return self._outext

    # -----------------------------------------------------------------------
    # alignment options
    # -----------------------------------------------------------------------

    def add_tiedlist(self, entries):
        """Add missing triphones/biphones in the tiedlist of the model.

        Backup the initial file if entries were added.

        :param entries: (list) List of missing entries into the tiedlist.
        :returns: list of entries really added

        """
        tied_file = os.path.join(self._model, "tiedlist")
        if os.path.exists(tied_file) is False:
            return []

        tie = sppasTiedList()
        tie.read(tied_file)
        add_entries = tie.add_to_tie(entries)
        if len(add_entries) > 0:
            today = str(date.today())
            rand_val = str(int(random.random()*10000))
            backup_tied_file = os.path.join(
                self._model,
                "tiedlist." + today + "." + rand_val)
            shutil.copy(tied_file, backup_tied_file)
            tie.save(tied_file)

        return add_entries

    # ------------------------------------------------------------------------

    def set_phones(self, phones):
        """Fix the pronunciations of each token.

        :param phones: (str) Phonetization

        """
        phones = sppasUnicode(phones).unicode()
        self._phones = phones

    # ------------------------------------------------------------------------

    def set_tokens(self, tokens):
        """Fix the tokens.

        :param tokens: (str) Tokenization

        """
        tokens = sppasUnicode(tokens).unicode()
        self._tokens = tokens

    # -----------------------------------------------------------------------

    def check_data(self):
        """Check the given data to be aligned (phones and tokens).

        :returns: A warning message, or an empty string if check is OK.

        """
        if len(self._phones) == 0:
            raise IOError("No data to time-align.")

        phones = sppasUnicode(self._phones).to_strip().split()
        tokens = sppasUnicode(self._tokens).to_strip().split()
        if len(tokens) != len(phones):
            message = "Tokens alignment disabled: " \
                      "not the same number of tokens in tokenization ({:d}) " \
                      "and phonetization ({:d}).".format(len(self._tokens),
                                                         len(self._phones))
            # assign a "w_" to each phone
            self._tokens = " ".join(["w_" + str(i)
                                     for i in range(len(phones))])
            return message

        return ""

    # -----------------------------------------------------------------------

    def run_alignment(self, input_wav, output_align):
        """Perform forced-alignment.

        It is expected that the alignment is performed on a file with a size
        less or equal to a sentence (sentence/IPUs/segment/utterance).

        The audio file must be of type PCM-WAV 16000 Hz, 16 bits, like in the
        model.

        :param input_wav: (str) the audio input file name
        :param output_align: (str) the output file name
        :returns: (str) A message of the aligner

        """
        raise NotImplementedError
