# -*- coding:utf-8 -*-
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

    src.files.tests.test_filedatafilters.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import unittest
import os

import sppas
from sppas import u
from ..filedata import FileData
from ..filedatacompare import *
from ..filedatafilters import sppasFileDataFilters


class TestsFileDataFilter (unittest.TestCase):

    def setUp(self):
        f1 = os.path.join(sppas.paths.samples, 'samples-fra', 'AC track_0379.PitchTier')
        f2 = os.path.join(sppas.paths.samples, 'samples-jpn', 'JPA_M16_JPA_T02.TextGrid')
        f3 = os.path.join(sppas.paths.samples, 'samples-cat', 'TB-FE1-H1_phrase1.TextGrid')

        self.files = FileData()
        self.files.add_file(__file__)
        self.files.add_file(f1)
        self.files.add_file(f2)
        self.files.add_file(f3)

        spk1 = FileReference('spk1')
        spk1.set_type('SPEAKER')
        spk1.append(sppasAttribute('age', '20', "int"))
        spk1.append(sppasAttribute('name', 'toto'))

        ref2 = FileReference('record')
        ref2.append(sppasAttribute('age', '50', "int"))
        ref2.append(sppasAttribute('name', 'toto'))

        fr1 = self.files.get_object(FileRoot.root(f1))
        fr1.add_ref(spk1)

        fr2 = self.files.get_object(FileRoot.root(f3))
        fr2.add_ref(ref2)

        self.data_filter = sppasFileDataFilters(self.files)

    def test_path(self):
        self.assertEqual(3, len(self.data_filter.path(contains=u('samples-'))))

    def test_root(self):
        self.assertEqual(4, len(self.data_filter.root(contains=u('_'))))

    def test_filename(self):
        self.assertEqual(1, len(self.data_filter.name(iexact=u('jpa_m16_jpa_t02'))))

    def test_filename_extension(self):
        self.assertEqual(3, len(self.data_filter.extension(not_exact=u('.PY'))))

    def test_filename_state(self):
        self.assertEqual(4, len(self.data_filter.file(state=States().UNUSED)))

    def test_ref_id(self):
        self.assertEqual(1, len(self.data_filter.ref(startswith=u('rec'))))
        self.assertEqual(0, len(self.data_filter.ref(startswith=u('aa'))))

    def test_att(self):
        self.assertEqual(1, len(self.data_filter.att(iequal=('age', '20'))))
        self.assertEqual(1, len(self.data_filter.att(gt=('age', '30'))))
        self.assertEqual(2, len(self.data_filter.att(le=('age', '60'))))
        self.assertEqual(2, len(self.data_filter.att(exact=('name', 'toto'))))
        self.assertEqual(2, len(self.data_filter.att(exact=('name', 'toto'), lt=('age', '60'), logic_bool="and")))
        self.assertEqual(1, len(self.data_filter.att(exact=('name', 'toto'), equal=('age', '20'), logic_bool="and")))
        self.assertEqual(2, len(self.data_filter.att(exact=('name', 'toto'), equal=('age', '20'), logic_bool="or")))

    def test_mixed_filter_sets_way(self):
        self.assertEqual(1, len(self.data_filter.extension(not_exact=u('.PY')) &
                                self.data_filter.name(iexact=u('jpa_m16_jpa_t02'))))

    def test_mixed_filter_argument_way(self):
        self.assertEqual(2, len(self.data_filter.extension(not_exact=u('.PY'), startswith=u('.TEXT'), logic_bool='and')))
