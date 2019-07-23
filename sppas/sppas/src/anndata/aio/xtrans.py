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

    src.anndata.aio.xtrans.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~

XTrans is a multi-platform, multilingual, multi-channel transcription tool
that supports manual transcription and annotation of audio recordings.
Last version of Xtrans was released in 2009.

https://www.ldc.upenn.edu/language-resources/tools/xtrans

"""
import codecs

from sppas.src.config import sg

from ..anndataexc import AioLineFormatError
from ..anndataexc import AnnDataTypeError
from ..ann.annlocation import sppasLocation
from ..ann.annlocation import sppasPoint
from ..ann.annlocation import sppasInterval

from .text import sppasBaseText
from .aioutils import load
from .aioutils import format_labels

# ----------------------------------------------------------------------------


class sppasTDF(sppasBaseText):
    """SPPAS TDF reader.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    This class implements a TDF reader, but not a writer.
    TDF is a Tab-Delimited Format. It contains 13 columns but SPPAS only
    extracts 8 of them.

    TDF does not support alternatives labels nor locations. Only the ones
    with the best score are saved.
    TDF can save several tiers.
    TDF does not support controlled vocabularies.
    TDF does not support hierarchy.
    TDF does not support metadata.
    TDF supports media assignment.
    TDF supports intervals only.
    TDF does not support alternative tags.
    TDF does not support radius.

    """

    @staticmethod
    def detect(filename):
        """Check whether a file is of TDF format or not.

        :param filename: (str) Name of the file to check.
        :returns: (bool)

        """
        # Open and load the content.
        try:
            with codecs.open(filename, 'r', sg.__encoding__) as fp:
                lines = fp.readlines()
                fp.close()
        except IOError:
            # can't open the file
            return False
        except UnicodeDecodeError:
            # can't open with SPPAS default encoding
            return False

        # Check each line
        for line in lines:
            if sppasTDF.is_comment(line):
                continue
            tab = line.split('\t')
            if len(tab) < 10:  # expected is 13
                return False

        return True

    # -----------------------------------------------------------------------

    @staticmethod
    def make_point(midpoint):
        """The localization is a time value, so always a float."""
        try:
            midpoint = float(midpoint)
        except ValueError:
            raise AnnDataTypeError(midpoint, "float")

        return sppasPoint(midpoint, radius=0.005)

    # -----------------------------------------------------------------------

    def __init__(self, name=None):
        """Initialize a new sppasTDF instance.

        :param name: (str) This transcription name.

        """
        if name is None:
            name = self.__class__.__name__
        super(sppasTDF, self).__init__(name)

        self.default_extension = "tdf"
        self.software = "Xtrans"

        # override all
        self._accept_multi_tiers = True
        self._accept_no_tiers = True
        self._accept_metadata = False
        self._accept_ctrl_vocab = False
        self._accept_media = False
        self._accept_hierarchy = False
        self._accept_point = True
        self._accept_interval = True
        self._accept_disjoint = False
        self._accept_alt_localization = False
        self._accept_alt_tag = False
        self._accept_radius = False
        self._accept_gaps = True
        self._accept_overlaps = True

    # -----------------------------------------------------------------------

    def read(self, filename):
        """Read a raw file and fill the sppasTranscription.

        It creates a tier for each speaker-channel observed in the file.

        :param filename: (str)

        """
        lines = load(filename)
        if len(lines) < 2:
            return

        # The first line is the name of the columns
        first_line = lines[0]
        lines.pop(0)
        self._extract_lines(first_line, lines)

    # -----------------------------------------------------------------------

    def _extract_lines(self, first_line, lines):
        """Extract the content of the TDF file.

        :param first_line: The first line of the TDF file (column' names)
        :param lines: the content of the file

        """
        # The 1st line indicates the names of the columns.
        column_names = first_line.split('\t')

        # Find indexes of the relevant information
        try:
            # index function raises a ValueError if the string is missing
            channel = column_names.index('channel;int')
            speaker = column_names.index('speaker;unicode')
            speaker_type = column_names.index('speakerType;unicode')
            speaker_dialect = column_names.index('speakerDialect;unicode')
            tag = column_names.index('transcript;unicode')
            begin = column_names.index('start;float')
            end = column_names.index('end;float')
            media_url = column_names.index('file;unicode')
        except ValueError:
            raise AioLineFormatError(1, first_line)

        # Extract rows, create tiers and metadata.
        for i, line in enumerate(lines):

            line = line.strip()

            # ignore blank lines
            if len(line) == 0:
                continue
            # a comment can contain metadata
            if sppasBaseText.is_comment(line):
                sppasBaseText._parse_comment(line, self)
                continue

            # a tab-delimited line
            line = line.split('\t')
            if len(line) < 10:
                raise AioLineFormatError(i + 1, line)

            # check for the tier (find it or create it)
            tier_name = line[speaker] + '-' + line[channel]
            tier = self.find(tier_name)
            if tier is None:

                # Create the media linked to the tier
                media = sppasBaseText.create_media(line[media_url].strip(),
                                                   self)

                # Create the tier and set metadata
                tier = self.create_tier(tier_name, media=media)
                tier.set_meta("media_channel", line[channel])
                tier.set_meta("speaker_name", line[speaker])
                tier.set_meta("speaker_type", line[speaker_type])
                tier.set_meta("speaker_dialect", line[speaker_dialect])

            # Add the new annotation
            location = sppasLocation(sppasInterval(
                sppasTDF.make_point(line[begin]),
                sppasTDF.make_point(line[end])))

            labels = format_labels(line[tag], separator="\n", empty="")

            tier.create_annotation(location, labels)
