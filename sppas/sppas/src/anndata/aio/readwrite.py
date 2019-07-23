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

    anndata.aio.readwrite.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os.path
from collections import OrderedDict

from sppas.src.utils.makeunicode import u
from sppas.src.utils.datatype import sppasTime

from ..anndataexc import AioEncodingError
from ..anndataexc import AioFileExtensionError
from ..anndataexc import AioError

from .text import sppasRawText
from .text import sppasCSV
from .sclite import sppasCTM
from .sclite import sppasSTM
from .xtrans import sppasTDF
from .praat import sppasTextGrid
from .praat import sppasPitchTier
from .praat import sppasIntensityTier
from .phonedit import sppasMRK
from .phonedit import sppasSignaix
from .htk import sppasLab
from .subtitle import sppasSubRip
from .subtitle import sppasSubViewer
from .weka import sppasARFF
from .weka import sppasXRFF
from .transcriber import sppasTRS
from .audacity import sppasAudacity
from .anvil import sppasAnvil
from .elan import sppasEAF
from .annotationpro import sppasANT
from .annotationpro import sppasANTX
from .xra import sppasXRA

# ---------------------------------------------------------------------------


class sppasRW(object):
    """Main parser of annotated data.
    
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    Readers and writers of annotated data.

    """
    
    TRANSCRIPTION_TYPES = OrderedDict()
    TRANSCRIPTION_TYPES[sppasXRA().default_extension.lower()] = sppasXRA
    TRANSCRIPTION_TYPES[sppasTextGrid().default_extension.lower()] = sppasTextGrid
    TRANSCRIPTION_TYPES[sppasARFF().default_extension.lower()] = sppasARFF
    TRANSCRIPTION_TYPES[sppasXRFF().default_extension.lower()] = sppasXRFF
    TRANSCRIPTION_TYPES[sppasAnvil().default_extension.lower()] = sppasAnvil
    TRANSCRIPTION_TYPES[sppasEAF().default_extension.lower()] = sppasEAF
    TRANSCRIPTION_TYPES[sppasANT().default_extension.lower()] = sppasANT
    TRANSCRIPTION_TYPES[sppasANTX().default_extension.lower()] = sppasANTX
    TRANSCRIPTION_TYPES[sppasTRS().default_extension.lower()] = sppasTRS
    TRANSCRIPTION_TYPES[sppasMRK().default_extension.lower()] = sppasMRK
    TRANSCRIPTION_TYPES[sppasSignaix().default_extension.lower()] = sppasSignaix
    TRANSCRIPTION_TYPES[sppasLab().default_extension.lower()] = sppasLab
    TRANSCRIPTION_TYPES[sppasSubRip().default_extension.lower()] = sppasSubRip
    TRANSCRIPTION_TYPES[sppasSubViewer().default_extension.lower()] = sppasSubViewer
    TRANSCRIPTION_TYPES[sppasCTM().default_extension.lower()] = sppasCTM
    TRANSCRIPTION_TYPES[sppasSTM().default_extension.lower()] = sppasSTM
    TRANSCRIPTION_TYPES[sppasIntensityTier().default_extension.lower()] = sppasIntensityTier
    TRANSCRIPTION_TYPES[sppasPitchTier().default_extension.lower()] = sppasPitchTier
    TRANSCRIPTION_TYPES[sppasAudacity().default_extension.lower()] = sppasAudacity
    TRANSCRIPTION_TYPES[sppasTDF().default_extension.lower()] = sppasTDF
    TRANSCRIPTION_TYPES[sppasCSV().default_extension.lower()] = sppasCSV
    TRANSCRIPTION_TYPES[sppasRawText().default_extension.lower()] = sppasRawText

    TRANSCRIPTION_SOFTWARE = dict()
    TRANSCRIPTION_SOFTWARE[sppasXRA().default_extension] = sppasXRA().software
    TRANSCRIPTION_SOFTWARE[sppasTextGrid().default_extension] = sppasTextGrid().software
    TRANSCRIPTION_SOFTWARE[sppasARFF().default_extension] = sppasARFF().software
    TRANSCRIPTION_SOFTWARE[sppasXRFF().default_extension] = sppasXRFF().software
    TRANSCRIPTION_SOFTWARE[sppasAnvil().default_extension] = sppasAnvil().software
    TRANSCRIPTION_SOFTWARE[sppasEAF().default_extension] = sppasEAF().software
    TRANSCRIPTION_SOFTWARE[sppasANT().default_extension] = sppasANT().software
    TRANSCRIPTION_SOFTWARE[sppasANTX().default_extension] = sppasANTX().software
    TRANSCRIPTION_SOFTWARE[sppasTRS().default_extension] = sppasTRS().software
    TRANSCRIPTION_SOFTWARE[sppasMRK().default_extension] = sppasMRK().software
    TRANSCRIPTION_SOFTWARE[sppasSignaix().default_extension] = sppasSignaix().software
    TRANSCRIPTION_SOFTWARE[sppasLab().default_extension] = sppasLab().software
    TRANSCRIPTION_SOFTWARE[sppasSubRip().default_extension] = sppasSubRip().software
    TRANSCRIPTION_SOFTWARE[sppasSubViewer().default_extension] = sppasSubViewer().software
    TRANSCRIPTION_SOFTWARE[sppasCTM().default_extension] = sppasCTM().software
    TRANSCRIPTION_SOFTWARE[sppasSTM().default_extension] = sppasSTM().software
    TRANSCRIPTION_SOFTWARE[sppasIntensityTier().default_extension] = sppasIntensityTier().software
    TRANSCRIPTION_SOFTWARE[sppasPitchTier().default_extension] = sppasPitchTier().software
    TRANSCRIPTION_SOFTWARE[sppasAudacity().default_extension] = sppasAudacity().software
    TRANSCRIPTION_SOFTWARE[sppasTDF().default_extension] = sppasTDF().software
    TRANSCRIPTION_SOFTWARE[sppasCSV().default_extension] = sppasCSV().software
    TRANSCRIPTION_SOFTWARE[sppasRawText().default_extension] = sppasRawText().software

    # -----------------------------------------------------------------------

    @staticmethod
    def extensions():
        """Return the list of supported extensions in lower case."""
        return sppasRW.TRANSCRIPTION_TYPES.keys()

    # -----------------------------------------------------------------------

    def __init__(self, filename):
        """Create a Transcription reader-writer.

        :param filename: (str)

        """
        self.__filename = u(filename)

    # -----------------------------------------------------------------------

    def get_filename(self):
        """Return the filename."""
        return self.__filename

    # -----------------------------------------------------------------------

    def set_filename(self, filename):
        """Set a new filename. 

        :param filename: (str)

        """
        self.__filename = u(filename)
        
    # -----------------------------------------------------------------------

    def read(self, heuristic=True):
        """Read a transcription from a file.

        :param heuristic: (bool) if the extension of the file is unknown, use
        an heuristic to detect the format, then to choose the reader-writer.
        :returns: sppasTranscription reader-writer

        """
        try:
            trs = sppasRW.create_trs_from_extension(self.__filename)
        except AioFileExtensionError:
            if heuristic is True:
                trs = sppasRW.create_trs_from_heuristic(self.__filename)
            else:
                raise

        if os.path.exists(self.__filename) is False:
            raise AioError(self.__filename)

        try:
            # Add metadata about the file
            fn = u(self.__filename)
            trs.set_meta('file_reader', trs.__class__.__name__)
            trs.set_meta('file_name', os.path.basename(fn))
            trs.set_meta('file_path', os.path.dirname(fn))
            trs.set_meta('file_ext', os.path.splitext(fn)[1])
            trs.set_meta('file_read_date', sppasTime().now)

            # Read the file content dans store into a Transcription()
            trs.read(self.__filename)

        except UnicodeError as e:
            raise AioEncodingError(filename=self.__filename, error_msg=str(e))
        except IOError:
            raise
        except Exception:
            raise

        return trs

    # -----------------------------------------------------------------------

    @staticmethod
    def create_trs_from_extension(filename):
        """Return a transcription according to a given filename.

        Only the extension of the filename is used.

        :param filename: (str)
        :returns: Transcription()

        """
        extension = os.path.splitext(filename)[1][1:]
        extension = extension.lower()
        if extension in sppasRW.extensions():
            return sppasRW.TRANSCRIPTION_TYPES[extension]()

        raise AioFileExtensionError(filename)

    # -----------------------------------------------------------------------

    @staticmethod
    def create_trs_from_heuristic(filename):
        """Return a transcription according to a given filename.

        The given file is opened and an heuristic allows to fix the format.

        :param filename: (str)
        :returns: Transcription()

        """
        for file_reader in sppasRW.TRANSCRIPTION_TYPES.values():
            try:
                if file_reader.detect(filename) is True:
                    return file_reader()
            except:
                continue
        return sppasRawText()

    # -----------------------------------------------------------------------

    def write(self, transcription):
        """Write a transcription into a file.

        :param transcription: (sppasTranscription)

        """
        trs_rw = sppasRW.create_trs_from_extension(self.__filename)
        trs_rw.set(transcription)

        # Add metadata about the file
        trs_rw.set_meta('file_writer', trs_rw.__class__.__name__)
        trs_rw.set_meta('file_name', os.path.basename(self.__filename))
        trs_rw.set_meta('file_path', os.path.dirname(self.__filename))
        trs_rw.set_meta('file_ext', os.path.splitext(self.__filename)[1])
        trs_rw.set_meta('file_write_date', "{:s}".format(sppasTime().now))
        file_version = int(trs_rw.get_meta("file_version", "0")) + 1
        trs_rw.set_meta('file_version', str(file_version))

        try:
            trs_rw.write(self.__filename)
        except UnicodeError as e:
            raise AioEncodingError(self.__filename, str(e))
        except Exception:
            raise
