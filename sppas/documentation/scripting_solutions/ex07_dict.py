#!/usr/bin python
"""

:author:       Fix Me
:date:         Now
:contact:      me@me.org
:license:      GPL, v3
:copyright:    Copyright (C) 2017  Fixme

:summary:      Simple script to manipulate dictionaries: SAMPA to IPA converter.

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
from ex05_reading_file import read_file

# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

#my_file="C:\phonemes.csv"
my_file = "phonemes.csv"

# ----------------------------------------------------------------------------


def extract_dict_from_lines(lines, col_key, col_value):
    """ Extract a dictionary from the columns of a list of lines.

    :param lines: (list)
    :param col_key: (str)
    :param col_value: (str)

    """
    # Check if everything is normal:
    my_dict = dict()
    if col_key < 0 or col_value < 0:
        print("Error. Bad column number.")
        return my_dict

    for line in lines:
        # Get columns in a list
        columns = line.split(';')
        # Check if the given column values are normal!
        if len(columns) > col_key and len(columns) > col_value:
            the_key = columns[col_key].strip()
            the_value = columns[col_value].strip()
            # Add the new pair in the dict. If the key is already
            # existing, it will be updated with the new value!
            my_dict[the_key] = the_value
        else:
            print("Warning. Bad number of columns for line: {0}".format(line))

    return my_dict

# ----------------------------------------------------------------------------

if __name__ == '__main__':

    lines = read_file(my_file)

    # before doing something, check the data!
    if not len(lines):
        print('Hum... the file was empty!')
        sys.exit(0)

    sampa_dict = extract_dict_from_lines(lines, 1, 2)
    my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'E', 'g', 'a~', 'S']
    for phone in my_list:
        if phone in sampa_dict:
            print("Sampa phoneme {:s} is IPA {:s}.".format(phone, sampa_dict[phone]))
        else:
            print("Sampa phoneme {:s} has no IPA!".format(phone))
