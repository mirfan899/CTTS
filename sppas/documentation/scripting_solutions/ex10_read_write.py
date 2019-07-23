#!/usr/bin python2
"""

:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file and save it as CSV file.

Use of this software is governed by the GNU Public License, version 3.

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this script. If not, see <http://www.gnu.org/licenses/>.

""" 
import sys
import os.path
SPPAS_IS_HERE = os.path.join("..", "..")
sys.path.append(SPPAS_IS_HERE)

from sppas.src.anndata import sppasRW

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

input_filename = 'F_F_B003-P9-merge.TextGrid'
output_filename = input_filename.replace('.TextGrid', '.csv')

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

if __name__ == '__main__':

    # Create a parser object then parse the input file.
    parser = sppasRW(input_filename)
    trs = parser.read()

    # Save the Transcription object into a file.
    parser.set_filename(output_filename)
    parser.write(trs)
