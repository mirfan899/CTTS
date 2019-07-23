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

    src.annotations.splitter.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Module to split a string for the multilingual text normalization system.

"""
import re

from sppas.src.resources.dictrepl import sppasDictRepl
from sppas.src.utils.makeunicode import u, sppasUnicode

from .language import sppasLangISO

# ---------------------------------------------------------------------------


class sppasSimpleSplitter(object):
    """Utterance splitter

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    Split an utterance into tokens using whitespace or characters.

    Should be extended to properly split telephone numbers or dates, etc.
    (for written texts).

    """
    def __init__(self, lang, dict_replace=None, speech=True):
        """Creates a sppasSimpleSplitter.

        :param lang: the language code in iso639-3.
        :param dict_replace: Replacement dictionary
        :param speech: (bool) split transcribed speech vs written text

        """
        self.__lang = lang
        self.__speech = speech
        if dict_replace is not None:
            self.__repl = dict_replace
        else:
            self.__repl = sppasDictRepl(None)

    # -----------------------------------------------------------------------

    def split_characters(self, utt):
        """Split an utterance by characters.

        :param utt: (str) the utterance (a transcription, a sentence, ...) in utf-8
        :returns: A string (split character by character, using whitespace)

        """
        y = u(utt)
        tmp = " ".join(y)

        # split all characters except numbers and ascii characters
        sstr = re.sub(u("([０-９0-9a-zA-ZＡ-Ｔ\s]+\.?[０-９0-9a-zA-ZＡ-Ｔ\s]+)"),
                      lambda o: u(" %s " % o.group(0).replace(" ", "")), tmp)
        # and dates...
        if self.__speech is False:
            sstr = re.sub(u("([０-９0-9\s]+\.?[月年日\s]+)"),
                          lambda o: u(" %s " % o.group(0).replace(" ", "")), sstr)
        # and ・
        sstr = re.sub(u('[\s]*・[\s]*'), u("・"), sstr)

        return sstr

    # -----------------------------------------------------------------------

    def split(self, utt):
        """Split an utterance using whitespace.

        If the language is character-based, split each character.

        :param utt: (str) an utterance of a transcription, a sentence, ...
        :param std: (bool)

        :returns: A list (array of string)

        """
        s = utt
        if sppasLangISO.without_whitespace(self.__lang) is True:
            s = self.split_characters(s)

        toks = list()
        for t in s.split():

            # if not a phonetized entry
            if t.startswith("/") is False and t.endswith("/") is False:

                if sppasLangISO.without_whitespace(self.__lang) is False:
                    # Split numbers if stick to characters
                    # attention: do not replace [a-zA-Z] by [\w] (because \w includes numbers)
                    # and not on Asian languages: it can be a tone!
                    t = re.sub(u('([0-9])([a-zA-Z])'), u(r'\1 \2'), t)
                    t = re.sub(u('([a-zA-Z])([0-9])'), u(r'\1 \2'), t)

                # Split some punctuation
                t = re.sub(u('\\[\\]'), u(r'\\] \\['), t)

                # Split dots if stick to the beginning of a word
                # info: a dot at the end of a word is analyzed by the tokenizer
                t = re.sub(u(' \.([\w-])'), u(r' . \1'), t)
                t = re.sub(u('^\.([\w-])'), u(r' . \1'), t)

                # Split replacement characters
                for r in self.__repl:
                    if t.endswith(r):
                        t = t[:-len(r)]
                        t = t + ' ' + r

            toks.append(t.strip())

        # s = " ".join(toks)

        # Then split each time there is a space and return result
        # s = sppasUnicode(s).to_strip()

        return s.split()
