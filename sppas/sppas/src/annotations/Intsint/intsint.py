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

    src.annotations.Intsint.intsint.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import math
from ..annotationsexc import SmallSizeInputError

# ----------------------------------------------------------------------------

BIG_NUMBER = 32764

# ----------------------------------------------------------------------------


def octave(value):
    return math.log(value) / math.log(2)

# ----------------------------------------------------------------------------


def linear(value):
    return 2 ** value

# -------------------------------------------------------------------


class Intsint(object):
    """Provide optimal INTSINT coding for anchor points.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    # parameters for data checking.
    MIN_F0 = 60  # (Hz)
    MAX_F0 = 600  # (Hz)

    # parameters for optimization.
    MIN_PAUSE = 0.5  # seconds
    MIN_RANGE = 0.5  # octaves
    MAX_RANGE = 2.5  # octaves
    STEP_RANGE = 0.1  # octaves
    MEAN_SHIFT = 50  # (Hz)
    STEP_SHIFT = 1  # (Hz)

    # parameters for target estimation.
    HIGHER = 0.5
    LOWER = 0.5
    UP = 0.25
    DOWN = 0.25

    # List of "absolute" tones
    TONES_ABSOLUTE = ['T', 'M', 'B']

    # List of "relative" tones
    TONES_RELATIVE = ['H', 'L', 'U', 'D', 'S']

    # All tones
    TONES = TONES_ABSOLUTE + TONES_RELATIVE

    # -------------------------------------------------------------------

    def __init__(self):
        """Create a new Intsint instance."""
        self.best_intsint = None
        self.best_estimate = None

        self.intsint = []
        self.estimates = []
        self.targets = []
        self.time = []

        self.mid = 0
        self.top = 0
        self.bottom = 0
        self.last_estimate = 0

        self.best_mid = 0
        self.best_range = 0
        self.min_mean = 0
        self.max_mean = 0
        self.min_ss_error = 0

    # -------------------------------------------------------------------

    def reset(self):
        """Fix all member to their initial value."""
        self.best_intsint = None
        self.best_estimate = None

        self.intsint = []
        self.estimates = []
        self.targets = []
        self.time = []

        self.mid = 0
        self.top = 0
        self.bottom = 0
        self.last_estimate = 0

        self.best_mid = 0
        self.best_range = 0
        self.min_mean = 0
        self.max_mean = 0
        self.min_ss_error = 0

    # -------------------------------------------------------------------

    def adjust_f0(self, f0):
        """Return F0 value within self range of values.

        :param f0: (float) Input pitch value.
        :returns: (float) Normalized pitch value.

        """
        if f0 < Intsint.MIN_F0:
            return Intsint.MIN_F0

        if f0 > Intsint.MAX_F0:
            return Intsint.MAX_F0

        return f0

    # -------------------------------------------------------------------

    def init(self, momel_anchors):
        """Initialize INTSINT attributes from a list of targets.

        :param momel_anchors: (list of tuple) List of time
        (in seconds) and anchors (Hz).

        """
        self.reset()
        for (time, target) in momel_anchors:
            # Convert f0 to octave scale
            self.targets.append(octave(self.adjust_f0(target)))
            self.time.append(time)

        self.intsint = [""]*len(self.targets)
        self.estimates = [0]*len(self.targets)

        sum_octave = sum(self.targets)
        mean_f0 = float(sum_octave) / float(len(self.targets))
        linear_mean_f0 = round(linear(mean_f0))
        self.min_mean = linear_mean_f0 - Intsint.MEAN_SHIFT
        self.max_mean = linear_mean_f0 + Intsint.MEAN_SHIFT
        self.min_ss_error = BIG_NUMBER

    # -------------------------------------------------------------------

    def optimise(self, mid, _range):
        """Fix tones.

        :param mid:
        :param _range:

        """
        self.top = mid + _range / 2
        self.bottom = mid - _range / 2
        f0 = self.targets[0]

        if self.top - f0 < math.fabs(f0 - mid):
            self.intsint[0] = "T"
        elif f0 - self.bottom < math.fabs(f0 - mid):
            self.intsint[0] = "B"
        else:
            self.intsint[0] = "M"

        estimated = self.estimate(self.intsint[0], self.last_estimate)
        self.estimates[0] = estimated
        error = math.fabs(estimated - self.targets[0])
        ss_error = error * error
        self.last_estimate = estimated

        for i in range(1, len(self.targets)):
            target = self.targets[i]

            # after pause choose from (MTB)
            if self.time[i] - self.time[i - 1] > Intsint.MIN_PAUSE:
                if self.top - target < math.fabs(target - mid):
                    self.intsint[i] = "T"
                elif target - self.bottom < math.fabs(target - mid):
                    self.intsint[i] = "B"
                else:
                    self.intsint[i] = "M"
            # elsewhere any tone except M
            else:
                min_difference = BIG_NUMBER
                best_tone = ""
                for tone in Intsint.TONES:
                    if tone != "M":
                        estimate = self.estimate(tone, self.last_estimate)
                        difference = math.fabs(target - estimate)
                        if difference < min_difference:
                            min_difference = difference
                            best_tone = tone

                self.intsint[i] = best_tone

            estimate = self.estimate(self.intsint[i], self.last_estimate)
            self.estimates[i] = estimate
            error = math.fabs(estimate - self.targets[i])
            ss_error += error * error
            self.last_estimate = estimate

        if ss_error < self.min_ss_error:
            self.min_ss_error = ss_error
            self.best_range = _range
            self.best_mid = mid
            self.best_intsint = self.intsint[:]
            self.best_estimate = self.estimates[:]

    # -------------------------------------------------------------------

    def estimate(self, tone, last_anchor):
        """Estimate f0 from current tone and last target.

        :param tone:
        :param last_anchor:

        """
        estimated = ""
        if tone == "M":
            estimated = self.mid
        elif tone == "S":
            estimated = last_anchor
        elif tone == "T":
            estimated = self.top
        elif tone == "H":
            estimated = last_anchor + \
                        (self.top - last_anchor) * Intsint.HIGHER
        elif tone == "U":
            estimated = last_anchor + \
                        (self.top - last_anchor) * Intsint.UP
        elif tone == "B":
            estimated = self.bottom
        elif tone == "L":
            estimated = last_anchor - \
                        (last_anchor - self.bottom) * Intsint.LOWER
        elif tone == "D":
            estimated = last_anchor - \
                        (last_anchor - self.bottom) * Intsint.DOWN

        return estimated

    # -------------------------------------------------------------------

    def recode(self):
        """Recode within the parameters space.

        mean +/- 50 Hz for key and [0.5..2.5 octaves] for range.

        """
        _range = Intsint.MIN_RANGE

        while _range < Intsint.MAX_RANGE:
            lm = self.min_mean
            while lm < self.max_mean:
                self.mid = octave(lm)
                self.optimise(self.mid, _range)
                lm += Intsint.STEP_SHIFT

            _range += Intsint.STEP_RANGE

    # -------------------------------------------------------------------

    def annotate(self, momel_anchors):
        """Provide optimal INTSINT coding for sequence of target points.

        :param momel_anchors: (list of tuple) List of time (in seconds)
        and anchors (Hz).

        """
        if len(momel_anchors) < 2:
            raise SmallSizeInputError(2)

        self.init(momel_anchors)
        self.recode()
        return self.best_intsint
