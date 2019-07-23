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

    src.annotations.TextNorm.num2letter.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Module to convert numbers to their written form the multilingual text
    normalization system.
    Num2Letter conversion is language-specific.

"""

from sppas.src.utils.makeunicode import u

# -------------------------------------------------------------------------


class sppasNum(object):
    """Numerical conversion using a multilingual algorithm.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    The language names used in this class are based on iso639-3.

    >>> num = sppasNum('fra')
    >>> num.convert("3")
    trois
    >>> num.convert("03")
    >>>zéro-trois
    >>> sppasNum('3.0')
    ValueError

    IMPORTANT:
    ==========

    Notice that this class should be fully re-implemented.
    It should use an external resource file to make the match
    between numbers and letters, for each language:
        0 zéro
        1 un
        ...
        10 dix
        100 cent
        1000 mille
        1000000 million
        1000000000 milliard

    """
    LANGUAGES = ["und", "yue", "cmn", "fra", "ita", "eng", "spa", "khm",
                 "vie", "jpn", "pol", "por", "pcm"]

    ZERO = dict()
    ZERO["und"] = u("0")
    ZERO["yue"] = u("零")
    ZERO["cmn"] = u("零")
    ZERO["fra"] = u("zéro")
    ZERO["ita"] = u("zero")
    ZERO["eng"] = u("zero")
    ZERO["spa"] = u("cero")
    ZERO["khm"] = u("ស្សូន  ")
    ZERO["vie"] = u("không")
    ZERO["jpn"] = u("ゼロ")
    ZERO['pol'] = u("zerowej")
    ZERO['por'] = u("zero")

    def __init__(self, lang="und"):
        """Create a new sppasNum instance.

        :param lang: (str) the language code in ISO639-3 (fra, eng, spa,
        khm, ita, ...). If lang is set to "und" (undetermined), no conversion
        is performed.

        """
        self._lang = "und"
        self.set_lang(lang)

    # -------------------------------------------------------------------------

    def set_lang(self, lang):
        """Set the language.

        :param lang: (str) the language code in ISO639-3.

        """
        if lang == "pcm":
            lang = "eng"
        self._lang = lang

    # -------------------------------------------------------------------------

    def get_lang(self):
        """Return the current language code."""

        return self._lang

    # -------------------------------------------------------------------------
    # Number 0
    # -------------------------------------------------------------------------

    def zero(self):
        """Convert the zero number.

        :param number: (int) the number to convert to letters.

        """
        return sppasNum.ZERO[self._lang]

    # -------------------------------------------------------------------------
    # Numbers from 1 to 9
    # -------------------------------------------------------------------------

    def __unite_khm(self, number):
        _r = ""
        if number == 9:
            _r = u("ប្រាំបួន ")
        if number == 8:
            _r = u("ប្រាំបី ")
        if number == 7:
            _r = u("ប្រាំពីរ ")
        if number == 6:
            _r = u("ប្រាំមួយ ")
        if number == 5:
            _r = u("ប្រាំ ")
        if number == 4:
            _r = u("បួន ")
        if number == 3:
            _r = u("បី ")
        if number == 2:
            _r = u("ពីរ ")
        if number == 1:
            _r = u("មួយ ")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_por(self, number):
        _r = ""
        if number == 9:
            _r = u("nove")
        if number == 8:
            _r = u("oito")
        if number == 7:
            _r = u("sete")
        if number == 6:
            _r = u("seis")
        if number == 5:
            _r = u("cinco")
        if number == 4:
            _r = u("quatro")
        if number == 3:
            _r = u("três")
        if number == 2:
            _r = u("dois")
        if number == 1:
            _r = u("um")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_spa(self, number):
        _r = ""
        if number == 9:
            _r = u("nueve")
        if number == 8:
            _r = u("ocho")
        if number == 7:
            _r = u("siete")
        if number == 6:
            _r = u("seis")
        if number == 5:
            _r = u("cinco")
        if number == 4:
            _r = u("cuatro")
        if number == 3:
            _r = u("tres")
        if number == 2:
            _r = u("dos")
        if number == 1:
            _r = u("uno")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_vie(self, number):
        _r = ""
        if number == 9:
            _r = u("chín")
        if number == 8:
            _r = u("tám")
        if number == 7:
            _r = u("bảy")
        if number == 6:
            _r = u("sáu")
        if number == 5:
            _r = u("năm")
        if number == 4:
            _r = u("bốn")
        if number == 3:
            _r = u("ba")
        if number == 2:
            _r = u("hai")
        if number == 1:
            _r = u("một")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_cmn(self, number):
        _r = ""
        if number == 9:
            _r = u("九")
        if number == 8:
            _r = u("八")
        if number == 7:
            _r = u("七")
        if number == 6:
            _r = u("六")
        if number == 5:
            _r = u("五")
        if number == 4:
            _r = u("四")
        if number == 3:
            _r = u("三")
        if number == 2:
            _r = u("二")
        if number == 1:
            _r = u("一")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_fra(self, number):
        _r = ""
        if number == 9:
            _r = u("neuf")
        if number == 8:
            _r = u("huit")
        if number == 7:
            _r = u("sept")
        if number == 6:
            _r = u("six")
        if number == 5:
            _r = u("cinq")
        if number == 4:
            _r = u("quatre")
        if number == 3:
            _r = u("trois")
        if number == 2:
            _r = u("deux")
        if number == 1:
            _r = u("un")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_ita(self, number):
        _r = ""
        if number == 9:
            _r = u("nove")
        if number == 8:
            _r = u("otto")
        if number == 7:
            _r = u("sette")
        if number == 6:
            _r = u("sei")
        if number == 5:
            _r = u("cinque")
        if number == 4:
            _r = u("quattro")
        if number == 3:
            _r = u("tré")
        if number == 2:
            _r = u("due")
        if number == 1:
            _r = u("uno")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_eng(self, number):
        _r = ""
        if number == 9:
            _r = u("nine")
        if number == 8:
            _r = u("eight")
        if number == 7:
            _r = u("seven")
        if number == 6:
            _r = u("six")
        if number == 5:
            _r = u("five")
        if number == 4:
            _r = u("four")
        if number == 3:
            _r = u("three")
        if number == 2:
            _r = u("two")
        if number == 1:
            _r = u("one")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def __unite_pol(self, number):
        _r = ""
        if number == 9:
            _r = u("września")
        if number == 8:
            _r = u("osiem")
        if number == 7:
            _r = u("siedem")
        if number == 6:
            _r = u("sześć")
        if number == 5:
            _r = u("pięć")
        if number == 4:
            _r = u("cztery")
        if number == 3:
            _r = u("trzy")
        if number == 2:
            _r = u("dwa")
        if number == 1:
            _r = u("stycznia")
        if number == 0:
            _r = self.zero()
        return _r

    # -------------------------------------------------------------------------

    def unite(self, number):
        """Convert a number from 0 to 9.

        :param number: (int) the number to convert to letters.

        """
        if self._lang == "khm":
            return self.__unite_khm(number)
        if self._lang == "spa":
            return self.__unite_spa(number)
        if self._lang == "vie":
            return self.__unite_vie(number)
        if self._lang in ["cmn", "yue", "jpn"]:
            return self.__unite_cmn(number)
        if self._lang == "fra":
            return self.__unite_fra(number)
        if self._lang == "ita":
            return self.__unite_ita(number)
        if self._lang == "eng":
            return self.__unite_eng(number)
        if self._lang == "pol":
            return self.__unite_pol(number)
        if self._lang == "por":
            return self.__unite_por(number)
        if self._lang == "und":
            return str(number)

        raise ValueError("Unknown language {:s} to convert numbers"
                         "".format(self._lang))

    # -------------------------------------------------------------------------
    # Numbers from 10 to 99
    # -------------------------------------------------------------------------

    def __dizaine_pol(self, number):
        if number < 10:
            return self.unite(number)
        if number < 22:
            if number == 10:
                _r = u("dziesięć")
            elif number == 11:
                _r = u("jedenaście")
            elif number == 12:
                _r = u("dwanaście")
            elif number == 13:
                _r = u("trzynaście")
            elif number == 14:
                _r = u("czternaście")
            elif number == 15:
                _r = u("piętnaście")
            elif number == 16:
                _r = u("szesnaście")
            elif number == 17:
                _r = u("siedemnaście")
            elif number == 18:
                _r = u("osiemnaście")
            elif number == 19:
                _r = u("dziewiętnaście")
            elif number == 20:
                _r = u("dwadzieścia")
            elif number == 21:
                _r = u("dwadzieścia jeden")
            return _r

        n = (number / 10) * 10
        r = number % 10
        if number < 50:
            dizaine = u("dzieścia")
        else:
            dizaine = u("dziesiąt")
        if r == 0:
            return u("%s%s") % (self.unite(n/10), dizaine)
        return u("%s%s-%s") % (self.unite(n/10), dizaine, self.unite(r))

    # -------------------------------------------------------------------------

    def __dizaine_por(self, number):
        if number < 10:
            return self.unite(number)
        if number < 20:
            if number == 10:
                return u("dez")
            elif number == 11:
                return u("onze")
            elif number == 12:
                return u("doze")
            elif number == 13:
                return u("treze")
            elif number == 14:
                return u("quatorze")
            elif number == 15:
                return u("quinze")
            elif number == 16:
                return u("dezesseis")
            elif number == 17:
                return u("dezessete")
            elif number == 18:
                return u("dezoito")
            elif number == 19:
                return u("dezenove")
        n = (number / 10) * 10
        r = number % 10
        if 19 < n < 30:
            dizaine = u("vinte")
        elif 29 < n < 40:
            dizaine = u("trinta")
        elif 39 < n < 50:
            dizaine = u("quarenta")
        elif 49 < n < 60:
            dizaine = u("cinquenta")
        elif 59 < n < 70:
            dizaine = u("sessenta")
        elif 69 < n < 80:
            dizaine = u("setenta")
        elif 79 < n < 90:
            dizaine = u("oitenta")
        elif 89 < n < 100:
            dizaine = u("noventa")
        if r == 0: return dizaine
        return u("%s-e-%s") % (dizaine, self.unite(r))

    # -------------------------------------------------------------------------

    def __dizaine_spa(self, number):
        if number < 10:
            return self.unite(number)
        if number == 10:
            return u("diez")
        if number == 11:
            return u("once")
        if number == 12:
            return u("doce")
        if number == 13:
            return u("trece")
        if number == 14:
            return u("catorce")
        if number == 15:
            return u("quince")
        if number == 16:
            return u("dieciséis")
        if number == 17:
            return u("diecisiete")
        if number == 18:
            return u("dieciocho")
        if number == 19:
            return u("diecinueve")
        if number == 20:
            return u("veinte")
        if number == 21:
            return u("veintiuno")
        if number == 22:
            return u("veintidós")
        if number == 23:
            return u("veintitrés")
        if number == 24:
            return u("veinticuatro")
        if number == 25:
            return u("veinticinco")
        if number == 26:
            return u("veintiséis")
        if number == 27:
            return u("veintisiete")
        if number == 28:
            return u("veintiocho")
        if number == 29:
            return u("veintinueve")

        n = (number / 10) * 10
        r = number % 10
        if 29 < n < 40:    
            dizaine = u("treinta")
        elif 39 < n < 50:  
            dizaine = u("cuarenta")
        elif 49 < n < 60:  
            dizaine = u("cincuenta")
        elif 59 < n < 70:  
            dizaine = u("sesenta")
        elif 69 < n < 80:  
            dizaine = u("setenta")
        elif 79 < n < 90:  
            dizaine = u("ochenta")
        elif 89 < n < 100:
            dizaine = u("noventa")
        if r == 0: return dizaine
        return u("%s-y-%s") % (dizaine, self.unite(r))

    # -------------------------------------------------------------------------

    def __dizaine_cmn(self, number):
        if number < 10:
            _str = self.unite(number)
        elif 10 <= number < 100:
            if (number % 10) == 0:
                _str = self.unite(int(number/10)) + u("十")
            else:
                _str = self.unite(int(number/10)) + u("十") + self.unite(number%10)
        return _str

    # -------------------------------------------------------------------------

    def __dizaine_fra(self, number):
        if 90 <= number <= 99:
            _str = u("quatre-vingt-") + self.dizaine(number-80)
        elif 80 <= number <= 89:
            _str = u("quatre-vingt ")
            if number > 80:
                _str = u("quatre-vingt-") + self.unite(number-80)
        elif 70 <= number <= 79:
            _str = u("soixante-") + self.dizaine(number-60)
        elif 60 <= number <= 69:
            _str = u("soixante ")
            if number == 61:
                _str = u("soixante-et-un ")
            if number > 61:
                _str = u("soixante-") + self.unite(number-60)
        elif 50 <= number <= 59:
            _str = u("cinquante ")
            if number == 51:
                _str = u("cinquante-et-un ")
            if number > 51:
                _str = u("cinquante-") + self.unite(number-50)
        elif 40 <= number <= 49:
            _str = u("quarante ")
            if number == 41:
                _str = u("quarante-et-un ")
            if number > 41:
                _str = u("quarante-") + self.unite(number-40)
        elif 30 <= number <= 39:
            _str = u("trente ")
            if number == 31:
                _str = u("trente-et-un ")
            if number > 31:
                _str = u("trente-") + self.unite(number-30)
        elif 20 <= number <= 29:
            _str = u("vingt ")
            if number == 21:
                _str = u("vingt-et-un ")
            if number > 21:
                _str = u("vingt-") + self.unite(number-20)
        elif 10 <= number <= 19:
            if number == 10: 
                _r = u("dix")
            if number == 11: 
                _r = u("onze")
            if number == 12: 
                _r = u("douze")
            if number == 13: 
                _r = u("treize")
            if number == 14:
                _r = u("quatorze")
            if number == 15:
                _r = u("quinze")
            if number == 16:
                _r = u("seize")
            if number == 17: 
                _r = u("dix-sept")
            if number == 18: 
                _r = u("dix-huit")
            if number == 19:
                _r = u("dix-neuf")
            return _r
        else:
            _str = self.unite(number)
        return _str

    # -------------------------------------------------------------------------

    def __dizaine_eng(self, number):
        if 90 < number <= 99:
            _str = u("ninety-") + self.dizaine(number-90)
        elif number == 90:
            _str = u("ninety")
        elif 80 < number <= 89:
            _str = u("eighty-") + self.dizaine(number-80)
        elif number == 80:
            _str = u("eighty")
        elif 70 < number <= 79:
            _str = u("seventy-") + self.dizaine(number-70)
        elif number == 70:
            _str = u("seventy")
        elif 60 < number <= 69:
            _str = u("sixty-") + self.unite(number-60)
        elif number == 60:
            _str = u("sixty ")
        elif 50 < number <= 59:
            _str = u("fifty-") + self.unite(number-50)
        elif number == 50:
            _str = u("fifty")
        elif 40 < number <= 49:
            _str = u("fourty-") + self.unite(number-40)
        elif number == 40:
            _str = u("fourty")
        elif 30 < number <= 39:
            _str = u("thirty-") + self.unite(number-30)
        elif number == 30:
            _str = u("thirty")
        elif 20 < number <= 29:
            _str = u("twenty-") + self.unite(number-20)
        elif number == 20:
            _str = u("twenty ")
        elif 10 <= number <= 19:
            if number == 10: 
                _r = u("ten")
            if number == 11:
                _r = u("eleven")
            if number == 12: 
                _r = u("twelve")
            if number == 13: 
                _r = u("thirteen")
            if number == 14: 
                _r = u("fourteen")
            if number == 15: 
                _r = u("fifteen")
            if number == 16: 
                _r = u("sixteen")
            if number == 17: 
                _r = u("seventeen")
            if number == 18: 
                _r = u("eigteen")
            if number == 19: 
                _r = u("nineteen")
            return _r
        else:
            _str = self.unite(number)
        return _str
    
    # -------------------------------------------------------------------------

    def __dizaine_ita(self,number):
        if number == 91 or number == 98:
            _str = u("novant") + self.dizaine(number-90).strip() + " "
        elif 90 < number <= 99:
            _str = u("novanti-") + self.dizaine(number-90).strip() + " "
        elif number == 90:
            _str = u("novanti")
        elif number == 81 or number == 88:
            _str = u("ottant") + self.dizaine(number-80).strip() + " "
        elif 81 < number <= 89:
            _str = u("ottanta-") + self.dizaine(number-80).strip() + " "
        elif number == 80:
            _str = u("ottanta")
        elif number == 71 or number == 78:
            _str = u("settant") + self.dizaine(number-70).strip() + " "
        elif number >= 71 and number <= 79:
            _str = u("settanta-") + self.dizaine(number-70).strip() + " "
        elif number == 70:
            _str = u("settanta")
        elif number == 61 or number == 68:
            _str = u("sessant") + self.unite(number-60).strip() + " "
        elif number > 61 and number <= 69:
            _str = u("sessanta-") + self.unite(number-60).strip() + " "
        elif number == 60:
            _str = u("sessanta")
        elif number == 51 or number == 58:
            _str = u("cinquant") + self.unite(number-50).strip() + " "
        elif number > 50 and number <= 59:
            _str = u("cinquanta-") + self.unite(number-50).strip() + " "
        elif number == 50:
            _str = u("cinquanta")
        elif number == 41 or number == 48:
            _str = u("quarant") + self.unite(number-40).strip() + " "
        elif number > 41 and number <= 49:
            _str = u("quaranta-") + self.unite(number-40).strip() + " "
        elif number == 40:
            _str = u("quaranta")
        elif number == 31 or number == 38:
            _str = u("trent") + self.unite(number-30).strip() + " "
        elif number > 31 and number <= 39:
            _str = u("trenta-") + self.unite(number-30).strip() + " "
        elif number == 30:
            _str = u("trenta")
        elif number == 21 or number == 28:
            _str = u("vent") + self.unite(number-20).strip() + " "
        elif number > 21 and number <= 29:
            _str = u("venti-") + self.unite(number-20).strip() + " "
        elif number == 20:
            _str = u("venti")
        elif number >= 10 and number <= 19:
            if number == 10: _r = u("dieci")
            if number == 11: _r = u("undici")
            if number == 12: _r = u("dodici")
            if number == 13: _r = u("tredici")
            if number == 14: _r = u("quattordici")
            if number == 15: _r = u("quindici")
            if number == 16: _r = u("sedici")
            if number == 17: _r = u("diciassette")
            if number == 18: _r = u("diciotto")
            if number == 19: _r = u("diciannove")
            return _r
        else:
            _str = self.unite(number)
        return _str
    
    # -------------------------------------------------------------------------

    def dizaine(self, number):
        """Convert a number from 10 to 99.
        
        :param number: (int)
        
        """
        if self._lang == "spa":
            return self.__dizaine_spa(number)
        if "cmn" in self._lang  \
                or "yue" in self._lang  \
                or "jpn" in self._lang:
            return self.__dizaine_cmn(number)
        if self._lang == "eng":
            return self.__dizaine_eng(number)
        if self._lang == "fra":
            return self.__dizaine_fra(number)
        if self._lang == "ita":
            return self.__dizaine_ita(number)
        if self._lang == "pol":
            return self.__dizaine_pol(number)
        if self._lang == "por":
            return self.__dizaine_por(number)

        if self._lang == "und":
            return str(number)
        raise Exception('Unrecognized language: '+self._lang)

    # -------------------------------------------------------------------------
    # Numbers from 100 to 999
    # -------------------------------------------------------------------------

    def __centaine_por(self, number):
        if number < 100:
            return self.dizaine(number)
        if number == 100:
            return u("centavo")
        n = number / 100
        r = number % 100
        s = ""
        if 100 < number < 200:
            return u("centavo-%s") % self.dizaine(r)
        if 199 < number < 300:
            s = u("duzentos")
        elif 299 < number < 400:
            s = u("trezentos")
        elif 399 < number < 500:
            s = u("quatrocentos")
        elif 499 < number < 600:
            s = u("quinhentos")
        elif 599 < number < 700:
            s = u("seiscentos")
        elif 699 < number < 800:
            s = u("setecentos")
        elif 799 < number < 900:
            s = u("oitocentos")
        elif 899 < number < 1000:
            s = u("novecentos")
        if r == 0: return s
        return u("%s-e-%s") % (s, self.dizaine(r))

    # -------------------------------------------------------------------------

    def __centaine_spa(self, number):
        if number < 100:
            return self.dizaine(number)
        if number == 100:
            return u("cien")
        n = number / 100
        r = number % 100
        s = ""
        if 100 < number < 200:
            return u("ciento-%s") % self.dizaine(r)
        if 499 < number < 600:
            s = u("quinientos")
        elif 699 < number < 800:
            s = u("setecientos")
        elif 899 < number < 1000:
            s = u("novecientos")
        else:
            s = u("{:s}cientos".format(self.unite(n)))
        if r == 0:
            return s
        return u("%s-%s") % (s, self.dizaine(r))

    # -------------------------------------------------------------------------

    def __centaine_cmn(self, number):
        if number < 100:
            return self.dizaine(number)
        if number >= 100 and number < 1000:
            if (number % 100) != 0:
                if (number % 100) > 0 and (number % 100) < 10:
                    return self.dizaine(int(number/100)) + u("百零") + self.dizaine(number % 100)
                return self.dizaine(int(number/100)) + u("百") + self.dizaine(number % 100)
            else:
                return self.dizaine(int(number/100)) + u("百")
        return str(number)

    # -------------------------------------------------------------------------

    def __centaine_fra(self, number):
        if number < 100:
            return self.dizaine(number)
        if number == 100:
            return u("cent")
        if number > 100 and number <= 199:
            return u("cent-") + self.dizaine(number % 100)
        if (number%100) == 0:
            return self.unite(number % 100) + u("-cents")
        return self.unite(int(number/100)) + u("-cent-") + self.dizaine(number % 100)

    # -------------------------------------------------------------------------

    def __centaine_ita(self, number):
        if number < 100:
            return self.dizaine(number)
        if number == 100:
            return u("cento")
        if number > 100 and number <= 199:
            return u("cento-") + self.dizaine(number%100)
        if (number%100) == 0:
            return " " + self.unite(number % 100) + u("-cento")
        return " " + self.unite(int(number/100)) + u("-cento-") + self.dizaine(number % 100)

    # -------------------------------------------------------------------------

    def __centaine_eng(self, number):
        if number < 100:
            return self.dizaine(number)
        n = number / 100
        r = number % 100
        s = u("%s hundred") % self.unite(n)
        if r == 0:
            return s
        else:
            return "%s %s" % (s, self.dizaine(r))

    # -------------------------------------------------------------------------

    def __centaine_pol(self, number):
        if number < 100:
            return self.dizaine(number)

        if number == 100:
            return u("sto")
        if number > 100 and number <= 199:
            return u("sto ") + self.dizaine(number % 100)
        if number == 200:
            return u("dwieście")
        if number > 200 and number <= 299:
            return u("dwieście ") + self.dizaine(number % 100)
        if number == 300:
            return u("trzysta")
        if number > 300 and number <= 399:
            return u("trzysta ") + self.dizaine(number % 100)
        if number == 400:
            return u("czterysta")
        if number > 400 and number <= 499:
            return u("czterysta ") + self.dizaine(number % 100)
        if number == 500:
            return u("pięćset")
        if number > 500 and number <= 599:
            return u("pięćset ") + self.dizaine(number % 100)
        if number == 600:
            return u("sześćset")
        if number > 600 and number <= 699:
            return u("sześćset ") + self.dizaine(number % 100)
        if number == 700:
            return u("siedemset")
        if number > 700 and number <= 799:
            return u("siedemset ") + self.dizaine(number % 100)
        if number == 800:
            return u("osiemset")
        if number > 800 and number <= 899:
            return u("osiemset ") + self.dizaine(number % 100)
        if number == 900:
            return u("osiemset")
        if number > 900 and number <= 999:
            return u("osiemset ") + self.dizaine(number % 100)

    # -------------------------------------------------------------------------

    def centaine(self, number):
        """Convert a number from 100 to 999.

        :param number: (int)

        """
        if self._lang == "spa":
            return self.__centaine_spa(number)
        if "cmn" in self._lang  \
                or "yue" in self._lang  \
                or "jpn" in self._lang:
            return self.__centaine_cmn(number)
        if self._lang == "fra":
            return self.__centaine_fra(number)
        if self._lang == "ita":
            return self.__centaine_ita(number)
        if self._lang == "eng":
            return self.__centaine_eng(number)
        if self._lang == "pol":
            return self.__centaine_pol(number)
        if self._lang == "por":
            return self.__centaine_por(number)

        if self._lang == "und":
            return str(number)

        raise Exception('Unrecognized language: ' + self._lang)

    # -------------------------------------------------------------------------
    # Numbers from more than 999
    # -------------------------------------------------------------------------

    def __milliers_por(self, number):
        if number < 1000:
            return self.centaine(number)

        n = number / 1000
        r = number % 1000

        if number < 2000:
            s = u("mil")
        else:
            s = u("%s-milhas") % self.centaine(n)
        if r == 0:
            return s
        return u("%s-%s") % (s, self.centaine(r))

    # -----------------------------------------------------------------------

    def __milliers_spa(self, number):
        if number < 1000:
            return self.centaine(number)

        n = number / 1000
        r = number % 1000

        if number < 2000:
            s = u("mil")
        else:
            s = u("%s-mil") % self.centaine(n)
        if r == 0:
            return s
        return u("%s-%s") % (s, self.centaine(r))

    # -----------------------------------------------------------------------

    def __millier_cmn(self, number):
        if number < 1000:
            return self.centaine(number)

        if number >= 1000 and number < 10000:
            if (number % 1000) != 0:
                if number % 1000 > 0 \
                   and number % 1000 < 100:
                    return self.centaine(int(number/1000)) + u("千零") + self.centaine(number % 1000)
                else:
                    return self.centaine(int(number/1000)) + u("千") + self.centaine(number % 1000)
            return self.centaine(int(number/1000)) + u("千")
        return str(number)

    # -----------------------------------------------------------------------

    def __milliers_cmn(self, number):
        if number < 10000:
            return self.__millier_cmn(number)

        if (number % 10000) == 0:
            return self.unite(int(number/10000)) + u("万")
        if number >= 10000 and number < 100000000:
            if (number % 10000) != 0:
                if (number % 10000) > 0 and (number % 10000) < 1000:
                    return self.unite(int(number/10000)) + u("万零") + self.__millier_cmn(number % 10000)
                return self.unite(int(number/10000)) + u("万") + self.__millier_cmn(number % 10000)
            else:
                return u("万")
        return str(number)

    # -----------------------------------------------------------------------

    def __milliers_fra(self, number):
        if number < 1000:
            return self.centaine(number)

        # Milliers
        if number == 1000:
            return u("mille ")
        elif number > 1000 and number < 2000:
            return u("mille-") + self.centaine(number % 1000)
        elif number >= 2000 and number < 10000:
            if (number % 1000) == 0:
                return self.unite(int(number/1000)) + u("-mille-")
            return self.unite(int(number/1000)) + u("-mille-") + self.centaine(number % 1000)

        # Dizaines de milliers
        if number == 10000:
            return u("dix-mille")
        elif number > 10000 and number < 100000:
            if (number%1000) == 0:
                return self.dizaine(int(number/1000)) + u("-mille ")
            return self.dizaine(int(number/1000)) + u("-mille-") + self.centaine(number % 1000)

        # Centaines de milliers
        if number == 100000:
            return u("cent-mille")
        elif number >= 100000 and number < 1000000:
            if (number % 1000) == 0:
                return self.centaine(int(number/1000)) + u("-mille ")
            return self.centaine(int(number/1000)) + u("-mille-") + self.centaine(int(number % 1000))

        return str(number)

    # -----------------------------------------------------------------------

    def __milliers_ita(self,number):
        if number < 1000:
            return self.centaine(number)

        # Milliers
        if number == 1000:
            return u("mille")
        if number > 1000 and number < 2000:
            return u("mille-") + self.centaine(number % 1000)
        if number >= 2000 and number < 10000:
            if (number % 1000) != 0:
                return self.unite(int(number/1000)).strip() + u("-mila-") + self.centaine(number % 1000)
            return self.unite(int(number/1000)).strip() + u("-mila")

        # Dizaines de milliers
        if number == 10000:
            return u("diecimila")
        if number > 10000 and number < 100000:
            if (number % 1000) != 0:
                return self.dizaine(int(number/1000)).strip() + u("-mila-") + self.centaine(number % 1000)
            return self.dizaine(int(number/1000)) + u("-mila")

        # Centaines de milliers
        if number == 100000:
            return u("centomila")
        if number >= 100000 and number < 1000000:
            if (number % 1000) != 0:
                return self.centaine(int(number/1000)).strip() + u("-mila-") + self.centaine(int(number%1000))
            return self.centaine(int(number/1000)).strip() + u("mila-")

        return str(number)

    # -----------------------------------------------------------------------

    def __milliers_eng(self, number):
        if number < 1000:
            return self.centaine(number)

        n = number / 1000
        r = number % 1000
        s = u("%s thousand") % self.centaine(n)
        if r == 0:
            return s
        else:
            return u("%s %s") % (s, self.centaine(r))

    # -----------------------------------------------------------------------

    def __milliers_pol(self, number):
        if number < 1000:
            return self.centaine(number)

        n = number / 1000
        r = number % 1000
        if number < 2000:
            s = u("tysięcy")
        else:
            s = u("%s tysiące") % self.centaine(n)
        if r == 0:
            return s
        return u("%s %s") % (s, self.centaine(r))

    # -----------------------------------------------------------------------

    def milliers(self, number):
        """Convert a number from 1000 to 9999.

        :param number: (int)

        """
        if self._lang == "spa":
            return self.__milliers_spa(number)
        if "cmn" in self._lang  \
                or "yue" in self._lang  \
                or "jpn" in self._lang:
            return self.__milliers_cmn(number)
        if self._lang == "fra":
            return self.__milliers_fra(number)
        if self._lang == "ita":
            return self.__milliers_ita(number)
        if self._lang == "eng":
            return self.__milliers_eng(number)
        if self._lang == "pol":
            return self.__milliers_pol(number)
        if self._lang == "por":
            return self.__milliers_por(number)

        raise Exception('Unrecognized language: '+self._lang)

    # -------------------------------------------------------------------------
    # -----------------------------------------------------------------------

    def __millions_por(self, number):
        if number < 1000000:
            return self.milliers(number)

        n = number / 1000000
        r = number % 1000000

        if number < 2000000:
            s = u("un-millón")
        else:
            s = u("%s-millones") % self.milliers(n)
        if r == 0:
            return s
        return u("%s-%s") % (s, self.milliers(r))

    # -----------------------------------------------------------------------

    def __millions_spa(self, number):
        if number < 1000000:
            return self.milliers(number)

        n = number / 1000000
        r = number % 1000000

        if number < 2000000:
            s = u("un-millón")
        else:
            s = u("%s-millones") % self.milliers(n)
        if r == 0:
            return s
        return u("%s-%s") % (s, self.milliers(r))

    # -----------------------------------------------------------------------

    def __millions_cmn(self, number):
        if number < 100000000:
            return self.__milliers_cmn(number)

        if (number % 100000000) == 0:
            return self.__millier_cmn(int(number/100000000)) + u("亿")

        if (number % 100000000) != 0:
            if (number % 100000000) > 0 and (number % 100000000) < 10000000:
                return self.__millier_cmn(int(number/100000000)) + u("亿零") + self.__millier_cmn(number % 100000000)
            return self.__millier_cmn(int(number/100000000)) + u("亿") + self.__millier_cmn(number % 100000000)
        else:
            return u("亿")

    # -----------------------------------------------------------------------

    def __millions_fra(self,number):
        if number < 1000000:
            return self.milliers(number)

        if number >= 1000000 and number < 2000000:
            return u("un-million-") + self.milliers(int(number%1000000))

        if number >= 2000000 and number < 1000000000:
            return self.centaine(int(number/1000000)) + u("-millions-") + self.milliers(int(number % 1000000))

        return str(number)

    # -----------------------------------------------------------------------

    def __millions_ita(self,number):
        if number < 1000000:
            return self.milliers(number)

        if number >= 1000000 and number < 2000000:
            return u("un-milione-") + self.milliers(int(number % 1000000))

        if number >= 2000000 and number < 1000000000:
            return self.centaine(int(number/1000000)).strip() + u("-milioni-") + self.milliers(int(number % 1000000))

        return str(number)

    # -----------------------------------------------------------------------

    def __millions_eng(self, number):
        if number < 1000000:
            return self.milliers(number)

        n = number / 1000000
        r = number % 1000000
        s = u("%s million") % self.centaine(n)
        if r == 0:
            return s
        else:
            return u("%s %s") % (s, self.milliers(r))

    # -----------------------------------------------------------------------

    def __millions_pol(self, number):
        if number < 1000000:
            return self.milliers(number)

        if number >= 1000000 and number < 2000000:
            return u("milion ") + self.milliers(int(number % 1000000))

        if number >= 2000000 and number < 1000000000:
            return self.centaine(int(number/1000000)).strip() + u(" miliony ") + self.milliers(int(number % 1000000))

        return str(number)

    # -----------------------------------------------------------------------

    def millions(self,number):
        """
        Convert a number from 1000 to 1000000.
        """
        if self._lang == "spa":
            return self.__millions_spa(number)
        if "cmn" in self._lang  \
                or "yue" in self._lang  \
                or "jpn" in self._lang:
            return self.__millions_cmn(number)
        if self._lang == "fra":
            return self.__millions_fra(number)
        if self._lang == "ita":
            return self.__millions_ita(number)
        if self._lang == "eng":
            return self.__millions_eng(number)
        if self._lang == "pol":
            return self.__millions_pol(number)
        if self._lang == "por":
            return self.__millions_por(number)

        raise Exception('Unrecognized language: '+self._lang)

    # -------------------------------------------------------------------------
    # -----------------------------------------------------------------------

    def __milliards_spa(self, number):
        if number < 1000000000:
            return self.millions(number)
        n = number / 1000000000
        r = number % 1000000000
        s = u("%s-mil-millones") % self.millions(n)
        if r == 0:
            return s
        else:
            return u("%s-%s") % (s, self.millions(r))

    # -----------------------------------------------------------------------

    def __milliards_fra(self, number):
        if number < 1000000000:
            return self.millions(number)

        if number >= 1000000000 and number < 2000000000:
            return u("un-milliard-") + self.millions(int(number % 1000000000))

        if number >= 2000000000 and number < 1000000000000:
            return self.centaine(int(number/1000000000)) + u("-milliards-") + self.millions(int(number % 1000000000))

        return str(number)

    # -----------------------------------------------------------------------

    def __milliards_ita(self, number):
        if number < 1000000000:
            _str = self.millions(number)

        # Millions
        elif number >= 1000000000 and number < 2000000000:
            _str = u("un-miliardo-") + self.millions(int(number % 1000000000))

        elif number >= 2000000000 and number < 1000000000000:
            _str = "-" + self.centaine(int(number/1000000000)).strip() + u("-miliardi-") + self.millions(int(number % 1000000000))

        else:
            return str(number)
        return _str

    # -----------------------------------------------------------------------

    def __milliards_eng(self, number):
        if number < 1000000000:
            return self.millions(number)

        n = number / 1000000000
        r = number % 1000000000
        s = u("%s billion") % self.centaine(n)
        if r == 0:
            return s
        else:
            return u("%s %s") % (s, self.millions(r))

    # -----------------------------------------------------------------------

    def __milliards_pol(self, number):
        if number < 1000000000:
            return self.millions(number)

        if number >= 1000000000 and number < 2000000000:
            return u("miliard") + self.millions(int(number % 1000000000))

        if number >= 2000000000 and number < 1000000000000:
            return self.centaine(int(number/1000000000)) + u(" miliardy ") + self.millions(int(number % 1000000000))

        return str(number)

    # -----------------------------------------------------------------------

    def __milliards_por(self, number):
        if number < 1000000000:
            return self.millions(number)

        return self.milliers(int(number/1000000)) + u("-") + self.millions(int(number % 1000000))

    # -----------------------------------------------------------------------

    def __convert(self, number):

        if self._lang == "spa":
            return self.__milliards_spa(number)

        if "cmn" in self._lang  \
                or "yue" in self._lang  \
                or "jpn" in self._lang:
            return self.__millions_cmn(number)

        if self._lang == "fra":
            return self.__milliards_fra(number)

        if self._lang == "eng":
            return self.__milliards_eng(number)

        if self._lang == "ita":
            res = self.__milliards_ita(number)
            return res.replace('oo', 'o')  # ex: centoottanta -> centottanta

        if self._lang == "pol":
            return self.__milliards_pol(number)

        if self._lang == "por":
            return self.__milliards_por(number)

        raise ValueError("Unknown language {:s} for numerical conversion".format(self._lang))

    # -----------------------------------------------------------------------

    def convert(self, number):
        """Convert a number to a string. Example: 23 => twenty-three

        :param number: (int) A numerical representation
        :returns: string corresponding to the given number
        :raises: ValueError

        """
        if self._lang not in sppasNum.LANGUAGES:
            raise ValueError("Unknown language {:s} for numerical conversion".format(self._lang))

        number = str(number)
        if number.isdigit() is False:
            raise ValueError("Numerical conversion is available only for positive unsigned integers. Got {:s}.".format(number))

        _strnum = ""
        _w = str(number)
        _i = int(number)

        # Numbers starting by one or more '0' (like phone numbers...)
        while _w.startswith(u("0")):
            _strnum = _strnum + self.zero()
            _w = _w[1:]

        if len(_w) > 0:
            _strnum = _strnum + self.__convert(_i)

        return ' '.join(_strnum.split())

# ------------------------------------------------------------------


if __name__ == '__main__':
    import os
    import sys
    from argparse import ArgumentParser
    PROGRAM = os.path.abspath(__file__)

    parser = ArgumentParser(usage="%s -l lang" % os.path.basename(PROGRAM), prog=PROGRAM, description="Num2Letter command line interface.")
    parser.add_argument("-l", "--lang", required=True, help='Language code (iso639-3)')

    if len(sys.argv) <= 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    nb = sppasNum(args.lang)
    for line in sys.stdin:
        print(nb.convert(line).encode('utf8'))
