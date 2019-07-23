#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              Automatic
#           \__   |__/  |__/  |___| \__             Annotation
#              \  |     |     |   |    \             of
#           ___/  |     |     |   | ___/              Speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2016  Brigitte Bigi
#
#                   This banner notice must not be removed
# ---------------------------------------------------------------------------
# Use of this software is governed by the GNU Public License, version 3.
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: files.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

import os

# ---------------------------------------------------------------------------


class xFiles(object):
    """
    Information about a list of files: the file name and an object.
    TODO: Change the data structure... use dictionaries or a list of tuples.
    """

    def __init__(self):
        """
        Create a new instance, with empty lists.
        """
        self._name  = []
        self._obj   = []
        self._other = []

    # End __init__
    # ------------------------------------------------------------------------


    def GetIndex(self, filename):
        """
        Return the index of the first occurrence of a given filename, or -1.
        """
        if filename in self._name:
            return self._name.index(filename)
        return -1

    # End GetIndex
    # ------------------------------------------------------------------------


    def GetFilename(self, index):
        """
        Return the filename (including path), or an empty string.
        """
        if len(self._name) > index:
            return self._name[index]
        return ""

    # End GetFilename
    # ------------------------------------------------------------------------


    def GetBasename(self, index):
        """
        Return the basename of filename (ie not including path), or an empty string.
        """
        if len(self._name) > index:
            return os.path.basename(self._name[index])
        return ""

    # End GetBasename
    # ------------------------------------------------------------------------


    def GetObject(self, index):
        """
        Return the object, or None.
        """
        if len(self._obj) > index:
            return self._obj[index]
        return None

    # End GetObject
    # ------------------------------------------------------------------------


    def GetOther(self, index):
        """
        Return the object, or None.
        """
        if len(self._other) > index:
            return self._other[index]
        return None

    # End GetOther
    # ------------------------------------------------------------------------


    def GetSize(self):
        """
        Return the number of items in xFiles.
        """
        return len(self._name)

    # End GetSize
    # ------------------------------------------------------------------------


    def Exists(self, filename):
        """
        Return True if filename is in self.
        """
        return filename in self._name

    # End Exists
    # ------------------------------------------------------------------------


    def Append(self, filename, obj, other=-1):
        """
        Append a new item in self.
        """
        self._name.append(filename)
        self._obj.append(obj)
        self._other.append(other)

    # End Append
    # ------------------------------------------------------------------------


    def SetFilename(self, i, filename):
        """
        Rename.
        """
        if filename in self._name:
            raise Exception('SetFilename. error. name existing.')
        self._name[i] = filename

    # End SetFilename
    # ------------------------------------------------------------------------


    def Pop(self):
        """
        Remove the last item.
        """
        self._name.pop()
        self._obj.pop()
        self._other.pop()

    # End Pop
    # ------------------------------------------------------------------------


    def Remove(self, index):
        """
        Remove an item in self.
        """
        if len(self._name) > index:
            self._name.pop(index)
            self._obj.pop(index)
            self._other.pop(index)

    # End Remove
    # ------------------------------------------------------------------------


    def RemoveAll(self):
        """
        Remove all items in self.
        """
        del self._name[:]
        del self._obj[:]
        del self._other[:]

    # End RemoveAll
    # ------------------------------------------------------------------------
