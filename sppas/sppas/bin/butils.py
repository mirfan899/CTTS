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

    bin.butils.py
    ~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Utility functions for scripts of the bin directory.

"""
import os
import sys
import time
import subprocess

# ----------------------------------------------------------------------------

EXIT_DELAY = 6
EXIT_STATUS = 1

# ----------------------------------------------------------------------------


def exit_error(msg="Unknown."):
    """Exit the program with status 1 and an error message.

    :param msg: (str) Message to print on stdout.

    """
    print("[ ERROR ] {:s}".format(msg))
    time.sleep(EXIT_DELAY)
    sys.exit(EXIT_STATUS)

# ----------------------------------------------------------------------------


def check_python():
    """Check if the current python in use is the right one: 2.7.something.

    Exit if it's not the case.

    """
    if sys.version_info < (2, 7):
        exit_error("The version of Python is too old: "
                   "SPPAS requires exactly the version 2.7.something.")

    if sys.version_info >= (3, 0):
        exit_error("The version of Python is not the right one: "
                   "SPPAS requires exactly the version 2.7.something.")

# ----------------------------------------------------------------------------


def check_aligner():
    """Test if one of julius/HVite is available.

    :returns: False if none of them are available.

    """
    julius = True
    hvite = True
    try:
        NULL = open(os.devnull, "r")
        subprocess.call(['julius'], stdout=NULL, stderr=subprocess.STDOUT)
    except OSError:
        julius = False

    try:
        NULL = open(os.devnull, "r")
        subprocess.call(['HVite'], stdout=NULL, stderr=subprocess.STDOUT)
    except OSError:
        hvite = False

    return julius or hvite
