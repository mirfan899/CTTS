#! /usr/bin/env python

__author__ = "virtuoso.irfan@gmail.com(Muhammad Irfan)"

import io
import sys

STDOUT = io.open(1, mode="wt", encoding="utf-8", closefd=False)

STATIC_QUESTIONS = r"""
QS "Toner_C-Syl_1"   {/A:1-}
QS "Toner_C-Syl_2"   {/A:2-}
QS "Toner_C-Syl_3"   {/A:3-}
QS "Toner_C-Syl_4"   {/A:4-}
QS "Toner_C-Syl_5"   {/A:5-}
QS "Toner_C-Syl_6"   {/A:6-}
QS "Toner_L-Syl_1"   {-1^}
QS "Toner_L-Syl_2"   {-2^}
QS "Toner_L-Syl_3"   {-3^}
QS "Toner_L-Syl_4"   {-4^}
QS "Toner_L-Syl_5"   {-5^}
QS "Toner_L-Syl_6"   {-6^}
QS "Toner_R-Syl_1"   {^1@}
QS "Toner_R-Syl_2"   {^2@}
QS "Toner_R-Syl_3"   {^3@}
QS "Toner_R-Syl_4"   {^4@}
QS "Toner_R-Syl_5"   {^5@}
QS "Toner_R-Syl_6"   {^6@}
CQS "Pos_C-Syl_in_C-Word(Fw)"                          {@(\d+)^}
CQS "Pos_C-Syl_in_C-Word(Bw)"                          {^(\d+)^}
CQS "Pos_C-Syl_in_C-Prosodic-Word(Fw)"                 {^(\d+)+}
CQS "Pos_C-Syl_in_C-Prosodic-Word(Bw)"                 {+(\d+)#}
CQS "Pos_C-Syl_in_C-Prosodic-Phrase(Fw)"               {#(\d+)-}
CQS "Pos_C-Syl_in_C-Prosodic-Phrase(Bw)"               {-(\d+)-}
CQS "Pos_C-Syl_in_Utterance(Fw)"                       {/B:(\d+)+}
CQS "Pos_C-Syl_in_Utterance(Bw)"                       {+(\d+)@}
CQS "Pos_C-Prosodic-Word_in_C-Prosodic-Phrase(Fw)"     {@(\d+)-}
CQS "Pos_C-Prosodic-Word_in_C-Prosodic-Phrase(Bw)"     {-(\d+)&}
CQS "Pos_C-Prosodic-Phrase_in_Utterance(Fw)"           {!(\d+)-}
CQS "Pos_C-Prosodic-Phrase_in_Utterance(Bw)"           {-(\d+)=}
CQS "Num_Syl_in_C-Word"                                {+(\d+)+}
CQS "Num_Syl_in_L-Word"                                {#(\d+)+}
CQS "Num_Syl_in_R-Word"                                {+(\d+)&}
CQS "Num_Syl_in_C-Prosodic-Word"                       {=(\d+)!}
CQS "Num_Syl_in_L-Prosodic-Word"                       {/D:(\d+)=}
CQS "Num_Syl_in_R-Prosodic-Word"                       {!(\d+)@}
CQS "Num_Syl_in_C-Prosodic-Phrase"                     {|(\d+)-}
CQS "Num_Syl_in_L-Prosodic-Phrase"                     {/E:(\d+)|}
CQS "Num_Syl_in_R-Prosodic-Phrase"                     {-(\d+)@}
CQS "Num_Prosodic-Word_in_C-Prosodic-Phrase"           {#(\d+)&}
CQS "Num_Prosodic-Word_in_L-Prosodic-Phrase"           {@(\d+)#}
CQS "Num_Prosodic-Word_in_R-Prosodic-Phrase"           {&(\d+)!}
CQS "Num_Syl_in_Utterance"                             {^(\d+)=}
CQS "Num_Word_in_Utterance"                            {=(\d+)_}
CQS "Num_Prosodic-Word_in_Utterance"                   {_(\d+)-}
CQS "Num_Prosodic-Phrase_in_Utterance"                 {-(\d+)!}
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

NASAL_QUESTIONS = [["L-Nasal", "*^%s-*"]]

LABIAL_QUESTIONS = [["L-Labial", "*^%s-*"]]
LABIAL2_QUESTIONS = [["L-Labial", "*^%s-*"]]

INITIAL_QUESTIONS = [["L-initial", "*^%s-*"]]
FINAL_QUESTIONS = [["L-final", "*^%s-*"]]
SILENCE_QUESTIONS = [["L-silence", "*^%s-*"]]

L_INITIAL_QUESTIONS = [["L", "*^%s-*"]]
L_FINAL_QUESTIONS = [["L", "*^%s?-*"]]

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

initial = ["b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "ng", "h", "gw", "kw", "w", "z", "c", "s", "j"]
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
    # Fricative ==================================================================
    f = []
    for v in Fricative:
        f.append(FRICATIVE_QUESTIONS[0][1] % v)
    f = ",".join(f)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (FRICATIVE_QUESTIONS[0][0], f)
    vf = []
    for v in Fricative:
        vf.append(VOICELESS_FRICATIVE_QUESTIONS[0][1] % v)
    vf = ",".join(vf)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (VOICELESS_FRICATIVE_QUESTIONS[0][0], vf)
    # Nasal ==================================================================
    n = []
    for v in Nasal:
        n.append(NASAL_QUESTIONS[0][1] % v)
    n = ",".join(n)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (NASAL_QUESTIONS[0][0], n)
    # Labial ==================================================================
    l = []
    for v in Labial:
        l.append(LABIAL_QUESTIONS[0][1] % v)
    l = ",".join(l)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (LABIAL_QUESTIONS[0][0], l)

    l2 = []
    for v in Labial2:
        l2.append(LABIAL2_QUESTIONS[0][1] % v)
    l2 = ",".join(l2)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (LABIAL2_QUESTIONS[0][0], l2)

    i = []
    for v in initial:
        i.append(INITIAL_QUESTIONS[0][1] % v)
    i = ",".join(i)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (INITIAL_QUESTIONS[0][0], i)

    f = []
    for v in final:
        f.append(FINAL_QUESTIONS[0][1] % v)
    f = ",".join(f)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (FINAL_QUESTIONS[0][0], f)

    s = []
    for v in silence:
        s.append(SILENCE_QUESTIONS[0][1] % v)
    s = ",".join(s)
    content += "QS \"%s\"\t\t\t\t{%s}\n" % (SILENCE_QUESTIONS[0][0], s)
    # L questions ==================================================================
    for v in initial:
        k = L_INITIAL_QUESTIONS[0][1] % v
        content += "QS \"%s-%s\"\t\t\t\t{%s}\n" % (L_INITIAL_QUESTIONS[0][0], v, k)
    for v in final:
        k = L_FINAL_QUESTIONS[0][1] % v
        content += "QS \"%s-%s\"\t\t\t\t{%s}\n" % (L_FINAL_QUESTIONS[0][0], v, k)
    for v in silence:
        k = SILENCE_QUESTIONS[0][1] % v
        content += "QS \"L-%s\"\t\t\t\t{%s}\n" % (v,  k)
    print(content)


if __name__ == "__main__":
    main()
