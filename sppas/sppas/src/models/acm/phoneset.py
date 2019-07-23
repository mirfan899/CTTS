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

    src.models.acm.phoneset.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sppas.src.config import symbols
from sppas.src.config import separators
from sppas.src.resources.dictpron import sppasDictPron
from sppas.src.resources.vocab import sppasVocabulary

# ---------------------------------------------------------------------------


class sppasPhoneSet(sppasVocabulary):
    """Manager of the list of phonemes.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    This class allows to manage the list of phonemes:

        - get it from a pronunciation dictionary,
        - read it from a file,
        - write it into a file,
        - check if a phone string is valid to be used with HTK toolkit.

    """

    def __init__(self, filename=None):
        """Create a sppasPhoneSet instance.

        Add events to the list: laugh, dummy, noise, silence.

        :param filename (str) A file with 1 column containing
        the list of phonemes.

        """
        super(sppasPhoneSet, self).__init__(filename,
                                            nodump=True,
                                            case_sensitive=True)

        for key in symbols.phone:
            if symbols.phone[key] != "pause":
                self.add(key)

    # -----------------------------------------------------------------------

    def add_from_dict(self, dict_filename):
        """Add the list of phones from a pronunciation dictionary.

        :param dict_filename: (str) Name of an HTK-ASCII pronunciation dict

        """
        d = sppasDictPron(dict_filename)
        for key in d:
            value = d.get_pron(key)
            variants = value.split(separators.variants)
            for variant in variants:
                phones = variant.split(separators.phonemes)
                for phone in phones:
                    self.add(phone)

    # -----------------------------------------------------------------------

    @staticmethod
    def check_as_htk_phone(phone):
        """Check if a phone is correct to be used with HTK toolkit.

        A phone can't start by a digit nor '-' nor '+', and must be ASCII.

        :param phone: (str) Phone to be checked
        :returns: (bool)

        """
        try:
            phone = str(phone)
        except UnicodeEncodeError:
            return False

        # Must not contain spaces
        phone_copy = phone.strip()
        if len(phone_copy) != len(phone):
            return False

        # Must contain characters!
        if len(phone) == 0:
            return False

        # Must not start by minus or plus
        if phone[0] in ['-', '+']:
            return False

        # Must not start by a digit
        try:
            int(phone[0])
        except ValueError:
            return False

        return True
