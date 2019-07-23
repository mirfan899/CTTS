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

    config.po.py
    ~~~~~~~~~~~

"""
import sys
import gettext
import locale

from .sglobal import sppasPathSettings
from .sglobal import sppasGlobalSettings

# ---------------------------------------------------------------------------


class T:
    """Utility class to simulate the GNUTranslations class.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    @staticmethod
    def gettext(msg):
        """Return msg in unicode."""
        if sys.version_info >= (3, 0):
            return msg
        else:
            with sppasGlobalSettings() as sg:
                return msg.decode(sg.__encoding__)

    @staticmethod
    def ugettext(msg):
        """Return msg."""
        if sys.version_info >= (3, 0):
            return msg
        else:
            with sppasGlobalSettings() as sg:
                return msg.decode(sg.__encoding__)

# ---------------------------------------------------------------------------


class sppasTranslate(object):
    """Fix the domain to translate messages and to activate the gettext method.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    sppasTranslate is useful for the internationalization of texts for both
    Python 2 and Python 3.

    The locale is used to set the language and English is the default.
    The path to search a domain translation is the one of SPPAS (po folder).

    >>> _ = sppasTranslate().translation("domain").gettext
    >>> my_string = _("Some string in the domain.")

    """

    def __init__(self):
        """Create a sppasTranslate instance: fix language."""
        self.lang = sppasTranslate.get_lang_list()

    # -----------------------------------------------------------------------

    @staticmethod
    def get_lang_list():
        """Return the list of languages depending on the default locale.

        At a first stage, the language is fixed with the default locale.
        English is then either appended to the list or used by default.

        """
        try:
            lc, encoding = locale.getdefaultlocale()
            if lc is not None:
                return [lc, "en_US"]
        except:
            pass

        return ["en_US"]

    # -----------------------------------------------------------------------

    def translation(self, domain):
        """Create the GNUTranslations for a given domain.

        :param domain: (str) Name of the domain.
        A domain corresponds to a ".po" file of the language in the 'po' folder
        of the SPPAS package.
        :returns: (GNUTranslations)

        """
        try:
            # Install translation for the local language + English
            with sppasPathSettings() as path:
                t = gettext.translation(domain, path.po, self.lang)
                t.install()
                return t

        except:
            try:
                # Install translation for English only
                with sppasPathSettings() as path:
                    t = gettext.translation(domain, path.po, ["en_US"])
                    t.install()
                    return t

            except IOError:
                pass

        # No language installed. The messages won't be translated;
        # at least they are simply returned.
        return T()
