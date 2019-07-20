"""
eSpeak Dictionary
"""
from __future__ import absolute_import
import io

CHS_DICT = {}


def load_dictionary():

    dictionary_file = "/Users/mirfan/PycharmProjects/MTTS/src/dictionary/zhy_jyut_cantonese.tsv"
    # logger.log('Load dictionary %s.' % dictionary_file)
    with io.open(dictionary_file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split('\t')
            chs, jyp = line
            CHS_DICT[chs] = jyp


if __name__ == '__main__':
    load_dictionary()
