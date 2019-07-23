#!/usr/bin python
"""

:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file, select tiers and save into a new file.

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

# ----------------------------------------------------------------------------
# Get SPPAS API
# ----------------------------------------------------------------------------

import sys
import os.path
SPPAS_IS_HERE = os.path.join("..", "..")
sys.path.append(SPPAS_IS_HERE)

from sppas.src.anndata import sppasRW
from sppas.src.anndata import sppasTranscription

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

# The input file name
filename = 'F_F_B003-P9-merge.TextGrid'

# The list of tiers we want to select
tier_names = ['PhonAlign', 'TokensAlign', 'toto']

# The output file name
output_filename = 'F_F_B003-P9-selection.TextGrid'

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

# Create a parser object then parse the input file.
parser = sppasRW(filename)
print("Read the file {:s}".format(filename))
trs = parser.read()
print("   Number of tiers: {:d}.".format(len(trs)))

# Create a new Transcription to add selected tiers.
new_trs = sppasTranscription("Selected")

# Select some tiers, add into the new Transcription
for name in tier_names:
    tier = trs.find(name, case_sensitive=False)
    if tier is not None:
        new_trs.append(tier)
        print("  - Tier {:s} successfully added.".format(tier.get_name()))
    else:
        print("  - Error: the file does not contain a tier with name {:s}".format(name))

# Save the Transcription object into a file.
parser.set_filename(output_filename)
parser.write(new_trs)
if os.path.exists(output_filename) is True:
    print("The file {:s} was successfully saved.".format(output_filename))
else:
    print("The file {:s} wasn't saved.".format(output_filename))
