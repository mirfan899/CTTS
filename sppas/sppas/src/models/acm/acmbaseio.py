# -*- coding: UTF-8 -*-
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

    src.models.acm.acmbaseio.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base object for readers and writers of acoustic models.

"""
from .acmodel import sppasAcModel
from ..modelsexc import ModelsDataTypeError

# ----------------------------------------------------------------------------


class sppasBaseIO(sppasAcModel):
    """Base object for readers and writers of acm.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:

    """

    @staticmethod
    def detect(filename):
        return False

    # -----------------------------------------------------------------------

    def __init__(self, name=None):
        """Initialize a new Acoustic Model reader-writer instance.

        :param name: (str) Name of the acoustic model.

        """
        super(sppasBaseIO, self).__init__(name)
        self._is_ascii = True
        self._is_binary = False

    # -----------------------------------------------------------------------
    # Getters
    # -----------------------------------------------------------------------

    def is_ascii(self):
        """Return True if it supports to read/write ASCII files.

        :returns: (bool)

        """
        return self._is_ascii

    # -----------------------------------------------------------------------

    def is_binary(self):
        """Return True if it supports to read and write binary files.

        :returns: (bool)

        """
        return self._is_binary

    # -----------------------------------------------------------------------
    # Setters
    # -----------------------------------------------------------------------

    def set(self, other):
        """Set self with other content.

        :param other: (sppasAcModel)

        """
        try:
            self._name = other.get_name()
            self._macros = other.get_macros()
            self._hmms = other.get_hmms()
            self._tiedlist = other.get_tiedlist()
            self._repllist = other.get_repllist()
        except AttributeError:
            raise ModelsDataTypeError("acoustic model",
                                      "sppasAcModel",
                                      type(other))

    # -----------------------------------------------------------------------

    def read(self, folder):
        """Read a folder content and fill the Acoustic Model.

        :param folder: (str)

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def write(self, folder):
        """Write the Acoustic Model into a folder.

        :param folder: (str)

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------

    @staticmethod
    def write_hmm_proto(proto_size, proto_filename):
        """Write a `proto` file. The proto is based on a 5-states HMM.

        :param proto_size: (int) Number of mean and variance values.
        It's commonly either 25 or 39, it depends on the MFCC parameters.
        :param proto_filename: (str) Full name of the prototype to write.

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def read_phonesrepl(self, filename):
        """Read a replacement table of phone names from a file.

        :param filename: (str)

        """
        try:
            self._repllist.load_from_ascii(filename)
            # Some HACK...
            # because '+' and '-' are the biphones/triphones delimiters,
            # they can't be used as phone name.
            self._repllist.remove('+')
            self._repllist.remove('-')
        except Exception:
            pass

    # -----------------------------------------------------------------------

    def read_tiedlist(self, filename):
        """Read a tiedlist from a file.

        :param filename: (str)

        """
        try:
            self._tiedlist.read(filename)
        except:
            pass
