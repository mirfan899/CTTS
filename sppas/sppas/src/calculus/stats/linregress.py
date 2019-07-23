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

    src.calculus.stats.linregress.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

The goal of linear regression is to fit a line to a set of points.
Equation of the line is y = mx + b
where m is slope, b is y-intercept.

"""

from .central import fmean
from .central import fsum

# ---------------------------------------------------------------------------


def compute_error_for_line_given_points(b, m, points):
    """Error function (also called a cost function).

    It measures how "good" a given line is.

    This function will take in a (m,b) pair and return an
    error value based on how well the line fits our data.
    To compute this error for a given line, we'll iterate through each (x,y)
    point in our data set and sum the square distances between each point's y
    value and the candidate line's y value (computed at mx + b).

    Lines that fit our data better (where better is defined by our error
    function) will result in lower error values.

    """
    total_error = 0
    for x, y in points:
        total_error += (y - (m * x + b)) ** 2
    return total_error / float(len(points))

# ---------------------------------------------------------------------------


def step_gradient(b_current, m_current, points, learning_rate):
    """One step of a gradient linear regression.

    To run gradient descent on an error function, we first need to compute
    its gradient. The gradient will act like a compass and always point us
    downhill. To compute it, we will need to differentiate our error function.
    Since our function is defined by two parameters (m and b), we will need
    to compute a partial derivative for each.

    Each iteration will update m and b to a line that yields slightly lower
    error than the previous iteration.

    The learning_rate variable controls how large of a step we take downhill
    during each iteration. If we take too large of a step, we may step over
    the minimum. However, if we take small steps, it will require many
    iterations to arrive at the minimum.

    """
    b_gradient = 0
    m_gradient = 0
    n = float(len(points))
    for x, y in points:
        b_gradient += -(2./n) * (y - ((m_current * x) + b_current))
        m_gradient += -(2./n) * x * (y - ((m_current * x) + b_current))
    new_b = b_current - (learning_rate * b_gradient)
    new_m = m_current - (learning_rate * m_gradient)

    return [new_b, new_m]

# ---------------------------------------------------------------------------


def gradient_descent(points,
                     starting_b, starting_m, learning_rate, num_iterations):
    """Gradient descent is an algorithm that minimizes functions.

    Given a function defined by a set of parameters, gradient descent starts
    with an initial set of parameter values and iteratively moves toward a set
    of parameter values that minimize the function. This iterative minimization
    is achieved using calculus, taking steps in the negative direction of
    the function gradient.

    :param points: a list of tuples (x,y) of float values.
    :param starting_b: (float)
    :param starting_m: (float)
    :param learning_rate: (float)
    :param num_iterations: (int)
    :returns: intercept, slope

    """
    if len(points) == 0:
        return 0.
    b = starting_b
    m = starting_m
    for i in range(num_iterations):
        b, m = step_gradient(b, m, points, learning_rate)

    return b, m

# ---------------------------------------------------------------------------


def gradient_descent_linear_regression(points, num_iterations=50000):
    """Gradient descent method for linear regression.

    adapted from:
    http://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/

    :param points: a list of tuples (x,y) of float values.
    :param num_iterations: (int)
    :returns: intercept, slope

    """
    g = gradient_descent(points,
                         starting_b=0.,  # initial y-intercept guess
                         starting_m=0.,  # initial slope guess
                         learning_rate=0.0001,
                         num_iterations=num_iterations)
    return g

# ---------------------------------------------------------------------------


def tga_linear_regression(points):
    """Linear regression as proposed in TGA, by Dafydd Gibbon.

    http://wwwhomes.uni-bielefeld.de/gibbon/TGA/

    :param points: a list of tuples (x,y) of float values.
    :returns: intercept, slope

    """
    if len(points) == 0:
        return 0.

    # Fix means
    mean_x = fmean([x for x, y in points])
    mean_y = fmean([y for x, y in points])

    xy_sum = 0.
    xsq_sum = 0.
    for x, y in points:
        dx = x - mean_x
        dy = y - mean_y
        xy_sum += (dx*dy)
        xsq_sum += (dx*dx)

    # Intercept
    m = xy_sum
    if xsq_sum != 0:
        m = xy_sum / xsq_sum

    # Slope
    b = mean_y - m * mean_x

    return b, m

# ---------------------------------------------------------------------------


def tansey_linear_regression(points):
    """Linear regression, as proposed in AnnotationPro.

    http://annotationpro.org/

    Translated from C# code from here:
    https://gist.github.com/tansey/1375526

    :param points: a list of tuples (x,y) of float values.
    :returns: intercept, slope

    """
    if len(points) == 0:
        return 0.

    sum_x_sq = 0.
    sum_codeviates = 0.
    n = len(points)

    for x, y in points:
        sum_codeviates += (x*y)
        sum_x_sq += (x*x)

    sum_x = fsum([x for x, y in points])
    sum_y = fsum([y for x, y in points])
    mean_x = fmean([x for x, y in points])
    mean_y = fmean([y for x, y in points])

    ssx = sum_x_sq - ((sum_x*sum_x) / n)
    sco = sum_codeviates - ((sum_x * sum_y) / n)

    b = mean_y - ((sco / ssx) * mean_x)
    m = sco / ssx

    return b, m
