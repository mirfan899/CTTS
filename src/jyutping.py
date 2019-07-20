# -*- coding: utf-8 -*-
"""
Convert Chinese characters to Jyutping.
"""
from __future__ import absolute_import
import dictionary


def get_jyutping_list(characters):
    """
    Convert Chinese characters to Jyutping.
    @return an array of Jyutping for each character.
    """
    result = []
    words = characters.split(" ")
    for word in words:
        for ch in word:
            result.append(search_single(ch))
    return result


def get_jyutping(characters):
    """
    Convert Chinese characters to Jyutping.
    @return an array of Jyutping for each character.
    """
    result = []
    for ch in characters:
        result.append(search_single(ch))
    return result


def search_single(character):
    if len(dictionary.CHS_DICT) == 0:
        dictionary.load_dictionary()
    jyp = dictionary.CHS_DICT.get(character)
    # get first word of multiple phoneme
    if jyp and '/' in jyp:
        jyp = jyp.split('/')[0]
    return jyp


def _test(word):
    print(word, get_jyutping(word))


if __name__ == '__main__':
    _test('整完香腸同埋蛋之後呢我就叫馮曉立起身咁佢起咗身我哋一齊食早餐呢我先至開始拾嗰隻糭')

