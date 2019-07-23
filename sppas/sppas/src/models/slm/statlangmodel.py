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

    models.slm.statlangmodel.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from ..modelsexc import ModelsDataTypeError
from .arpaio import sppasArpaIO

# ---------------------------------------------------------------------------


class sppasSLM(object):
    """Statistical language model representation.

    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      develop@sppas.org

    """

    def __init__(self):
        """Create a sppasSLM instance without model."""
        self.model = None

    # -----------------------------------------------------------------------

    def set(self, model):
        """Set the language model.

        :param model: (list) List of lists of tuples for 1-gram, 2-grams, ...

        """
        if not (isinstance(model, list) and
                all([isinstance(m, list) for m in model])):
            raise ModelsDataTypeError("slm",
                                      "list of lists of tuples",
                                      type(model))

        self.model = model

    # -----------------------------------------------------------------------

    def load_from_arpa(self, filename):
        """Load the model from an ARPA-ASCII file.

        :param filename: (str) Filename from which to read the model.

        """
        arpa_io = sppasArpaIO()
        self.model = arpa_io.load(filename)

    # -----------------------------------------------------------------------

    def save_as_arpa(self, filename):
        """Save the model into an ARPA-ASCII file.

        :param filename: (str) Filename in which to write the model.

        """
        arpa_io = sppasArpaIO()
        arpa_io.set(self.model)
        arpa_io.save(filename)

    # -----------------------------------------------------------------------

    def evaluate(self, filename):
        """Evaluate a model on a file (perplexity)."""
        raise NotImplementedError("The method 'evaluate' of sppasSLM is "
                                  "not implemented yet. Any help is welcome!")

    # -----------------------------------------------------------------------

    def interpolate(self, other):
        """Interpolate the model with another one.

        An N-Gram language model can be constructed from a linear interpolation
        of several models. In this case, the overall likelihood P(w|h) of a
        word w occurring after the history h is computed as the arithmetic
        average of P(w|h) for each of the models.

        The default interpolation method is linear interpolation. In addition,
        log-linear interpolation of models is possible.

        :param other: (sppasSLM)
        """
        raise NotImplementedError("The method 'interpolate' of sppasSLM is "
                                  "not implemented yet. Any help is welcome!")
