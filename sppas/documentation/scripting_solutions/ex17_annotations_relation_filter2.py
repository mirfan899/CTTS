#!/usr/bin python
"""
:author:       Brigitte Bigi
:date:         2018-07-09
:contact:      contact@sppas.org
:license:      GPL, v3
:copyright:    Copyright (C) 2018 Brigitte Bigi, Laboratoire Parole et Langage

:summary:      Open an annotated file and filter to answer the following request:
               get tokens either preceded by OR followed by a silence.

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

from sppas.src.analysis import sppasTierFilters
from sppas.src.utils.makeunicode import u
from .ex15_annotations_label_filter import get_tier

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

filename = 'F_F_B003-P9-merge.TextGrid'

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

# Read an annotated file.
tier = get_tier(filename, "TokensAlign")
tier.set_radius(0.005)
f = sppasTierFilters(tier)

# get tokens, except silences
annset_not_sil = f.tag(not_exact=u("#"))
tier_tokens = annset_not_sil.to_tier('Tokens')

# get silences
annset_sil = f.tag(exact=u("#"))
tier_silences = annset_sil.to_tier('Silences')

# Find annotations of tiers with relations 'meets' or 'metby'.
# Replace the label of the token by the name of the relation
# If both relations are true, relation' names are concatenated.
fr = sppasTierFilters(tier_tokens)
ann_set = fr.rel(tier_silences, 'meets', 'metby')

for ann in ann_set:
    print(' - {}: {}'.format(ann, ann_set.get_value(ann)))
