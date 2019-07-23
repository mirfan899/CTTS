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

    src.calculus.scoring.ubpa.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

Estimates the Unit Boundary Positioning Accuracy.

"""
import sys


def _eval_index(step, value):
    m = (value % step)  # Estimate the rest
    d = (value-m)       # Make "d" an entire value
    index = d/step      # evaluate the index depending on step
    return int(index)


def _inc(vector, idx):
    if idx >= len(vector):
        toadd = idx - len(vector) + 1
        vector.extend([0]*toadd)
    vector[idx] += 1


def ubpa(vector, text, fp=sys.stdout, delta_max=0.04, step=0.01):
    """Estimate the Unit Boundary Positioning Accuracy.

    :param vector: contains the list of the delta values.
    :param text: one of "Duration", "Position Start", ...
    :param fp: a file pointer
    :param delta_max: Maximum delta duration to print result (default: 40ms)
    :param step: Delta time (default: 10ms)

    :returns: (tab_neg, tab_pos) with number of occurrences of each position

    """
    # Estimates the UBPA
    tab_neg = []
    tab_pos = []

    for delta in vector:
        if delta > 0.:
            idx = _eval_index(step, delta)
            _inc(tab_pos, idx)
        else:
            idx = _eval_index(step, delta*-1.)
            _inc(tab_neg, idx)

    # Print the result
    nb_values = len(vector)
    verif_values = 0
    fp.write("|--------------------------------------------| \n")
    fp.write("|      Unit Boundary Positioning Accuracy    | \n")
    fp.write("|            Delta=T(hyp)-T(ref)             | \n")
    fp.write("|--------------------------------------------| \n")
    i = len(tab_neg)-1
    percentsum = 0
    for value in reversed(tab_neg):
        verif_values += value
        if (i+1)*step <= delta_max:
            percent = (value*100.) / nb_values
            fp.write("|  Delta-%s < -%.3f: %d (%.2f%%) \n" % (text, (i+1)*step, value, percent))
            percentsum += percent
        i -= 1
    fp.write("|--------------------------------------------| \n")
    for i, value in enumerate(tab_pos):
        verif_values += value
        if (i+1)*step <= delta_max:
            percent = round(((value*100.)/nb_values), 3)
            fp.write("|  Delta-%s < +%.3f: " % (text, ((i+1)*step)))
            fp.write("%d (%.2f%%)\n" % (value, percent))
            percentsum += percent
    fp.write("|--------------------------------------------| \n")
    fp.write("| Total: {0:.2f} %                           | \n"
             "".format(round(percentsum, 3)))
    fp.write("|--------------------------------------------| \n")

