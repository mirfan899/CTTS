#!/usr/bin python
"""

:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file and filter depending on the label.

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
from sppas.src.anndata import sppasTranscription
from sppas.src.analysis import sppasTierFilters
from sppas.src.utils.makeunicode import u

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

filename = 'F_F_B003-P9-merge.TextGrid'
output_filename = filename.replace('.TextGrid', '.csv')

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def get_tier(filename, tier_name, verbose=True):
    """ Get a tier from a file.

    :param filename: (str) Name of the annotated file.
    :param tier_name: (str) Name of the tier
    :param verbose: (bool) Print message
    :returns: (Tier)

    """
    # Read an annotated file.
    if verbose:
        print("Read file: {:s}".format(filename))
    parser = sppasRW(filename)
    trs = parser.read()
    if verbose:
        print(" ... [  OK  ] ")

    # Get the expected tier
    if verbose:
        print("Get tier {:s}".format(tier_name))

    tier = trs.find(tier_name, case_sensitive=False)
    if tier is None:
        print("Tier not found.")
        sys.exit(1)
    if verbose:
        print(" ... [  OK  ] ")

    return tier

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


if __name__ == '__main__':

    # Get data: the tier with phonemes
    # -------------------------------------------------------------

    verbose = True
    tier = get_tier(filename, "PhonAlign", verbose)

    # Create a filter object
    f = sppasTierFilters(tier)

    # Apply a filter: Extract phonemes 'a'
    # ------------------------------------
    phon_set_a = f.tag(exact=u("a"))

    if verbose:
        print("{:s} has the following {:d} 'a':"
              "".format(tier.get_name(), len(phon_set_a)))
        for ann in phon_set_a:
            print(' - {}: {}'.format(ann.get_location().get_best(),
                                     phon_set_a.get_value(ann)))

    # convert the data set into a tier
    tier_phon_a = phon_set_a.to_tier(name="Phon-a")

    # Apply a filter: Extract phonemes 'a', 'A', 'E' and 'e'
    # ------------------------------------------------------
    phon_set_a_e = f.tag(iexact=u("a")) | f.tag(iexact=u("e"))

    # convert the data set into a tier
    tier_phon_a_e = phon_set_a_e.to_tier(name="Phon-a-e")

    if verbose:
        print("{:s} has {:d} phonemes 'aeAE'.".format(tier.get_name(), len(tier_phon_a_e)))

    # Save
    # -------------------------------------------------------------
    t = sppasTranscription()
    t.append(tier_phon_a)
    t.append(tier_phon_a_e)
    parser = sppasRW(output_filename)
    parser.write(t)
    if verbose:
        print("File {:s} saved".format(output_filename))
