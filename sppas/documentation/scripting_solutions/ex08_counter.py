#!/usr/bin python
"""

:author:       Fix Me
:date:         Now
:contact:      me@me.org
:license:      GPL, v3
:copyright:    Copyright (C) 2017  Fixme

:summary:      Simple script to compare 2 sets of data using NLP techniques.

Use of this software is governed by the GNU Public License, version 3.

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this script. If not, see <http://www.gnu.org/licenses/>.

"""
import collections
import math

from ex05_reading_file import read_file

# ---------------------------------------------------------------------------
# Declarations
# ---------------------------------------------------------------------------

# The corpora to deal with
corpus1 = 'corpus1.txt'
corpus2 = 'corpus2.txt'

# ---------------------------------------------------------------------------
# General functions
# ---------------------------------------------------------------------------


def total(my_list, item):
    """ Return the number of occurrences of an item in the list.

    :param my_list: (list) list of items
    :param item: (any) an item of the list (or not!)
    :returns: (int) number of occurrences of an item in my list

    """
    return my_list.count(item)

# ---------------------------------------------------------------------------


def frequency(my_list, item):
    """ Return the relative frequency of an item of a list.

    :param my_list: (list) list of items
    :param item: (any) an item of the list (or not!)
    :returns: (float) frequency of an item in my list

    """
    return float(my_list.count(item)) / float(len(my_list))

# ---------------------------------------------------------------------------


def percentage(my_list, item):
    """ Return the percentage of an item of a list.

    :param my_list: (list) list of items
    :param item: (any) an item of the list (or not!)
    :returns: (float) percentage of an item in my list

    """
    return 100.0 * frequency(my_list, item)

# ---------------------------------------------------------------------------
# NLP functions
# ---------------------------------------------------------------------------


def get_occranks(counter):
    """ Return a dictionary with key=occurrence, value=rank.

    :param counter: (Counter)
    :returns: dict

    """
    occ = dict()
    for k in counter.keys():
        v = counter[k]
        if v in occ:
            occ[v] += 1
        else:
            occ[v] = 1

    occ_ranks = {}
    for r, o in enumerate(reversed(sorted(occ.keys()))):
        occ_ranks[o] = r+1

    return occ_ranks

# ---------------------------------------------------------------------------


def get_ranks(counter):
    """ Return a dictionary with key=token, value=rank.

    :param counter: (Counter)
    :returns: dict

    """
    ranks = dict()
    occ_ranks = get_occranks(counter)
    for k in counter:
        occ = counter[k]
        ranks[k] = occ_ranks[occ]
    return ranks

# ---------------------------------------------------------------------------


def zipf(ranks, item):
    """ Return the Zipf Law value of an item.

    Zipf's law states that given some corpus of natural language utterances,
    the frequency of any word is inversely proportional to its rank in the
    frequency table. Thus the most frequent word will occur approximately
    twice as often as the second most frequent word, three times as often
    as the third most frequent word, etc.

    :param ranks: (dict) is a dictionary with key=entry, value=rank.
    :param item: (any) is an entry of the ranks dictionary
    :returns: Zipf value or -1 if the entry is missing

    """
    if item in ranks:
        return 0.1 / ranks[item]
    return -1

# ---------------------------------------------------------------------------


def tfidf(documents, item):
    """ Return the tf.idf of an item.

    Term frequency–inverse document frequency, is a numerical statistic
    that is intended to reflect how important a word is to a document in a
    collection or corpus. The tf.idf value increases proportionally to the
    number of times a word appears in the document, but is offset by the
    frequency of the word in the corpus, which helps to control for the fact
    that some words are generally more common than others.

    :param documents: a list of list of entries.
    :param item: (str)
    :returns: (float)

    """
    # Estimate tf of item in the corpus
    all_tokens = []
    for d in documents:
        all_tokens.extend(d)
    tf = frequency(all_tokens, item)

    # number of documents in the corpus
    D = len(documents)

    # number of documents with at least one occurrence of item
    dw = 0.0
    for d in documents:
        if item in d:
            dw += 1.0
    if dw == 0.0:
        return 0.0

    return tf * (math.log(D / dw))

# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    phones1 = read_file(corpus1)
    phones2 = read_file(corpus2)

    counter1 = collections.Counter(phones1)
    counter2 = collections.Counter(phones2)

    # Hapax
    hapax1 = [k for k in counter1.keys() if counter1[k] == 1]
    hapax2 = [k for k in counter2.keys() if counter2[k] == 1]
    print("Corpus 1, Number of hapax: {:d}.".format(len(hapax1)))
    print("Corpus 2, Number of hapax: {:d}.".format(len(hapax2)))

    # Zipf law
    ranks1 = get_ranks(counter1)
    ranks2 = get_ranks(counter2)
    for t in ['@', 'e', "E"]:
        print("Corpus 1: {:s} {:d} {:f} {:d} {:f}".format(
            t,
            total(phones1, t),
            frequency(phones1, t),
            ranks1.get(t, -1),
            zipf(ranks1, t)))
        print("Corpus 2: {:s} {:d} {:f} {:d} {:f}".format(
            t,
            total(phones2, t),
            frequency(phones2, t),
            ranks2.get(t, -1),
            zipf(ranks2, t)))

    # TF.IDF
    print("TF.IDF @: {0}".format(tfidf([phones1, phones2], '@')))
    print("TF.IDF e: {0}".format(tfidf([phones1, phones2], 'e')))
    print("TF.IDF E: {0}".format(tfidf([phones1, phones2], 'E')))
