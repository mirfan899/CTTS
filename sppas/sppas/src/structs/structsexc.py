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

    structs.structsexc.py
    ~~~~~~~~~~~~~~~~~~~~~~

"""

from sppas.src.config import error

# -----------------------------------------------------------------------


class MetaKeyError(KeyError):
    """:ERROR 6010:.

    {meta} is not a known meta information.

    """

    def __init__(self, key):
        self.parameter = error(6010) + \
                         (error(6010, "structs")).format(meta=key)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class LangTypeError(TypeError):
    """:ERROR 6020:.

    Unknown resource type: expected file or directory.
    Got: {string}.

    """

    def __init__(self, lang_type):
        self.parameter = error(6020) + \
                         (error(6020, "structs")).format(string=lang_type)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class LangPathError(TypeError):
    """:ERROR 6024:.

    The resource folder {dirname} does not exists.

    """

    def __init__(self, folder):
        self.parameter = error(6024) + \
                         (error(6024, "structs")).format(dirname=folder)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class LangNameError(ValueError):
    """:ERROR 6028:.

    The language must be "und" or one of the language list.
    Unknown language {lang}.

    """

    def __init__(self, lang):
        self.parameter = error(6028) + \
                         (error(6028, "structs")).format(lang=lang)

    def __str__(self):
        return repr(self.parameter)
