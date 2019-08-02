#! /usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Generate HTS question file from json phonology.

Questions are generated according to the [1] format with support for Merlin CQS
tags.

[1] -
https://wiki.inf.ed.ac.uk/twiki/pub/CSTR/F0parametrisation/hts_lab_format.pdf

Usage
  ./festival_utils/generate_hts_questions.py si/festvox/ipa_phonology.json
"""

__author__ = "virtuoso.irfan@gmail.com(Muhammad Irfan)"

import io
import json
import sys

STDOUT = io.open(1, mode="wt", encoding="utf-8", closefd=False)

STATIC_QUESTIONS = r"""QS "C-Syl_Vowel==x"      {|x/C:}
QS "C-Syl_Vowel==no"    {|novowel/C:}
QS "L-Word_GPOS==0"     {/D:0_}
QS "L-Word_GPOS==aux"   {/D:aux_}
QS "L-Word_GPOS==cc"    {/D:cc_}
QS "L-Word_GPOS==content" {/D:content_}
QS "L-Word_GPOS==det"   {/D:det_}
QS "L-Word_GPOS==in"    {/D:in_}
QS "L-Word_GPOS==md"    {/D:md_}
QS "L-Word_GPOS==pps"   {/D:pps_}
QS "L-Word_GPOS==punc"    {/D:punc_}
QS "L-Word_GPOS==to"    {/D:to_}
QS "L-Word_GPOS==wp"    {/D:wp_}
QS "C-Word_GPOS==x"   {/E:x+}
QS "C-Word_GPOS==aux"   {/E:aux+}
QS "C-Word_GPOS==cc"    {/E:cc+}
QS "C-Word_GPOS==content" {/E:content+}
QS "C-Word_GPOS==det"   {/E:det+}
QS "C-Word_GPOS==in"    {/E:in+}
QS "C-Word_GPOS==md"    {/E:md+}
QS "C-Word_GPOS==pps"   {/E:pps+}
QS "C-Word_GPOS==punc"    {/E:punc+}
QS "C-Word_GPOS==to"    {/E:to+}
QS "C-Word_GPOS==wp"    {/E:wp+}
QS "R-Word_GPOS==0"     {/F:0_}
QS "R-Word_GPOS==aux"   {/F:aux_}
QS "R-Word_GPOS==cc"    {/F:cc_}
QS "R-Word_GPOS==content" {/F:content_}
QS "R-Word_GPOS==det"   {/F:det_}
QS "R-Word_GPOS==in"    {/F:in_}
QS "R-Word_GPOS==md"    {/F:md_}
QS "R-Word_GPOS==pps"   {/F:pps_}
QS "R-Word_GPOS==punc"    {/F:punc_}
QS "R-Word_GPOS==to"    {/F:to_}
QS "R-Word_GPOS==wp"    {/F:wp_}
CQS "Seg_Fw"                                      {@(\d+)_}
CQS "Seg_Bw"                                      {_(\d+)/A:}
CQS "L-Syl_Stress"                                {/A:(\d+)_}
CQS "L-Syl_Accent"                                {_(\d+)_}
CQS "L-Syl_Num-Segs"                              {_(\d+)/B:}
CQS "C-Syl_Stress"                                {/B:(\d+)-}
CQS "C-Syl_Accent"                                {-(\d+)-}
CQS "C-Syl_Num-Segs"                              {-(\d+)@}
CQS "Pos_C-Syl_in_C-Word(Fw)"                     {@(\d+)-}
CQS "Pos_C-Syl_in_C-Word(Bw)"                     {-(\d+)&}
CQS "Pos_C-Syl_in_C-Phrase(Fw)"                     {&(\d+)-}
CQS "Pos_C-Syl_in_C-Phrase(Bw)"                     {-(\d+)#}
CQS "Num-StressedSyl_before_C-Syl_in_C-Phrase"      {#(\d+)-}
CQS "Num-StressedSyl_after_C-Syl_in_C-Phrase"   {-(\d+)$}
CQS "Num-AccentedSyl_before_C-Syl_in_C-Phrase"      {$(\d+)-}
CQS "Num-AccentedSyl_after_C-Syl_in_C-Phrase"     {-(\d+)!}
CQS "Num-Syl_from_prev-StressedSyl"               {!(\d+)-}
CQS "Num-Syl_from_next-StressedSyl"                 {-(\d+);}
CQS "Num-Syl_from_prev-AccentedSyl"                 {;(\d+)-}
CQS "Num-Syl_from_next-AccentedSyl"                 {-(\d+)|}
CQS "R-Syl_Stress"                                {/C:(\d+)+}
CQS "R-Syl_Accent"                                {+(\d+)+}
CQS "R-Syl_Num-Segs"                              {+(\d+)/D:}
CQS "L-Word_Num-Syls"                             {_(\d+)/E:}
CQS "C-Word_Num-Syls"                             {+(\d+)@}
CQS "Pos_C-Word_in_C-Phrase(Fw)"                  {@(\d+)+}
CQS "Pos_C-Word_in_C-Phrase(Bw)"                  {+(\d+)&}
CQS "Num-ContWord_before_C-Word_in_C-Phrase"      {&(\d+)+}
CQS "Num-ContWord_after_C-Word_in_C-Phrase"         {+(\d+)#}
CQS "Num-Words_from_prev-ContWord"                  {#(\d+)+}
CQS "Num-Words_from_next-ContWord"                  {+(\d+)/F:}
CQS "R-Word_Num-Syls"                             {_(\d+)/G:}
CQS "L-Phrase_Num-Syls"                             {/G:(\d+)_}
CQS "L-Phrase_Num-Words"                          {_(\d+)/H:}
CQS "C-Phrase_Num-Syls"                             {/H:(\d+)=}
CQS "C-Phrase_Num-Words"                          {=(\d+)@}
CQS "Pos_C-Phrase_in_Utterance(Fw)"                 {@(\d+)=}
CQS "Pos_C-Phrase_in_Utterance(Bw)"                 {=(\d+)&}
CQS "R-Phrase_Num-Syls"                             {/I:(\d+)=}
CQS "R-Phrase_Num-Words"                          {=(\d+)/J:}
CQS "Num-Syls_in_Utterance"                         {/J:(\d+)+}
CQS "Num-Words_in_Utterance"                      {+(\d+)-}
CQS "Num-Phrases_in_Utterance"                    {-(\d+)}
"""

NASAL_VOWEL_QUESTIONS = [["L-Nasal_Vowel", "*^%s?-*"]]
SIMPLE_FINAL_QUESTIONS = [["L-Simple_Vowel", "*^%s?-*"]]
COMPOUND_FINAL_QUESTIONS = [["L-Compound_Vowel", "*^%s?-*"]]

TYPEA_QUESTIONS = [["L-TypeA", "*^%s?-*"]]
TYPEE_QUESTIONS = [["L-TypeE", "*^%s?-*"]]
TYPEI_QUESTIONS = [["L-TypeI", "*^%s?-*"]]
TYPEO_QUESTIONS = [["L-TypeO", "*^%s?-*"]]
TYPEU_QUESTIONS = [["L-TypeU", "*^%s?-*"]]
TYPEV_QUESTIONS = [["L-TypeV", "*^%s?-*"]]

ANTERIOR_NASAL_VOWEL_QUESTIONS = [["L-Anterior_Nasal_Vowel", "*^%s?-*"]]
POSTERIOR_NASAL_VOWEL_QUESTIONS = [["L-Posterior_Nasal_Vowel", "*^%s?-*"]]

STOP_QUESTIONS = [["L-Stop", "*^%s-*"]]
ASPIRATED_STOP_QUESTIONS = [["L-Aspirated_Sto", "*^%s-*"]]
UNASPIRATED_STOP_QUESTIONS = [["L-Unaspirated_Stop", "*^%s-*"]]

AFFRICATE_QUESTIONS = [["L-Affricate", "*^%s-*"]]
ASPIRATED_AFFRICATE_QUESTIONS = [["L-Aspirated_Affricate", "*^%s-*"]]
UNASPIRATED_AFFRICATE_QUESTIONS = [["L-Unaspirated_Affricate", "*^%s-*"]]

FRICATIVE_QUESTIONS = [["L-Fricative", "*^%s-*"]]
VOICELESS_FRICATIVE_QUESTIONS = [["L-Voiceless_Fricative", "*^%s-*"]]

Stop = ["p", "t", "k", "b", "d", "g"]
Aspirated_Stop = ["p", "t", "k"]
Unaspirated_Stop = ["b", "d", "g"]

Affricate = ["z", "c"]
Aspirated_Affricate = ["c"]
Unaspirated_Affricate = ["z"]

Fricative = ["f", "s", "h"]
Voiceless_Fricative = ["s"]

Nasal = ["m", "n", "ng"]

Labial = ["m", "b", "p"]
Labial2 = ["f"]

Simple_Final = ["am", "aam", "an", "aan", "em", "im", "in", "on", "ot", "eon", "un", "yun"]
Compound_Final = ["ang", "aang", "eng", "ing", "ong", "ok", "oeng", "ung"]

Nasal_Vowel = ["am", "aam", "an", "aan", "em", "im", "in", "on", "ot", "eon", "un", "yun", "ang", "aang", "eng", "ing",
               "ong", "ok", "oeng", "ung"]
Anterior_Nasal_Vowel = ["am", "aam", "an", "aan", "em", "im", "in", "on", "ot", "eon", "un", "yun"]
Posterior_Nasal_Vowel = ["ang", "aang", "eng", "ing", "ong", "ok", "oeng", "ung"]

TypeA = ["aa", "aai", "aau", "aam", "aan", "aang", "aap", "aat", "aak", "ai", "au", "am", "an", "ang", "ap", "at", "ak"]
TypeE = ["e", "eng", "ek", "ei", "eoi", "eon", "eot"]
TypeI = ["i", "iu", "im", "in", "ing", "ip", "it", "ik"]
TypeO = ["o", "on", "ong", "ot", "ok", "oi", "ou", "oe", "oeng", "oek"]
TypeU = ["u", "ui", "un", "ut", "ung", "uk"]
TypeV = ["yu", "yun", "yut"]

initial = ["b, p, m, f, d, t, n, l, g, k, ng, h, gw, kw, w, z, c, s, j"]
final = ["aa", "aai", "aau", "aam", "aan", "aang", "aap", "aat", "aak", "ai", "au", "am", "an", "ang", "ap", "at", "ak",
         "e", "eng", "ek", "ei", "eoi", "eon", "eot", "i", "iu", "im", "in", "ing", "ip", "it", "ik", "o", "on", "ong",
         "ot", "ok", "oi", "ou", "oe", "oeng", "oek", "u", "ui", "un", "ut", "ung", "uk", "yu", "yun", "yut", "ng", "m"]
silence = ["sil", "pau", "sp"]


def main():
    # phonology = json.loads(open(argv[1]).read())
    content = ""
    # Vowel =====================================================================
    nv = []
    for v in Nasal_Vowel:
        nv.append(NASAL_VOWEL_QUESTIONS[0][1] % v)
    nv = ",".join(nv)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (NASAL_VOWEL_QUESTIONS[0][0], nv)

    sf = []
    for v in Simple_Final:
        sf.append(SIMPLE_FINAL_QUESTIONS[0][1] % v)
    sf = ",".join(sf)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (SIMPLE_FINAL_QUESTIONS[0][0], sf)

    cf = []
    for v in Compound_Final:
        cf.append(COMPOUND_FINAL_QUESTIONS[0][1] % v)
    cf = ",".join(cf)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (COMPOUND_FINAL_QUESTIONS[0][0], cf)
    anv = []
    for v in Anterior_Nasal_Vowel:
        anv.append(ANTERIOR_NASAL_VOWEL_QUESTIONS[0][1] % v)
    anv = ",".join(anv)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (ANTERIOR_NASAL_VOWEL_QUESTIONS[0][0], anv)

    pnv = []
    for v in Posterior_Nasal_Vowel:
        pnv.append(POSTERIOR_NASAL_VOWEL_QUESTIONS[0][1] % v)
    pnv = ",".join(pnv)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (POSTERIOR_NASAL_VOWEL_QUESTIONS[0][0], pnv)

    ta = []
    for v in TypeA:
        ta.append(TYPEA_QUESTIONS[0][1] % v)
    ta = ",".join(ta)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (TYPEA_QUESTIONS[0][0], ta)

    te = []
    for v in TypeE:
        te.append(TYPEE_QUESTIONS[0][1] % v)
    te = ",".join(te)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (TYPEE_QUESTIONS[0][0], te)

    ti = []
    for v in TypeI:
        ti.append(TYPEI_QUESTIONS[0][1] % v)
    ti = ",".join(ti)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (TYPEI_QUESTIONS[0][0], ti)

    tu = []
    for v in TypeU:
        tu.append(TYPEO_QUESTIONS[0][1] % v)
    tu = ",".join(tu)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (TYPEO_QUESTIONS[0][0], tu)

    tv = []
    for v in TypeU:
        tv.append(TYPEO_QUESTIONS[0][1] % v)
    tv = ",".join(tv)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (TYPEO_QUESTIONS[0][0], tv)
    # STOP ======================================================================
    s = []
    for v in Stop:
        s.append(STOP_QUESTIONS[0][1] % v)
    s = ",".join(s)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (STOP_QUESTIONS[0][0], s)

    asp = []
    for v in Aspirated_Stop:
        asp.append(ASPIRATED_STOP_QUESTIONS[0][1] % v)
    asp = ",".join(asp)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (ASPIRATED_STOP_QUESTIONS[0][0], asp)

    unp = []
    for v in Unaspirated_Stop:
        unp.append(UNASPIRATED_STOP_QUESTIONS[0][1] % v)
    unp = ",".join(unp)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (UNASPIRATED_STOP_QUESTIONS[0][0], unp)
    # AFFRICATE ==================================================================
    af = []
    for v in Affricate:
        af.append(AFFRICATE_QUESTIONS[0][1] % v)
    af = ",".join(af)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (AFFRICATE_QUESTIONS[0][0], af)
    asp = []
    for v in Aspirated_Affricate:
        asp.append(ASPIRATED_AFFRICATE_QUESTIONS[0][1] % v)
    asp = ",".join(asp)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (ASPIRATED_AFFRICATE_QUESTIONS[0][0], asp)

    unp = []
    for v in Unaspirated_Affricate:
        unp.append(UNASPIRATED_AFFRICATE_QUESTIONS[0][1] % v)
    unp = ",".join(unp)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (UNASPIRATED_AFFRICATE_QUESTIONS[0][0], unp)


    # for qs in NASAL_VOWEL_QUESTIONS:
    #     for phoneinfo in Nasal_Vowel:
    #         content += "QS \"%s-%s\"\t\t\t\t{%s}\n" % (qs[0], phoneinfo,
    #                                                    qs[1] % phoneinfo)
    print(content)

    # Add phoneme questions.
    #  - Example - QS "C-uw"  {-uw+}
    # for qs in PHONEME_QUESTIONS:
    #     for phoneinfo in phonology["phones"]:
    #         phoneme = phoneinfo[0]
    #         content += "QS \"%s-%s\"\t\t\t\t{%s}\n" % (qs[0], phoneme,
    #                                                    qs[1] % (phoneme))
    #
    # # Add phoneme feature questions.
    # qs_list = {}
    # for phoneinfo in phonology["phones"]:
    #     phoneme = phoneinfo[0]
    #     features = phoneinfo[1:]
    #
    #     for feature in features:
    #         if feature in qs_list:
    #             qs_list.get(feature).append(phoneme)
    #         else:
    #             qs_list.update({feature: [phoneme]})
    #
    # # Example phoneme feature question.
    # # - QS "C-Vowel"  {-aa+,-ae+,-ah+}
    # for x in qs_list:
    #     content += "QS \"C-" + x + "\"\t\t\t\t{%s}\n" % (
    #         ",".join([("*^%s?-*") % y for y in qs_list.get(x)]))
    #
    # # Add syllabification questions.
    # # Example - QS "C-Syl_aa"  {|aa/C:}
    # for x in qs_list:
    #     content += "QS \"C-Syl-" + x + "\"\t\t\t\t{%s}\n" % (
    #         ",".join([("|%s/C:") % y for y in qs_list.get(x)]))
    #
    # content += STATIC_QUESTIONS
    #
    # STDOUT.write(content)


if __name__ == "__main__":
    main()
