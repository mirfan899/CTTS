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

    annotations.Align.aligners.alignerio.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import codecs
import logging

from sppas.src.config import sg
from sppas.src.config import separators
from sppas.src.utils.makeunicode import sppasUnicode

# ---------------------------------------------------------------------------


class BaseAlignersReader(object):
    """Base class for readers/writers of time-aligned files.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self):
        self.extension = ""

    # -----------------------------------------------------------------------

    @staticmethod
    def read(filename):
        raise NotImplementedError

    # -----------------------------------------------------------------------

    @staticmethod
    def get_lines(filename):
        """Return the lines of a file."""
        with codecs.open(filename, 'r', sg.__encoding__) as fp:
            lines = fp.readlines()
            fp.close()
        return lines

    # -----------------------------------------------------------------------

    @staticmethod
    def get_units_julius(lines):
        """Return the units of a palign/walign file (in frames).

        :param lines: (List of str)
        :returns: List of tuples (start, end)

        """
        units = list()
        i = 0
        while "=== begin forced alignment ===" not in lines[i]:
            i += 1
            if i > len(lines):
                raise IOError('Time units not found')

        while "=== end forced alignment ===" not in lines[i]:
            i += 1
            if i > len(lines):
                raise IOError('Time units not found in alignment result')
            if lines[i].startswith('['):
                # New phonemes
                line = lines[i].replace("[", "")
                line = line.replace("]", "")
                line = sppasUnicode(line).to_strip()
                tab = line.split()
                # tab 0: first frame
                # tab 1: last frame
                # tab 2: score of the segmentation (log proba)
                # tab 3: triphone used
                units.append((int(tab[0]), int(tab[1])))
        return units

    # -----------------------------------------------------------------------

    @staticmethod
    def get_phonemes_julius(lines):
        """Return the pronunciation of all words.

        :param lines: (List of str)
        :returns: List of tuples (ph1 ph2...phN)

        """
        phonemes = list()
        i = 0
        while lines[i].startswith('phseq1') is False:
            i += 1
            if i == len(lines):
                raise IOError('Phonemes sequence not found.')
        line = lines[i]
        line = line[7:].strip()
        if len(line) == 0:
            raise IOError('Empty phonemes sequence.')
        words = line.split('|')
        for phn in words:
            phn = phn.strip()
            phonemes.append(tuple(phn.split()))
        return phonemes

    # -----------------------------------------------------------------------

    @staticmethod
    def get_words_julius(lines):
        """Return all words.

        :param lines: (List of str)
        :returns: List

        """
        i = 0
        while lines[i].startswith('sentence1') is False:
            i += 1
            if i == len(lines):
                raise IOError('Words not found in alignment result')
        line = lines[i]
        line = line[10:]
        line = line.strip()
        return line.split()

    # -----------------------------------------------------------------------

    @staticmethod
    def get_word_scores_julius(lines):
        """Return all scores of words.

        :param lines: (List of str)
        :returns: List

        """
        i = 0
        while lines[i].startswith('cmscore1') is False:
            i += 1
            if i == len(lines):
                raise IOError('Scores not found in alignment result')
        line = lines[i]
        line = line[9:]
        line = line.strip()
        return line.split()

    # -----------------------------------------------------------------------

    @staticmethod
    def units_to_time(units, samplerate):
        """Return the conversion of units.

        Convert units (in frames) into time values (in seconds).

        :param samplerate: (int) Sample rate to be applied to the units.
        :returns: List of tuples (start, end)

        NOTE: DANS LES VERSIONS PREC. ON DECALAIT TOUT DE 10ms A DROITE.

        """
        samplerate = float(samplerate)
        u = list()
        i = 0
        while i < len(units):

            # Fix the begin of this annotation
            s = round(float(units[i][0]) / samplerate, 3)

            if i+1 < len(units):
                # Fix the end of this annotation to the begin of the next one
                e = round(float(units[i+1][0]) / samplerate, 3)
            else:
                e = round(float(units[i][1]) / samplerate, 3)

            u.append((s, e))
            i += 1

        return u

    # -----------------------------------------------------------------------

    @staticmethod
    def shift_time_units(units, delta):
        """Return the units shifted of a delta time.

        The first start time and the last end time are not shifted.

        :param units: (list of tuples) Time units
        :param delta: (float) Delta time value in range [-0.02;0.02]

        """
        if delta > 0.02:
            delta = 0.02
        if delta < -0.02:
            delta = -0.02

        shifted = list()
        i = 0
        while i < len(units):
            start, end = units[i]
            if i > 0:
                start += delta
            if i + 1 < len(units):
                end += delta
            shifted.append((round(start, 3), round(end, 3)))
            i += 1
        return shifted

    # -----------------------------------------------------------------------

    @staticmethod
    def make_result(units, words, phonemes, scores):
        """Make a unique data structure from the given data.

        :param units: (List of tuples)
        :param words: (List of str)
        :param phonemes: (List of tuples)
        :param scores: (List of str, or None)

        :returns: Two data structures

            1. List of (start_time end_time phoneme None)
            2. List of (start_time end_time word score)

        """
        if scores is None:
            scores = [None]*len(words)
        aligned_words = list()
        aligned_phones = list()
        i = 0
        for wd, phn_seq, sc in zip(words, phonemes, scores):

            start_wd = units[i][0]
            for phn in phn_seq:
                if i == len(units):
                    raise IOError('Phonemes/Units are not matching '
                                  'in alignment result')
                start_phn, end_phn = units[i]
                aligned_phones.append((start_phn, end_phn, phn, None))
                i += 1

            end_wd = units[i - 1][1]
            aligned_words.append((start_wd, end_wd, wd, sc))

        return aligned_phones, aligned_words

# ---------------------------------------------------------------------------


class palign(BaseAlignersReader):
    """palign reader/writer of time-aligned files (Julius CSR Engine).

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self):
        """Create a palign instance to read palign files of Julius."""
        super(palign, self).__init__()
        self.extension = "palign"

    # -----------------------------------------------------------------------

    @staticmethod
    def read(filename):
        """Read an alignment file in the format of Julius CSR engine.

        :param filename: (str) The input file name.
        :returns: 3 lists of tuples

            1. List of (start-time end-time phoneme None)
            2. List of (start-time end-time word None)
            3. List of (start-time end-time pron_word score)

        """
        b = BaseAlignersReader()
        lines = b.get_lines(filename)
        try:
            phonemes = b.get_phonemes_julius(lines)
        except IOError:
            logging.error('Got no time-aligned phonemes in file {:s}:'
                          ''.format(filename))
            raise

        words = b.get_words_julius(lines)
        pron_words = [separators.phonemes.join(phn) for phn in phonemes]
        scores = b.get_word_scores_julius(lines)

        if len(words) != len(phonemes):
            logging.error('Words/Phonemes are not matching in file: {:s}'
                          ''.format(filename))
            logging.error('   - words: {}'.format(words))
            logging.error('   - phonemes: {}'.format(phonemes))
            raise IOError("Words/Phonemes are not matching "
                          "in alignment result of file {:s}".format(filename))

        if len(words) != len(scores):
            logging.error('Words/Scores are not matching in file: {:s}'
                          ''.format(filename))
            logging.error('   - words: {}'.format(words))
            logging.error('   - scores: {}'.format(scores))
            raise IOError("Words/Scores are not matching in alignment result "
                          "of file {:s}".format(filename))

        units = b.get_units_julius(lines)
        units = b.units_to_time(units, 100)
        units = b.shift_time_units(units, 0.01)

        data_phon, data_words = b.make_result(units, words, phonemes, None)
        d, data_pron = b.make_result(units, pron_words, phonemes, scores)
        return data_phon, data_words, data_pron

    # -----------------------------------------------------------------------

    @staticmethod
    def write(phoneslist, tokenslist, alignments, outputfilename):
        """Write an alignment output file.

        :param phoneslist: (list) The phonetization of each token
        :param tokenslist: (list) Each token
        :param alignments: (list) Tuples (start-time end-time phoneme)
        :param outputfilename: (str) Output file name (a Julius-like output).

        """
        with codecs.open(outputfilename, 'w', sg.__encoding__) as fp:

            fp.write("----------------------- System Information begin "
                     "---------------------\n")
            fp.write("\n")
            fp.write("                        Basic Alignment\n")
            fp.write("\n")
            fp.write("----------------------- System Information end "
                     "-----------------------\n")

            fp.write("\n### Recognition: 1st pass\n")

            fp.write("pass1_best: ")
            fp.write("{:s}\n".format(" ".join(tokenslist)))

            fp.write("pass1_best_wordseq: ")
            fp.write("{:s}\n".format(" ".join(tokenslist)))

            fp.write("pass1_best_phonemeseq: ")
            fp.write("{:s}\n".format(" | ".join(phoneslist)))

            fp.write("\n### Recognition: 2nd pass\n")

            fp.write("ALIGN: === phoneme alignment begin ===\n")

            fp.write("sentence1: ")
            fp.write("{:s}\n".format(" ".join(tokenslist)))

            fp.write("wseq1: ")
            fp.write("{:s}\n".format(" ".join(tokenslist)))

            fp.write("phseq1: ")
            fp.write("{:s}\n".format(" | ".join(phoneslist)))

            fp.write("cmscore1: ")
            fp.write("{:s}\n".format("0.000 "*len(phoneslist)))

            fp.write("=== begin forced alignment ===\n")
            fp.write("-- phoneme alignment --\n")
            fp.write(" id: from  to    n_score    unit\n")
            fp.write(" ----------------------------------------\n")
            for tv1, tv2, phon in alignments:
                fp.write("[ {:d} ".format(tv1))
                fp.write(" {:d}]".format(tv2))
                fp.write(" -30.000000 " + str(phon) + "\n")
            fp.write("=== end forced alignment ===\n")

            fp.close()

# ---------------------------------------------------------------------------


class walign(BaseAlignersReader):
    """walign reader of time-aligned files (Julius CSR Engine).

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self):
        """Create a walign instance to read walign files of Julius."""
        super(walign, self).__init__()
        self.extension = "walign"

    # -----------------------------------------------------------------------

    @staticmethod
    def read(filename):
        """Read an alignment file in the format of Julius CSR engine.

        :param filename: (str) The input file name.
        :returns: A list of tuples (start-time end-time word score)

        """
        b = BaseAlignersReader()
        lines = b.get_lines(filename)
        words = b.get_words_julius(lines)
        scores = b.get_word_scores_julius(lines)
        if len(words) != len(scores):
            logging.error('Got words: {}'.format(words))
            logging.error('Got scores: {}'.format(scores))
            raise IOError("Words/Scores are not matching in alignment result")
        units = b.get_units_julius(lines)
        units = b.units_to_time(units, 100)
        units = b.shift_time_units(units, 0.01)

        aligned_words = list()
        i = 0
        for wd, sc in zip(words, scores):
            if i == len(units):
                logging.error('Got words: {}'.format(words))
                logging.error('Got units: {}'.format(units))
                raise IOError('Phonemes/Units are not matching '
                              'in alignment result')

            start_wd = units[i][0]
            end_wd = units[i][1]
            aligned_words.append((start_wd, end_wd, wd, sc))
            i += 1

        return aligned_words

# ---------------------------------------------------------------------------


class mlf(BaseAlignersReader):
    """mlf reader of time-aligned files (HTK Toolkit).

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    When the -m option is used, the transcriptions output by HVITE would by
    default contain both the model level and word level transcriptions .
    For example, a typical fragment of the output might be:

        7500000  8700000 f  -1081.604736 FOUR 30.000000
        8700000  9800000 ao  -903.821350
        9800000 10400000 r   -665.931641
       10400000 10400000 sp    -0.103585
       10400000 11700000 s  -1266.470093 SEVEN 22.860001
       11700000 12500000 eh  -765.568237
       12500000 13000000 v   -476.323334
       13000000 14400000 n  -1285.369629
       14400000 14400000 sp    -0.103585

    """

    def __init__(self):
        """Create a mlf instance to parse mlf files from HVite."""
        super(mlf, self).__init__()
        self.extension = "mlf"

    # -----------------------------------------------------------------------

    @staticmethod
    def is_integer(s):
        """Check whether a string is an integer or not.

        :param s: (str or unicode)
        :returns: (bool)

        """
        try:
            int(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    # -----------------------------------------------------------------------

    @staticmethod
    def get_units(lines):
        """Return the units of a mlf file (in nano-seconds).

        :param lines: (List of str)
        :returns: List of tuples (start, end)

        """
        units = list()
        for line in lines:
            columns = line.split()
            if len(columns) > 3:
                if mlf.is_integer(columns[0]) and mlf.is_integer(columns[1]):
                    units.append((int(columns[0]), int(columns[1])))
        return units

    # -----------------------------------------------------------------------

    @staticmethod
    def get_phonemes(lines):
        """Return the pronunciation of all words.

        :param lines: (List of str)
        :returns: List of tuples (ph1 ph2...phN)

        """
        phonemes = list()
        phon_seq = list()
        for line in lines:
            columns = line.split()
            if len(columns) > 3:
                if mlf.is_integer(columns[0]) and mlf.is_integer(columns[1]):
                    phon = columns[2]
                    if len(columns) >= 5:
                        if len(phon_seq) > 0:
                            phonemes.append(tuple(phon_seq))
                            phon_seq = list()
                    phon_seq.append(phon)
        if len(phon_seq) > 0:
            phonemes.append(tuple(phon_seq))

        return phonemes

    # -----------------------------------------------------------------------

    @staticmethod
    def get_words(lines):
        """Return all words.

        :param lines: (List of str)
        :returns: List

        """
        words = list()
        for line in lines:
            columns = line.split()
            if len(columns) > 3:
                if mlf.is_integer(columns[0]) and mlf.is_integer(columns[1]):
                    if len(columns) >= 5:
                        words.append(columns[4])
        return words

    # -----------------------------------------------------------------------

    @staticmethod
    def read(filename):
        """Read an alignment file (a mlf file).

        :param filename: (str) the input file (a HVite mlf output file).

        :returns: 2 lists of tuples:
            - (start-time end-time phoneme None)
            - (start-time end-time word None)

        """
        b = BaseAlignersReader()
        lines = b.get_lines(filename)
        units = mlf.get_units(lines)
        units = b.units_to_time(units, 10e6)
        units = b.shift_time_units(units, 0.01)

        phonemes = mlf.get_phonemes(lines)
        pron_words = [separators.phonemes.join(phn) for phn in phonemes]
        words = mlf.get_words(lines)
        if len(words) != len(phonemes):
            logging.error('Got words: {}'.format(words))
            logging.error('Got phonemes: {}'.format(phonemes))
            raise IOError("Words/Phonemes are not matching "
                          "in alignment result")

        data_phon, data_words = b.make_result(units, words, phonemes, None)
        data_phon, data_pron = b.make_result(units, pron_words, phonemes, None)
        return data_phon, data_words, data_pron

# ---------------------------------------------------------------------------


class AlignerIO(object):
    """Reader/writer of the output files of the aligners.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    AlignerIO implements methods to read/write files of the external aligner
    systems.

    """

    # List of file extensions this class is able to read and/or write.
    EXTENSIONS_READ = {palign().extension: palign,
                       mlf().extension: mlf,
                       walign().extension: walign}
    EXTENSIONS_WRITE = {palign().extension: palign}

    # -----------------------------------------------------------------------

    @staticmethod
    def read_aligned(basename):
        """Find an aligned file and read it.

        :param basename: (str) File name without extension
        :returns: Two lists of tuples with phones and words
            - (start-time end-time phoneme score)
            - (start-time end-time word score)

        The score can be None.
        todo: The "phoneme" column can be a sequence of alternative phonemes.

        """
        for ext in AlignerIO.EXTENSIONS_READ:
            track_name = basename + "." + ext
            if os.path.isfile(track_name) is True:
                return AlignerIO.EXTENSIONS_READ[ext]().read(track_name)

        raise IOError('No time-aligned file was found for {:s}'
                      ''.format(basename))
