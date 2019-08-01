# Problem set example

设置此中文上下文标注和对应问题集时参考了 
* [HTS label](http://www.cs.columbia.edu/~ecooper/tts/lab_format.pdf)
* [Merlin Questions](https://github.com/CSTR-Edinburgh/merlin/tree/master/misc/questions)
* [本项目使用的上下文相关标注](https://github.com/Jackiexiao/MTTS/blob/master/docs/mddocs/mandarin_label.md)

问题集中的中英文对照

* initial：声母
* final: 韵母
* syllable(abbr: syl): 音节
* character: 字
* word : 词
* prosodic word: 韵律词
* prosodic phrase: 韵律短语
* intonational phrase: 语调短语

### Problem set design rules
The design of the problem set depends on the linguistic knowledge of different languages, and it matches the context annotation file. Changing the context annotation method also needs to change the problem set accordingly. For Chinese speech synthesis, the rules for designing the problem set are:
* Before the previous, the previous, the current, the next, the next next vowel is a synthetic primitive, there are 65 synthetic primitives, for example, to determine whether it is a vowel a QS "LL-a" QS "La " QS "Ca" QS "Ra" QS "RR-a"
* The initials feature division, for example, the initials can be divided into stop, squeak, nasal, lip, etc., the initials are divided into 24
* The finalization of the finals, for example, the finals can be divided into single finals, composite finals, respectively containing the finals of aeiouv, and the finals are divided into 8
* Other information division, part of speech, 26 parts of speech; tone type, 5; whether it is initial or final or mute, 3
* Proportional feature division, such as whether it is accent, accent, and the number of prosody words/phrases
* Location and quantity feature division

### Possible improvements
Problem concentration primitive plus tone, for example
```
QS "C-a1"
```

### Problem set optimization
The number of problem-focused problems is not the more the better (experience talk), the specific optimization method [todo]

### Initial division feature
```textmate
Dividing Features | Description          | Primitive List
Stop|Stop sound                          | p, t, k, b, d, g 
Aspirated Stop|Plug air                  | p，t, k, 
Unaspirated Stop|Non-plugged air         | b, d, g
Affricate|Stop sound                     | z, c
Aspirated Affricate|Plug airing          | c
Unaspirated Affricate|Non-serial air     | z
Fricative|fricative                      | f, s, h
Voiceless Fricative|Clear sound          | s
Voice Fricative |Turbid                  |
Nasal | nasal                            | m, n, ng
Labial | labial                          | m, b, p
labial2 | labial2                        | f
```

### The division feature of the finals
```textmate
Dividing Features | Description          | Criteria List
Simple_Final | Single vowel              | am, aam, an, aan, em, im, in, on, ot, eon, un, yun
Compound_Final | Complex vowel           | ang, aang, eng, ing, ong, ok, oeng, ung
Nasal_Vowel | Nasal vowel                | am, aam, an, aan, em, im, in, on, ot, eon, un, yun, ang, aang, eng, ing, ong, ok, oeng, ung
Anterior_Nasal_Vowel | Front nose vowel  | am, aam, an, aan, em, im, in, on, ot, eon, un, yun
Posterior_Nasal_Vowel | Post nasal vowel | ang, aang, eng, ing, ong, ok, oeng, ung
Type A | Finals containing A             | aa, aai, aau, aam, aan, aang, aap, aat, aak, ai, au, am, an, ang, ap, at, ak
Type E | a vowel containing E            | e, eng, ek, ei, eoi, eon, eot
Type I | Finals containing I             | i, iu, im, in, ing, ip, it, ik, 
Type O | Vowel with O                    | o, on, ong, ot, ok, oi, ou, oe, oeng, oek
Type U | Vowel containing U              | u, ui, un, ut, ung, uk
Type V | V-containing vowel              | yu, yun, yut
```

### Vowel
```textmate
Initial                                  | b, p, m, f, d, t, n, l, g, k, ng, h, gw, kw, w, z, c, s, j
Final                                    | aa, aai, aau, aam, aan, aang, aap, aat, aak, ai, au, am, an, ang, ap, at, ak, e, eng, ek, ei, eoi, eon, eot, i, iu, im, in, ing, ip, it, ik, o, on, ong, ot, ok, oi, ou, oe, oeng, oek, u, ui, un, ut, ung, uk, yu, yun, yut, ng, m 
Silence                                  | sil, pau, sp
```

### Number of positions, prosodic characteristics

Mainly refer to context-sensitive annotations for corresponding problem set design

### stress

If you consider accent, the following example questions about accents can be referred to `HTS label <http://www.cs.columbia.edu/~ecooper/tts/lab_format.pdf>`_ 以及 `Merlin Questions <https://github.com/CSTR-Edinburgh/merlin/tree/master/misc/questions>`_ 设计相关的数量，位置问题

E.g
* Before and after, whether the current primitive is accented
* How many accented in front of the current syllable in the prosodic phrase
* Accent position

### Problem set
  
### Finals
QS "C-Simple_Final"  
QS "C-Compound_Final"  
QS "C-Nasal_Vowel"
QS "C-Anterior_Nasal_Vowel"
QS "C-Posterior_Nasal_Vowel"
QS "C-TypeA"  
QS "C-TypeE"  
QS "C-TypeI"  
QS "C-TypeO"  
QS "C-TypeU"  
QS "C-TypeV"  

### Initials
QS "C-Stop"  
QS "C-Aspirated_Stop"  
QS "C-Unaspirated_Stop"  
QS "C-Affricate"  
QS "C-Aspirated_Affricate"  
QS "C-Unaspirated_Affricate"  
QS "C-Fricative"  
QS "C-Fricative2"  
QS "C-Voiceless_Fricative"  
QS "C-Voice_Fricative"  
QS "C-Nasal"  
QS "C-Nasal2"  
QS "C-Labial"  
QS "C-Labial2"  
QS "C-Apical"  
QS "C-Apical_Front"  
QS "C-Apical1"  
QS "C-Apical2"  
QS "C-Apical3"  
QS "C-Apical_End"  
QS "C-Apical_End2"  
QS "C-Tongue_Top"  
QS "C-Tongue_Root"  
QS "C-Zero"  
    
### Determine whether it is an initial, final, fine (sil+pau+sp)
QS "C-initial"  
QS "C-final"  
QS "C-silence"  
QS "L-initial"  
QS "L-final"  
QS "L-silence"  
QS "R-initial"  
QS "R-final"  
QS "R-silence"  
        
### Part of speech  
QS "C-POS==a"  
QS "C-POS==b"  
QS "C-POS==c"  
QS "C-POS==d"  
QS "C-POS==e"  
QS "C-POS==f"  
QS "C-POS==g"  
QS "C-POS==h"  
QS "C-POS==i"  
QS "C-POS==j"  
QS "C-POS==k"  
QS "C-POS==l"  
QS "C-POS==m"  
QS "C-POS==n"  
QS "C-POS==o"  
QS "C-POS==p"  
QS "C-POS==q"  
QS "C-POS==r"  
QS "C-POS==s"  
QS "C-POS==t"  
QS "C-POS==u"  
QS "C-POS==v"  
QS "C-POS==w"  
QS "C-POS==x"  
QS "C-POS==y"  
QS "C-POS==z"  
    
    
### Synthetic primitive part  
QS "C-b"  
QS "C-p"  
QS "C-m"  
QS "C-f"  
QS "C-d"  
QS "C-t"  
QS "C-n"  
QS "C-l"  
QS "C-g"  
QS "C-k"  
QS "C-h"  
QS "C-j"  
QS "C-q"  
QS "C-x"  
QS "C-zh"  
QS "C-ch"  
QS "C-sh"  
QS "C-r"  
QS "C-z"  
QS "C-c"  
QS "C-s"  
QS "C-y"  
QS "C-w"  
QS "C-a"  
QS "C-o"  
QS "C-e"  
QS "C-ea"  
QS "C-i"  
QS "C-u"  
QS "C-v"  
QS "C-ic"  
QS "C-ih"  
QS "C-er"  
QS "C-ai"  
QS "C-ei"  
QS "C-ao"  
QS "C-ou"  
QS "C-ia"  
QS "C-ie"  
QS "C-ua"  
QS "C-uo"  
QS "C-ve"  
QS "C-iao"  
QS "C-iou"  
QS "C-uai"  
QS "C-uei"  
QS "C-an"  
QS "C-ian"  
QS "C-uan"  
QS "C-van"  
QS "C-en"  
QS "C-in"  
QS "C-uen"  
QS "C-vn"  
QS "C-ang"  
QS "C-iang"  
QS "C-uang"  
QS "C-eng"  
QS "C-ing"  
QS "C-ueng"  
QS "C-ong"  
QS "C-iong"  
QS "C-sil"  
QS "C-sp"  
QS "C-pau"  
    
QS "L-b"  
QS "L-p"  
QS "L-m"  
QS "L-f"  
QS "L-d"  
QS "L-t"  
QS "L-n"  
QS "L-l"  
QS "L-g"  
QS "L-k"  
QS "L-h"  
QS "L-j"  
QS "L-q"  
QS "L-x"  
QS "L-zh"  
QS "L-ch"  
QS "L-sh"  
QS "L-r"  
QS "L-z"  
QS "L-c"  
QS "L-s"  
QS "L-y"  
QS "L-w"  
QS "L-a"  
QS "L-o"  
QS "L-e"  
QS "L-ea"  
QS "L-i"  
QS "L-u"  
QS "L-v"  
QS "L-ic"  
QS "L-ih"  
QS "L-er"  
QS "L-ai"  
QS "L-ei"  
QS "L-ao"  
QS "L-ou"  
QS "L-ia"  
QS "L-ie"  
QS "L-ua"  
QS "L-uo"  
QS "L-ve"  
QS "L-iao"  
QS "L-iou"  
QS "L-uai"  
QS "L-uei"  
QS "L-an"  
QS "L-ian"  
QS "L-uan"  
QS "L-van"  
QS "L-en"  
QS "L-in"  
QS "L-uen"  
QS "L-vn"  
QS "L-ang"  
QS "L-iang"  
QS "L-uang"  
QS "L-eng"  
QS "L-ing"  
QS "L-ueng"  
QS "L-ong"  
QS "L-iong"  
QS "L-sil"  
QS "L-sp"  
QS "L-pau"  
    
    
QS "R-b"  
QS "R-p"  
QS "R-m"  
QS "R-f"  
QS "R-d"  
QS "R-t"  
QS "R-n"  
QS "R-l"  
QS "R-g"  
QS "R-k"  
QS "R-h"  
QS "R-j"  
QS "R-q"  
QS "R-x"  
QS "R-zh"  
QS "R-ch"  
QS "R-sh"  
QS "R-r"  
QS "R-z"  
QS "R-c"  
QS "R-s"  
QS "R-y"  
QS "R-w"  
QS "R-a"  
QS "R-o"  
QS "R-e"  
QS "R-ea"  
QS "R-i"  
QS "R-u"  
QS "R-v"  
QS "R-ic"  
QS "R-ih"  
QS "R-er"  
QS "R-ai"  
QS "R-ei"  
QS "R-ao"  
QS "R-ou"  
QS "R-ia"  
QS "R-ie"  
QS "R-ua"  
QS "R-uo"  
QS "R-ve"  
QS "R-iao"  
QS "R-iou"  
QS "R-uai"  
QS "R-uei"  
QS "R-an"  
QS "R-ian"  
QS "R-uan"  
QS "R-van"  
QS "R-en"  
QS "R-in"  
QS "R-uen"  
QS "R-vn"  
QS "R-ang"  
QS "R-iang"  
QS "R-uang"  
QS "R-eng"  
QS "R-ing"  
QS "R-ueng"  
QS "R-ong"  
QS "R-iong"  
QS "R-sil"  
QS "R-sp"  
QS "R-pau"  
    
    
QS "LL-b"  
QS "LL-p"  
QS "LL-m"  
QS "LL-f"  
QS "LL-d"  
QS "LL-t"  
QS "LL-n"  
QS "LL-l"  
QS "LL-g"  
QS "LL-k"  
QS "LL-h"  
QS "LL-j"  
QS "LL-q"  
QS "LL-x"  
QS "LL-zh"  
QS "LL-ch"  
QS "LL-sh"  
QS "LL-r"  
QS "LL-z"  
QS "LL-c"  
QS "LL-s"  
QS "LL-y"  
QS "LL-w"  
QS "LL-a"  
QS "LL-o"  
QS "LL-e"  
QS "LL-ea"  
QS "LL-i"  
QS "LL-u"  
QS "LL-v"  
QS "LL-ic"  
QS "LL-ih"  
QS "LL-er"  
QS "LL-ai"  
QS "LL-ei"  
QS "LL-ao"  
QS "LL-ou"  
QS "LL-ia"  
QS "LL-ie"  
QS "LL-ua"  
QS "LL-uo"  
QS "LL-ve"  
QS "LL-iao"  
QS "LL-iou"  
QS "LL-uai"  
QS "LL-uei"  
QS "LL-an"  
QS "LL-ian"  
QS "LL-uan"  
QS "LL-van"  
QS "LL-en"  
QS "LL-in"  
QS "LL-uen"  
QS "LL-vn"  
QS "LL-ang"  
QS "LL-iang"  
QS "LL-uang"  
QS "LL-eng"  
QS "LL-ing"  
QS "LL-ueng"  
QS "LL-ong"  
QS "LL-iong"  
QS "LL-sil"  
QS "LL-sp"  
QS "LL-pau"  
    
    
    
QS "RR-b"  
QS "RR-p"  
QS "RR-m"  
QS "RR-f"  
QS "RR-d"  
QS "RR-t"  
QS "RR-n"  
QS "RR-l"  
QS "RR-g"  
QS "RR-k"  
QS "RR-h"  
QS "RR-j"  
QS "RR-q"  
QS "RR-x"  
QS "RR-zh"  
QS "RR-ch"  
QS "RR-sh"  
QS "RR-r"  
QS "RR-z"  
QS "RR-c"  
QS "RR-s"  
QS "RR-y"  
QS "RR-w"  
QS "RR-a"  
QS "RR-o"  
QS "RR-e"  
QS "RR-ea"  
QS "RR-i"  
QS "RR-u"  
QS "RR-v"  
QS "RR-ic"  
QS "RR-ih"  
QS "RR-er"  
QS "RR-ai"  
QS "RR-ei"  
QS "RR-ao"  
QS "RR-ou"  
QS "RR-ia"  
QS "RR-ie"  
QS "RR-ua"  
QS "RR-uo"  
QS "RR-ve"  
QS "RR-iao"  
QS "RR-iou"  
QS "RR-uai"  
QS "RR-uei"  
QS "RR-an"  
QS "RR-ian"  
QS "RR-uan"  
QS "RR-van"  
QS "RR-en"  
QS "RR-in"  
QS "RR-uen"  
QS "RR-vn"  
QS "RR-ang"  
QS "RR-iang"  
QS "RR-uang"  
QS "RR-eng"  
QS "RR-ing"  
QS "RR-ueng"  
QS "RR-ong"  
QS "RR-iong"  
QS "RR-sil"  
QS "RR-sp"  
QS "RR-pau"  
     
### Stress problem  
重音为1，不重音为0
QS "C-Stressed"  
QS "L-Stressed"  
QS "R-Stressed"     
     
### tone  
CQS "Toner_C-Syl"
CQS "Toner_L-Syl"
CQS "Toner_R-Syl"
 
### Location problem  
CQS "Pos_C-Syl_in_C-Word(Fw)"	                     
CQS "Pos_C-Syl_in_C-Word(Bw)"	                     
CQS "Pos_C-Syl_in_C-Prosodic-Word(Fw)"	                   
CQS "Pos_C-Syl_in_C-Prosodic-Word(Bw)"	                   
CQS "Pos_C-Syl_in_C-Prosodic-Phrase(Fw)"	                   
CQS "Pos_C-Syl_in_C-Prosodic-Phrase(Bw)"	                   
CQS "Pos_C-Syl_in_Utterance(Fw)"	                   
CQS "Pos_C-Syl_in_Utterance(Bw)"	                   
    
CQS "Pos_C-Word_in_C-Prosodic-Word(Fw)"	                   
CQS "Pos_C-Word_in_C-Prosodic-Word(Bw)"	                   
CQS "Pos_C-Word_in_C-Prosodic-Phrase(Fw)"	                   
CQS "Pos_C-Word_in_C-Prosodic-Phrase(Bw)"	                   
CQS "Pos_C-Word_in_Utterance(Fw)"	                   
CQS "Pos_C-Word_in_Utterance(Bw)"	                   
    
CQS "Pos_C-Prosodic-Word_in_C-Prosodic-Phrase(Fw)"	                   
CQS "Pos_C-Prosodic-Word_in_C-Prosodic-Phrase(Bw)"	                   
CQS "Pos_C-Prosodic-Word_in_Utterance(Fw)"	                   
CQS "Pos_C-Prosodic-Word_in_Utterance(Bw)"	                   
    
CQS "Pos_C-Prosodic-Phrase_in_Utterance(Fw)"	                   
CQS "Pos_C-Prosodic-Phrase_in_Utterance(Bw)"	                   
    
### Quantity problem  
CQS "Num_Syl_in_C-Word"	                     
CQS "Num_Syl_in_L-Word"	                     
CQS "Num_Syl_in_R-Word"	                     
CQS "Num_Syl_in_C-Prosodic-Word"	                     
CQS "Num_Syl_in_L-Prosodic-Word"	                     
CQS "Num_Syl_in_R-Prosodic-Word"	                     
CQS "Num_Syl_in_C-Prosodic-Phrase"	                     
CQS "Num_Syl_in_L-Prosodic-Phrase"	                     
CQS "Num_Syl_in_R-Prosodic-Phrase"	                     
    
CQS "Num_Word_in_C-Prosodic-Word"	                     
CQS "Num_Word_in_L-Prosodic-Word"	                     
CQS "Num_Word_in_R-Prosodic-Word"	                     
CQS "Num_Word_in_C-Prosodic-Phrase"	                     
CQS "Num_Word_in_L-Prosodic-Phrase"	                     
CQS "Num_Word_in_R-Prosodic-Phrase"	                     
    
CQS "Num_Prosodic-Word_in_C-Prosodic-Phrase"	                     
CQS "Num_Prosodic-Word_in_L-Prosodic-Phrase"	                     
CQS "Num_Prosodic-Word_in_R-Prosodic-Phrase"	                     
    
CQS "Num_Syl_in_Utterance"	                     
CQS "Num_Word_in_Utterance"	                     
CQS "Num_Prosodic-Word_in_Utterance"	                     
CQS "Num_Prosodic-Pharse_in_Utterance"	                     
    