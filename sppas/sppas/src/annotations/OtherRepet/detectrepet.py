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

    src.annotations.OtherRepet.detectrepet.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from ..SelfRepet.datastructs import DataRepetition
from .rules import OtherRules

# ---------------------------------------------------------------------------


class OtherRepetition(DataRepetition):
    """Other-Repetition automatic detection.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi

    Search for the sources, then find where are the echos.

    """
    def __init__(self, stop_list=None):
        """Create a new Repetitions instance.

        :param stop_list: (sppasVocabulary) List of un-relevant tokens.

        """
        super(OtherRepetition, self).__init__()
        self.__rules = OtherRules(stop_list)

    # -----------------------------------------------------------------------
    # Detect sources
    # -----------------------------------------------------------------------

    def detect(self, speaker1, speaker2, limit=10):
        """Search for the first other-repetition in tokens.

        :param speaker1: (DataSpeaker) Entries of speaker 1
        :param speaker2: (DataSpeaker) Entries of speaker 2
        :param limit: (int) Go no longer than 'limit' entries of speaker 1

        """
        self.reset()

        current_spk1 = 0
        next_spk1 = self.get_longest(current_spk1, speaker1, speaker2)

        while current_spk1 < len(speaker1) and current_spk1 < limit and \
                self.get_source() is None:

            if next_spk1 == -1:
                current_spk1 += 1
            else:
                current_spk1 = self.select(current_spk1, next_spk1,
                                           speaker1, speaker2)

            next_spk1 = OtherRepetition.get_longest(current_spk1,
                                                    speaker1, speaker2)

    # -----------------------------------------------------------------------

    @staticmethod
    def get_longest(current1, speaker1, speaker2):
        """Return the index of the last token of the longest repeated string.

        :param current1: (int) Current index in entries of speaker 1
        :param speaker1: (DataSpeaker) Entries of speaker 1
        :param speaker2: (DataSpeaker2) Entries of speaker 2 (or None)
        :returns: (int) Index or -1

        """
        last_token = -1
        # Get the longest string
        for t in range(current1, len(speaker1)):

            param2 = 0
            spk = speaker2

            # search
            repet_idx = speaker1.is_word_repeated(t, param2, spk)
            if repet_idx > -1:
                last_token = t
            else:
                break

        return last_token

    # -----------------------------------------------------------------------

    def select(self, start, end, speaker1, speaker2):
        """Append (or not) an other-repetition.

        :param start: (int) start index of the entry of the source (speaker1)
        :param end: (int) end index of the entry of the source (speaker1)
        :param speaker1: (DataSpeaker) Entries of speaker 1
        :param speaker2: (DataSpeaker) Entries of speaker 2

        """
        # Rule 1: keep any repetition containing at least 1 relevant token
        keep_me = self.__rules.rule_syntagme(start, end, speaker1)
        if keep_me is False:
            # Rule 2: keep any repetition if N>2 AND strict echo
            keep_me = self.__rules.rule_strict(start, end, speaker1, speaker2)

        if keep_me is True:
            self.set_source(start, end)
            self.find_echos(start, end, speaker1, speaker2)
            return end + 1

        return start + 1

    # -----------------------------------------------------------------------
    # Search for echos (for a given source)
    # -----------------------------------------------------------------------

    def find_echos(self, start, end, speaker1, speaker2):
        """Find all echos of a source.
        
        :param start: (int) start index of the entry of the source (speaker1)
        :param end: (int) end index of the entry of the source (speaker1)
        :param speaker1: (DataSpeaker) Entries of speaker 1
        :param speaker2: (DataSpeaker) Entries of speaker 2
        :returns: DataRepetition()
        
        """
        # Find all repeated tokens of each token of the source
        repeats = list()

        ridx = 0
        i = start
        while i <= end:
            repeats.append(list())
            idx2 = speaker1.is_word_repeated(i, 0, speaker2)

            while idx2 != -1:
                repeats[ridx].append(idx2)
                idx2 = speaker1.is_word_repeated(i, idx2+1, speaker2)
            i += 1
            ridx += 1

        # Filter the repetitions (try to get the longest sequence)
        if len(repeats) == 1:
            self.add_echo(repeats[0][0], repeats[0][0])
        else:
            i = 0
            while i < len(repeats):
                repeated = OtherRepetition.__get_longest_repeated(i, repeats)
                self.add_echo(repeated[0], repeated[-1])
                i += len(repeated)

    # -----------------------------------------------------------------------

    @staticmethod
    def __get_longest_repeated(start, repeats):
        """Select the longest echo from start position in repeats."""

        path_repeats = []
        for i in range(len(repeats[start])):
            path_repeats.append([])
            path_repeats[i].append(repeats[start][i])

            for j in range(start+1, len(repeats)):
                prec_value = path_repeats[-1][-1]
                v = 0
                if prec_value not in repeats[j]:
                    if (prec_value+1) not in repeats[j]:
                        if (prec_value+2) not in repeats[j]:
                            if (prec_value-1) not in repeats[j]:
                                break
                            else:
                                v = repeats[j].index(prec_value-1)
                        else:
                            v = repeats[j].index(prec_value+2)
                    else:
                        v = repeats[j].index(prec_value+1)
                else:
                    v = repeats[j].index(prec_value)
                path_repeats[i].append(repeats[j][v])

        # return the (first of the) longest path:
        return sorted(max(path_repeats, key=lambda x: len(x)))
