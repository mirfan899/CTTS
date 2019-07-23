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

    models.slm.arpaio.py
    ~~~~~~~~~~~~~~~~~~~~~

"""
import codecs

from sppas.src.config import sg

from ..modelsexc import ModelsDataTypeError
from ..modelsexc import ArpaFileError

# ---------------------------------------------------------------------------


class sppasArpaIO(object):
    """ARPA statistical language models reader/writer.

    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      develop@sppas.org

    This class is able to load and save statistical language models from
    ARPA-ASCII files.

    """

    def __init__(self):
        """Create a sppasArpaIO instance without model."""
        self.__slm = None

    # -----------------------------------------------------------------------

    def set(self, slm):
        """Set the model of the sppasSLM.

        :param slm: (list) List of tuples for 1-gram, 2-grams, ...

        """
        if not (isinstance(slm, list) and
                all([isinstance(m, list) for m in slm])):
            raise ModelsDataTypeError("slm",
                                      "list of lists of tuples",
                                      type(slm))

        self.__slm = slm

    # -----------------------------------------------------------------------

    def load(self, filename):
        """Load a model from an ARPA file.

        :param filename: (str) Name of the file of the model.

        """
        # we expect small models, so we can read the whole file in one!
        with codecs.open(filename, 'r', sg.__encoding__) as f:
            lines = f.readlines()

        self.__slm = list()
        n = 0
        lm = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                pass
            elif line.startswith('\\end'):
                break
            elif line.startswith('\\') and "data" not in line:
                if n > 0:
                    self.__slm.append(lm)
                n += 1
                lm = []
            elif n > 0:
                # split line into columns
                cols = line.split()
                if len(cols) < n+1:
                    raise ArpaFileError(line)
                # probability is the first column
                proba = float(cols[0])
                # the n- following columns are the ngram
                tokenseq = " ".join(cols[1:n+1])
                # the last (optional) value is the bow
                bow = None
                if len(cols) > n+1:
                    bow = float(cols[-1])
                lm.append((tokenseq, proba, bow))

        if n > 0:
            self.__slm.append(lm)

        return self.__slm

    # -----------------------------------------------------------------------

    def save(self, filename):
        r"""Save the model into a file, in ARPA-ASCII format.

        The ARPA format:

        \data\
         ngram 1=nb1
         ngram 2=nb2
         . . .
         ngram N=nbN

         \1-grams:
         p(a_z)  a_z  bow(a_z)
         . . .

         \2-grams:
         p(a_z)  a_z  bow(a_z)
         . . .

         \n-grams:
         p(a_z)  a_z
         . . .

         \end\

        :param filename: (str) File where to save the model.

        """
        if self.__slm is not None:
            with codecs.open(filename, 'w', sg.__encoding__) as f:
                f.write(self._serialize_slm())

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def _serialize_slm(self):
        """Serialize a model into a string, in ARPA-ASCII format.

        :returns: The ARPA-ASCII model as a string.

        """
        result = self._serialize_header()
        for n, m in enumerate(self.__slm):
            new_ngram = sppasArpaIO._serialize_ngram(m, n+1)
            result = result + new_ngram
        result += sppasArpaIO._serialize_footer()

        return result

    # -----------------------------------------------------------------------

    def _serialize_header(self):
        r"""Serialize the header of an ARPA file.

        \data\
        ngram 1=nb1
        ngram 2=nb2
        ...
        ngram N=nbN

        """
        r = "\\data\\ \n"
        for i, m in enumerate(self.__slm):
            r += "ngram " + str(i+1) + "=" + str(len(m)) + "\n"
        r += "\n"

        return r

    # -----------------------------------------------------------------------

    @staticmethod
    def _serialize_ngram(model, order):
        r"""Serialize one of the ngrams of an ARPA file.

        \2-grams:
        p(a_z)  a_z  bow(a_z)
        ...

        """
        r = "\\"+str(order)+"-grams: \n"

        for (wseq, lp, bo) in model:
            r += str(round(lp, 6)) + "\t" + wseq
            if bo is not None:
                r += "\t"+str(round(bo, 6))
            r += "\n"
        r += "\n"

        return r

    # -----------------------------------------------------------------------

    @staticmethod
    def _serialize_footer():
        r"""Serialize the footer of an ARPA file.

        \end

        """
        return "\\end\n"
