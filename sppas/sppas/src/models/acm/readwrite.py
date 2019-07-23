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

    src.models.acm.readwrite.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Readers and writers of acoustic models.

"""
from collections import OrderedDict

from sppas.src.utils.makeunicode import u

from ..modelsexc import MioEncodingError
from ..modelsexc import MioFolderError
from ..modelsexc import MioFileFormatError

from .acmodelhtkio import sppasHtkIO

# ----------------------------------------------------------------------------


class sppasACMRW(object):
    """Generic reader and writer for acoustic models.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Currently, only HTK-ASCII is supported.

    We expect to add readers and writers for several file formats
    in a -- far -- future.

    """

    ACM_TYPES = OrderedDict()
    ACM_TYPES["hmmdefs"] = sppasHtkIO

    # -----------------------------------------------------------------------

    def __init__(self, folder):
        """Create an acoustic model reader-writer.

        :param folder: (str) Name of the folder with the acoustic model files

        """
        self.__folder = u(folder)

    # -----------------------------------------------------------------------

    @staticmethod
    def get_formats():
        """Return the list of accepted formats for acoustic models."""
        return sppasACMRW.ACM_TYPES.keys()

    # -----------------------------------------------------------------------

    def get_folder(self):
        """Return the name of the folder of the acoustic model."""
        return self.__folder

    # -----------------------------------------------------------------------

    def set_folder(self, folder):
        """Set a new folder to store files of the acoustic model.

        :param folder: (str) New name of the folder of the acoustic model.

        """
        self.__folder = u(folder)

    # -----------------------------------------------------------------------

    def read(self):
        """Read an acoustic model from the folder.

        :returns: sppasAcModel()

        """
        try:
            acm = self.get_reader()
            acm.read(self.__folder)
        except UnicodeError as e:
            raise MioEncodingError(self.__folder, str(e))
        except Exception:
            raise

        return acm

    # -----------------------------------------------------------------------

    def get_reader(self):
        """Return an acoustic model according to the given folder.

        :returns: sppasAcModel()

        """
        for file_reader in sppasACMRW.ACM_TYPES.values():
            try:
                if file_reader.detect(self.__folder) is True:
                    return file_reader()
            except:
                continue

        raise MioFolderError(self.__folder)

    # -----------------------------------------------------------------------

    def write(self, acmodel, format="hmmdefs"):
        """Write an acoustic model into a folder.

        :param acmodel: (str)
        :param format: The format to save the acoustic model

        """
        if format not in sppasACMRW.ACM_TYPES:
            raise MioFileFormatError(format)

        acm_rw = sppasACMRW.ACM_TYPES[format]()
        acm_rw.set(acmodel)
        try:
            acm_rw.write(self.__folder)
        except UnicodeError as e:
            raise MioEncodingError(self.__folder, str(e))
        except Exception:
            raise
