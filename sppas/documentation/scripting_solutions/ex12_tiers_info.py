#!/usr/bin python
"""

:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file and print information about tiers.

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

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

# Create a parser object then parse the input file.
print("Quick look on file {:s}:".format(filename))
parser = sppasRW(filename)
trs = parser.read()

for tier in trs:

    # Get the tier type
    tier_type = "Unknown"
    if tier.is_point() is True:
        tier_type = "Point"
    elif tier.is_interval() is True:
        tier_type = "Interval"

    # Print all information
    print(" * Tier: {:s}".format(tier.get_name()))
    print("    - Type: {:s}".format(tier_type))
    print("    - Number of annotations: {:d}".format(len(tier)))
    if len(tier) > 1:
        print("    - From time: {:.4f}".format(tier.get_first_point().get_midpoint()))
        print("    - To time: {:.4f} ".format(tier.get_last_point().get_midpoint()))
