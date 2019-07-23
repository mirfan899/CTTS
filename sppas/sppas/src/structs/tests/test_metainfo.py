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

    src.structs.tests.test_metainfo.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest

from sppas.src.utils.makeunicode import u

from ..metainfo import sppasMetaInfo
from ..structsexc import MetaKeyError

# ---------------------------------------------------------------------------


class TestMetaInfo(unittest.TestCase):

    def test_init(self):
        meta = sppasMetaInfo()
        self.assertEqual(len(meta), 0)

    def test_add_get(self):
        meta = sppasMetaInfo()
        meta.add_metainfo('author', 'moi')
        self.assertEqual(len(meta), 1)
        self.assertEqual(meta.get_metainfo('author'), 'moi')

        # add a "complex" meta info
        meta.add_metainfo('author', ('moi', 'toi'))
        self.assertEqual(meta.get_metainfo('author'), ('moi', 'toi'))

    def test_enable(self):
        meta = sppasMetaInfo()
        meta.add_metainfo('author', 'moi')
        self.assertTrue(meta.is_enable_metainfo('author'))
        self.assertEqual(len(meta.keys_enabled()), 1)

        # disable
        meta.enable_metainfo('author', False)
        self.assertFalse(meta.is_enable_metainfo('author'))
        self.assertEqual(len(meta.keys_enabled()), 0)
        # enable
        meta.enable_metainfo('author', True)
        self.assertEqual(len(meta.keys_enabled()), 1)
        self.assertTrue(meta.is_enable_metainfo('author'))

    def test_raises(self):
        meta = sppasMetaInfo()
        meta.add_metainfo('author', 'moi')

        with self.assertRaises(MetaKeyError):
            meta.pop_metainfo('toto')
        with self.assertRaises(MetaKeyError):
            meta.enable_metainfo('toto')
        with self.assertRaises(MetaKeyError):
            meta.get_metainfo('toto')
        with self.assertRaises(MetaKeyError):
            meta.is_enable_metainfo('toto')

    def test_pop(self):
        meta = sppasMetaInfo()
        meta.add_metainfo('author', 'moi')
        meta.pop_metainfo('author')
        self.assertEqual(len(meta), 0)

    def test_unicode(self):
        meta = sppasMetaInfo()
        meta.add_metainfo('éè', 'moi')
        self.assertEqual(len(meta.keys_enabled()), 1)
        self.assertTrue(u("éè") in meta.keys_enabled())
        self.assertEqual(meta.get_metainfo('éè'), 'moi')
        self.assertEqual(meta.get_metainfo(u('éè')), 'moi')
