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

    src.annotations.phonunk.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unknown words phonetization.

"""
import re

from sppas.src.utils.makeunicode import sppasUnicode
from .dagphon import sppasDAGPhonetizer

# ---------------------------------------------------------------------------

LIMIT_SIZE = 40  # Max nb of characters of an unknown entry

# ---------------------------------------------------------------------------


class sppasPhonUnk(object):
    """Perform a dictionary-based phonetization for unknown entries.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Implements a language-independent algorithm to phonetize unknown tokens.
    The algorithm is based on the idea that given enough examples it
    should be possible to predict the pronunciation of unseen tokens purely
    by analogy. It consists in exploring the unknown token from left to
    right, then from right to left, and to find the longest strings in the
    dictionary. Since this algorithm uses the dictionary, the quality of
    such a phonetization strongly depends on this resource.

    Example of use:

        >>> d = { 'a':'a|aa', 'b':'b', 'c':'c|cc', 'abb':'abb', 'bac':'bac' }
        >>> p = sppasPhonUnk(d)

    """
    def __init__(self, pron_dict):
        """Create a sppasPhonUnk instance.

        :param pron_dict: (sppasPronDict) Dictionary of a set of tuples:
        token=key, phon=value.

        """
        self.prondict = pron_dict
        self.dagphon = sppasDAGPhonetizer(variants=4)

    # ------------------------------------------------------------------
    # Getters and Setters
    # ------------------------------------------------------------------

    def set_variants(self, v):
        """Fix the maximum number of variants.

        :param v: (int) If v is set to 0, all variants will be returned.

        """
        self.dagphon.set_variants(v)

    # -----------------------------------------------------------------------

    def get_phon(self, entry):
        """Return the phonetization of an unknown entry.

        :param entry: (str) the string to phonetize
        :returns: a string with the proposed phonetization
        :raises: Exception if the word can NOT be phonetized

        """
        _str = sppasUnicode(entry).to_strip()
        _str = sppasUnicode(_str).to_lower()
        if len(_str) > 0 and _str[-1].isalnum() is False:
            _str = _str[:-1]
        if len(_str) > 0 and _str[0].isalnum() is False:
            _str = _str[1:]
        if len(_str) == 0:
            return ""

        if len(entry) > LIMIT_SIZE:
            raise Exception

        # Find all pronunciations of segments with a longest matching algo.
        _tabstr = re.split("[-'_\s]", _str)
        pronlr = ""
        pronrl = ""

        for s in _tabstr:
            plr = self.__recurslr(s)
            plr = plr.strip()
            if len(plr) > 0:
                pronlr = pronlr + " " + plr

            prl = self.__recursrl(s)
            prl = prl.strip()
            if len(prl) > 0:
                pronrl = pronrl + " " + prl

        pronlr = pronlr.strip()
        pronrl = pronrl.strip()

        # Create the output
        pron = ""
        if len(pronlr) > 0:
            if len(pronrl) > 0:
                pron = self.dagphon.decompose(pronlr, pronrl)
            else:
                pron = self.dagphon.decompose(pronlr)
        else:
            if len(pronrl) > 0:
                pron = self.dagphon.decompose(pronrl)

        if len(pron) > 0:
            return pron

        raise Exception

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __longestlr(self, entry):
        """Select the longest phonetization of an entry, from the end.

        :param entry: (str)

        """
        i = len(entry)
        while i > 0:
            # Find in the dictionary a substring from 0 to i
            if entry[:i] in self.prondict:
                # Return index for the longest string
                return i
            i -= 1

        # Did not find any pronunciation for this entry!
        return 0

    # -----------------------------------------------------------------------

    def __recurslr(self, entry):
        """Recursive method to find a phonetization of a supposed unk entry.

        Return a string with the proposed phonetization.
        Whitespace separate segments.

        """
        if len(entry) == 0:
            return ""

        # LEFT:
        # ###########
        # Find the index of the longest left string that can be phonetized
        left = ""
        left_index = self.__longestlr(entry)
        # Nothing can be phonetized at the left part!
        if left_index == 0:
            _phonleft = ""
            left_index = 1
            left = ""
        else:
            # left is from the first to the leftindex character in str
            left = entry[:left_index]
            # Phonetize
            _phonleft = self.prondict.get(left, "")
            # The entire entry can be phonetized (nothing to do at right)
            if left_index == len(entry):
                return _phonleft

        # RIGHT:
        # ###########
        right = entry[left_index:len(entry)]
        if len(right) == 0:
            return _phonleft
        if right in self.prondict:
            _phonright = self.prondict.get(right)
        else:
            # If right part of the entry is unknown...
            # Use recursivity to phonetize
            _phonright = self.__recurslr(right)

        if len(_phonleft) > 0 and len(_phonright) > 0:
            return _phonleft + " " + _phonright

        return _phonright

    # -----------------------------------------------------------------------

    def __longestrl(self, entry):
        """Select the longest phonetization of an entry, from the start."""
        i = 0
        while i < len(entry):
            # Find in the dictionary a substring from i to the entry-length
            if entry[i:] in self.prondict:
                # Return index for the longest string
                return i
            i += 1

        # Did not find any pronunciation for this entry!
        return len(entry)

    # -----------------------------------------------------------------------

    def __recursrl(self, enrty):
        """Recursive method to find a phonetization of a supposed unk entry.

        Return a string with the proposed phonetization.
        Whitespace separate segments.

        """
        if len(enrty) == 0:
            return ""

        # RIGHT:
        # ###########
        # Find the index of the longest right string that can be phonetized
        right = ""
        right_index = self.__longestrl(enrty)
        # Nothing can be phonetized at the right part!
        if right_index == len(enrty):
            _phonright = ""
            right_index = len(enrty)-1
            right = ""
        else:
            # right is from the end to the rightindex character in str
            right = enrty[right_index:]
            _phonright = self.prondict.get(right, "")
            # The entire entry can be phonetized (nothing to do at left)
            if right_index == 0:
                return _phonright

        # LEFT:
        # ###########
        left = enrty[0:right_index]
        if len(left) == 0:
            return _phonright
        if left in self.prondict:
            _phonleft = self.prondict.get(left)
        else:
            # If left part of the entry is unknown...
            # Use recursivity to phonetize
            _phonleft = self.__recursrl(left)

        if len(_phonleft) > 0 and len(_phonright) > 0:
            return _phonleft + " " + _phonright

        return _phonleft
