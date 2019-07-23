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

    anndata.ann.annlabel.tagcompare.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import re

from sppas.src.utils.makeunicode import text_type
from sppas.src.utils.datatype import sppasType
from sppas.src.structs.basecompare import sppasBaseCompare

from ...anndataexc import AnnDataTypeError

from .tag import sppasTag

# ---------------------------------------------------------------------------


class sppasTagCompare(sppasBaseCompare):
    """Comparison methods for sppasTag.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    Label'tags can be of 3 types in anndata (str, num, bool) so
    that this class allows to create different comparison methods
    depending on the type of the tags.

    :Example: Three different ways to compare a tag content to a given string

        >>> tc = sppasTagCompare()
        >>> tc.exact(sppasTag("abc"), u("abc"))
        >>> tc.methods['exact'](sppasTag("abc"), u("abc"))
        >>> tc.get('exact')(sppasTag("abc"), u("abc"))

    """

    def __init__(self):
        """Create a sppasTagCompare instance."""
        super(sppasTagCompare, self).__init__()

        # Methods on strings
        self.methods['exact'] = sppasTagCompare.exact
        self.methods['iexact'] = sppasTagCompare.iexact
        self.methods['startswith'] = sppasTagCompare.startswith
        self.methods['istartswith'] = sppasTagCompare.istartswith
        self.methods['endswith'] = sppasTagCompare.endswith
        self.methods['iendswith'] = sppasTagCompare.iendswith
        self.methods['contains'] = sppasTagCompare.contains
        self.methods['icontains'] = sppasTagCompare.icontains
        self.methods['regexp'] = sppasTagCompare.regexp

        # Methods on numerical values
        self.methods['greater'] = sppasTagCompare.greater
        self.methods['lower'] = sppasTagCompare.lower
        self.methods['equal'] = sppasTagCompare.equal

        # Methods on boolean values
        self.methods['bool'] = sppasTagCompare.bool

    # -----------------------------------------------------------------------
    # Methods for unicode string tags
    # -----------------------------------------------------------------------

    @staticmethod
    def exact(tag, text):
        """Test if two texts strictly contain the same characters.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content() == text

    # -----------------------------------------------------------------------

    @staticmethod
    def iexact(tag, text):
        """Case-insensitive exact.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content().lower() == text.lower()

    # -----------------------------------------------------------------------

    @staticmethod
    def startswith(tag, text):
        """Test if first text starts with the characters of the second text.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content().startswith(text)

    # -----------------------------------------------------------------------

    @staticmethod
    def istartswith(tag, text):
        """Case-insensitive startswith.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content().lower().startswith(text.lower())

    # -----------------------------------------------------------------------

    @staticmethod
    def endswith(tag, text):
        """Test if first text ends with the characters of the second text.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content().endswith(text)

    # -----------------------------------------------------------------------

    @staticmethod
    def iendswith(tag, text):
        """Case-insensitive endswith.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return tag.get_content().lower().endswith(text.lower())

    # -----------------------------------------------------------------------

    @staticmethod
    def contains(tag, text):
        """Test if the first text contains the second text.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return text in tag.get_content()

    # -----------------------------------------------------------------------

    @staticmethod
    def icontains(tag, text):
        """Case-insensitive contains.

        :param tag: (sppasTag) Tag to compare.
        :param text: (unicode) Unicode string to be compared with.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if not isinstance(text, text_type):
            raise AnnDataTypeError(text, text_type)

        return text.lower() in tag.get_content().lower()

    # -----------------------------------------------------------------------

    @staticmethod
    def regexp(tag, pattern):
        """test if text matches pattern.

        :param tag: (sppasTag) Tag to compare.
        :param pattern: (unicode) Pattern to search.
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        text = tag.get_content()

        return True if re.match(pattern, text) else False

    # -----------------------------------------------------------------------
    # Methods for numerical tags
    # -----------------------------------------------------------------------

    @staticmethod
    def equal(tag, x):
        """Return True if numerical value of the tag is equal to x.

        :param tag: (sppasTag) Tag to compare.
        :param x: (int, float)
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if tag.get_type() not in ["int", "float"]:
            raise AnnDataTypeError(tag, "int/float")
        if sppasType().is_number(x) is False:
            raise AnnDataTypeError(x, "int/float")

        return tag.get_typed_content() == x

    # -----------------------------------------------------------------------

    @staticmethod
    def greater(tag, x):
        """Return True if numerical value of the tag is greater than x.

        :param tag: (sppasTag) Tag to compare.
        :param x: (int, float)
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if tag.get_type() not in ["int", "float"]:
            raise AnnDataTypeError(tag, "int/float")
        if sppasType().is_number(x) is False:
            raise AnnDataTypeError(x, "int/float")

        return tag.get_typed_content() > x

    # -----------------------------------------------------------------------

    @staticmethod
    def lower(tag, x):
        """Return True if numerical value of the tag is lower than x.

        :param tag: (sppasTag) Tag to compare.
        :param x: (int, float)
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if tag.get_type() not in ["int", "float"]:
            raise AnnDataTypeError(tag, "int/float")
        if sppasType().is_number(x) is False:
            raise AnnDataTypeError(x, "int/float")

        return tag.get_typed_content() < x

    # -----------------------------------------------------------------------
    # Methods for boolean tags
    # -----------------------------------------------------------------------

    @staticmethod
    def bool(tag, x):
        """Return True if boolean value of the tag is equal to boolean x.

        :param tag: (sppasTag) Tag to compare.
        :param x: (bool)
        :returns: (bool)
        :raises: AnnDataTypeError

        """
        if isinstance(tag, sppasTag) is False:
            raise AnnDataTypeError(tag, "sppasTag")
        if tag.get_type() != "bool":
            raise AnnDataTypeError(tag, "bool")
        if sppasType().is_bool(x) is False:
            raise AnnDataTypeError(x, "bool")

        return tag.get_typed_content() == x
