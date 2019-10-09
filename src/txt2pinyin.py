# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals
import sys
import re
from pypinyin import pinyin, Style, load_phrases_dict
from jyutping import get_jyutping

consonant_list = [
    'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'h', 'gw', 'kw', 'w', 'z', 'c', 's', 'j'
]

TRANSFORM_DICT = {'ju':'jv', 'qu':'qv', 'xu':'xv', 'zi':'zic',
                  'ci':'cic', 'si':'sic', 'zhi':'zhih', 
                  'chi':'chih', 'shi':'shih', 'ri':'rih',
                  'yuan':'yvan', 'yue':'yve', 'yun':'yvn',
                  'quan':'qvan','xuan':'xvan','juan':'jvan',
                  'qun':'qvn','xun':'xvn', 'jun':'jvn',
                  'iu':'iou', 'ui':'uei', 'un':'uen',
                  'ya':'yia', 'ye':'yie', 'yao':'yiao',
                  'you':'yiou', 'yan':'yian', 'yin':'yin',
                  'yang':'yiang', 'ying':'ying', 'yong':'yiong',
                  'wa':'wua', 'wo':'wuo', 'wai':'wuai',
                  'wei':'wuei', 'wan':'wuan', 'wen':'wuen',
                  'weng':'wueng', 'wang':'wuang'}

translate_dict = {'ju':'jv', 'qu':'qv', 'xu':'xv', 'zi':'zic',
                  'ci':'cic', 'si':'sic', 'zhi':'zhih', 
                  'chi':'chih', 'shi':'shih', 'ri':'rih',
                  'yuan':'yvan', 'yue':'yve', 'yun':'yvn',
                  'quan':'qvan','xuan':'xvan','juan':'jvan',
                  'qun':'qvn','xun':'xvn', 'jun':'jvn',
                  'iu':'iou', 'ui':'uei', 'un':'uen'}
# phone-set with y w, this is the default phone set
translate_dict_more = {'ya':'yia', 'ye':'yie', 'yao':'yiao',
                       'you':'yiou', 'yan':'yian', 'yin':'yin',
                       'yang':'yiang', 'ying':'ying', 'yong':'yiong',
                       'wa':'wua', 'wo':'wuo', 'wai':'wuai',
                       'wei':'wuei', 'wan':'wuan', 'wen':'wuen',
                       'weng':'wueng', 'wang':'wuang'}
# phone-set without y w 
translate_dict_less = {'ya':'ia', 'ye':'ie', 'yao':'iao',
                       'you':'iou', 'yan':'ian', 'yin':'in',
                       'yang':'iang', 'ying':'ing', 'yong':'iong',
                       'yvan':'van', 'yve':'ve', 'yvn':'vn',
                       'wa':'ua', 'wo':'uo', 'wai':'uai',
                       'wei':'uei', 'wan':'uan', 'wen':'uen',
                       'weng':'ueng', 'wang':'uang'}


def _pre_pinyin_setting():
    ''' fix pinyin error'''
    load_phrases_dict({'嗯':[['ēn']]})

_pre_pinyin_setting()


def pinyinformat(syllable):
    """format pinyin to mtts's format"""
    if not syllable[-1].isdigit():
        syllable = syllable + '5'
        # syllable = syllable + '7'
    assert syllable[-1].isdigit()
    syl_no_tone = syllable[:-1]
    if syl_no_tone in TRANSFORM_DICT:
        syllable = syllable.replace(syl_no_tone, TRANSFORM_DICT[syl_no_tone])
    return syllable
 
    """
    for key, value in translate_dict.items():
        syllable = syllable.replace(key, value)
    for key, value in translate_dict_more.items():
        syllable = syllable.replace(key, value)
    if not syllable[-1].isdigit():
        syllable = syllable + '5'
    return syllable
    """


def seprate_syllable(syllable):
    """separate syllable to consonant + ' ' + vowel """
    assert syllable[-1].isdigit()
    if syllable[0:2] in consonant_list:
        #return syllable[0:2].encode('utf-8'),syllable[2:].encode('utf-8')
        return syllable[0:2], syllable[2:]
    elif syllable[0] in consonant_list:
        #return syllable[0].encode('utf-8'),syllable[1:].encode('utf-8')
        return syllable[0], syllable[1:]
    else:
        #return (syllable.encode('utf-8'),)
        return (syllable,)


def txt2pinyin(txt):
    phone_list = []
    """
    if isinstance(txt, str):
        pinyin_list = pinyin(unicode(txt,'utf-8'), style = Style.TONE3)
    elif isinstance(txt, unicode):
        pinyin_list = pinyin(txt, style = Style.TONE3)
    else:
        print('error: unsupport coding form')
    """

    pinyin_list = get_jyutping(txt)
    # assert len(pinyin_list) == len(list(txt))
    # pinyin_list = pinyin(txt, style=Style.TONE3)
    for item in pinyin_list:
        phone_list.append(seprate_syllable(item))

        # phone_list.append(seprate_syllable(pinyinformat(item[0])))
    return phone_list


if __name__ == '__main__':
    # print(txt2pinyin('整完香腸同埋蛋之後呢我就叫馮曉立起身咁佢起咗身我哋一齊食早餐呢我先至開始拾嗰隻糭'))
    print(txt2pinyin("".join("中华人 民共和国 论居然")))

"""
用法举例
print(txt2pinyin('中华人民共和国论居然'))
['zh ong1', 'h ua2', 'r en2', 'm in2', 'g ong4', 'h e2', 'g uo2', 'l uen4', 'j
v1', 'r an2']
"""


