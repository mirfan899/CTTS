#!/usr/bin python
"""

:author:       Fix Me
:date:         Now
:contact:      me@me.org
:license:      GPL, v3
:copyright:    Copyright (C) 2017  Fixme

:summary:      Simple script to print lists.

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


def is_empty(string):
    """ Return True if the given string contains no characters.
    
    :param string: (str) a string to check
    :returns: bool
    
    """
    # Clean the string: remove tabs, carriage returns...
    s = string.strip()

    # Check the length of the cleaned string
    return len(s) == 0

# ---------------------------------------------------------------------------


def print_list(my_list, message="  -"):
    """ Print a list on the screen.

    :param my_list: (list) the list to print
    :param message: (str) an optional message to print before each item

    """
    str_message = str(message)

    for item in my_list:

        str_item = str(item)
        if is_empty(str_item) is False:
            print("{:s} {:s}".format(str_message, str_item))
        else:
            print("{:s} Empty item.".format(str_message))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    vowels = ['a', 'e', 'E', 'i', 'o', 'u', 'y', '@', '2', '9', 'a~', 'o~', 'U~']
    plosives = ['p', 't', 'k', 'b', 'd', 'g']
    numbers = [1, 2, "", 3, "4"]

    print_list(vowels,   "Vowel:   ")
    print_list(plosives, "Plosive: ")
    print_list(numbers,  "Number:  ")
