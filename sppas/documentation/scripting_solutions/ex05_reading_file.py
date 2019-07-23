#!/usr/bin python
"""

:author:       Fix Me
:date:         Now
:contact:      me@me.org
:license:      GPL, v3
:copyright:    Copyright (C) 2017  Fixme

:summary:      Simple script to open and read a file.

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
import codecs
import sys

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

#myfile="C:\phonemes.csv"
myfile = "phonemes.csv"

# ----------------------------------------------------------------------------


def read_file(filename):
    """ Load the content of a file with utf-8 encoding.

    :param filename: (str) Name of the file to read, including path.
    :returns: List of strings

    """
    my_list = list()
    with codecs.open(filename, 'r', encoding="utf8") as fp:
        # strip each line
        for l in fp.readlines():
            my_list.append(l.strip())

    return my_list

# ----------------------------------------------------------------------------


if __name__ == '__main__':

    lines = read_file(myfile)

    # before doing something, check the data!
    if len(lines) == 0:
        print('Hum... the file was empty!')
        sys.exit(0)

    # print the lines
    for line in lines:
        print(line)

    # do something with the lines
    vowels = list()
    for line in lines:
        columns = line.split(';')
        if columns[0].strip() == "vowels":
            vowels.append(columns[1].strip())

    # then do something on the list of vowels...
    print("There are {:d} vowels.".format(len(vowels)))
