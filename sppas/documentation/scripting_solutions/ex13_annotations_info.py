#!/usr/bin python
"""

:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file and print information about annotations
               of a given tier.

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
sys.path.append(os.path.join("..", ".."))

from sppas.src.anndata import sppasRW


# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

filename = 'F_F_B003-P9-merge.TextGrid'
tiername = "PhonAlign"

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

# Create a parser object then parse the input file.
print("Quick look on file {:s}:".format(filename))
parser = sppasRW(filename)
trs = parser.read()
tier = trs.find(tiername, case_sensitive=False)

if tier is None:
    print("No tier {:s} in file {:s} ".format(tiername, filename))
    sys.exit(1)

# Check the tier type
tier_type = "Unknown"
if tier.is_point() is True:
    tier_type = "Point"
elif tier.is_interval() is True:
    tier_type = "Interval"

# Get the number of silences
nb_silence = 0
nb_empty = 0
dur_silence = 0.
dur_empty = 0.

for ann in tier:
    for label in ann.get_labels():
        if label.get_best().is_silence():
            nb_silence += 1
            dur_silence += ann.get_location().get_best().duration().get_value()
        elif label.get_best().is_empty():
            nb_empty += 1
            dur_empty += ann.get_location().get_best().duration().get_value()

# Print all information
print(" Tier: {:s}".format(tier.get_name()))
print("    - Type: {:s}".format(tier_type))
print("    - Number of annotations:      {:d}".format(len(tier)))
print("    - Number of silences:         {:d}".format(nb_silence))
print("    - Number of empty intervals:  {:d}".format(nb_empty))
print("    - Number of speech intervals: {:d}".format(len(tier) - (nb_empty + nb_silence)))
print("    - Silence duration: {:.3f}".format(dur_silence))
print("    - Empties duration: {:.3f}".format(dur_empty))
print("    - Speech duration:  {:.3f}".format((tier.get_last_point().get_midpoint() -
                                               tier.get_first_point().get_midpoint() -
                                               (dur_empty + dur_silence))))
