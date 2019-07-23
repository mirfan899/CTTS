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

    src.audiodata.aio.__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Readers and writers of audio data.

"""
from os.path import splitext

from sppas.src.utils.makeunicode import u

from ..audiodataexc import AudioIOError
from .audiofactory import sppasAudioFactory

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------


ext_wav = ['.wav', '.wave', '.[wWaAvV]', '.[wWaAvVeE]']
ext_aiff = ['.aif', '.aiff', '.[aAiIfF]']
ext_sunau = ['.au', '.[aAuU]']

extensions = ['.wav', '.wave', '.au']
extensionsul = ext_wav + ext_sunau

# ----------------------------------------------------------------------------


def get_extension(filename):
    return splitext(filename)[1][1:]

# ----------------------------------------------------------------------------
# Functions for opening and saving audio files.
# ----------------------------------------------------------------------------


def open(filename):
    """Open an audio file.

    :param filename: (str) the file name (including path)
    :raise: IOError, UnicodeError, Exception
    :returns: sppasAudioPCM()

    >>> Open an audio file:
    >>> audio = audiodata.aio.open(filename)

    """
    ext = get_extension(filename).lower()
    aud = sppasAudioFactory.new_audio_pcm(ext)
    try:
        aud.open(u(filename))
    except IOError as e:
        raise AudioIOError(message=str(e), filename=None)
    except EOFError:
        raise AudioIOError(message="Malformed file", filename=None)

    return aud

# ----------------------------------------------------------------------------


def save(filename, audio):
    """Write an audio file.

    :param filename: (str) the file name (including path)
    :param audio: (sppasAudioPCM) the Audio to write.
    :raises: IOError

    """
    ext = get_extension(filename).lower()
    output = sppasAudioFactory.new_audio_pcm(ext)

    output.set(audio)
    output.save(u(filename))

# ----------------------------------------------------------------------------


def save_fragment(filename, audio, frames):
    """Write a fragment of frames of an audio file.

    :param filename: (str) the file name (including path)
    :param audio: (sppasAudioPCM) the Audio to write.
    :param frames: (str)
    :raises: IOError

    """
    ext = get_extension(filename).lower()
    output = sppasAudioFactory.new_audio_pcm(ext)

    output.set(audio)
    output.save_fragment(filename, frames)
