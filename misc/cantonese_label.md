### Cantonese Label

* [HTS label](http://www.cs.columbia.edu/~ecooper/tts/lab_format.pdf)
label format for Cantonese(both are same)
* [HTS_LABEL](https://wiki.inf.ed.ac.uk/twiki/pub/CSTR/F0parametrisation/hts_lab_format.pdf)
* [Merlin Questions](https://github.com/CSTR-Edinburgh/merlin/tree/master/misc/questions)

[Question set](./questions-mandarin.hed)

```
层级          标注格式  
声韵母层     p1^p2-p3+p4=p5@p6@  
声调层       /A:a1-a2^a3@  
字/音节层    /B:b1+b2@b3^b4^b5+b6#b7-b8-  
词层         /C:c1_c2^c3#c4+c5+c6&  
韵律词层     /D:d1=d2!d3@d4-d5&  
韵律短语层   /E:e1|e2-e3@e4#e5&e6!e7-e8#  
语句层       /F:f1^f2=f3_f4-f5!
----------------------------------------------
Hierarchical            dimensioning format
Vocal matrix            p1^p2-p3+p4=p5@p6@
Tone layer              /A:a1-a2^a3@
Word/syllable layer     /B:b1+b2@b3^b4^b5+b6#b7-b8-
Word layer              /C:c1_c2^c3#c4+c5+c6&
Prosodic word layer     /D:d1=d2!d3@d4-d5&
Prosodic phrase layer   /E:e1|e2-e3@e4#e5&e6!e7-e8#
Statement layer         /F:f1^f2=f3_f4-f5!  
```
 
标号  |  含义
---- | ----
p1  |  前前基元
p2  |  前一基元
p3  |  当前基元
p4  |  后一基元
p5  |  后后基元
p6  |  当前音节的元音
----------------------------------------------
P1 | front front primitive
P2 | previous primitive
P3 | current primitive
P4 | latter primitive
P5 | post-primary primitive
P6 | vowel of the current syllable
---- | ----
a1  |  前一音节/字的声调
a2  |  当前音节/字的声调
a3  |  后一音节/字的声调
----------------------------------------------
A1 | The tone of the previous syllable/word
A2 | Current syllable/word tone
A3 | The tone of the last syllable/word
---- | ----
b1  |  当前音节/字到语句开始字的距离
b2  |  当前音节/字到语句结束字的距离
b3  |  当前音节/字在词中的位置（正序）
b4  |  当前音节/字在词中的位置（倒序）
b5  |  当前音节/字在韵律词中的位置（正序）
b6  |  当前音节/字在韵律词中的位置（倒序）
b7  |  当前音节/字在韵律短语中的位置（正序）
b8  |  当前音节/字在韵律短语中的位置（倒序）
----------------------------------------------
B1 | distance from the current syllable/word to the beginning of the statement
B2 | distance from the current syllable/word to the end of the statement
B3 | The position of the current syllable/word in the word (positive order)
B4 | Current syllable/word position in the word (reverse order)
B5 | The position of the current syllable/word in the prosody word (positive order)
B6 | The position of the current syllable/word in the prosody word (reverse order)
B7 | The position of the current syllable/word in the prosody phrase (positive order)
B8 | The position of the current syllable/word in the prosody phrase (reverse order)
---- | ----
c1  |  前一个词的词性
c2  |  当前词的词性
c3  |  后一个词的词性
c4  |  前一个词的音节数目
c5  |  当前词中的音节数目
c6  |  后一个词的音节数目
----------------------------------------------
C1 | The part of the word before
C2 | The part of speech of the current word
C3 | The part of the last word
C4 | Number of syllables in the previous word
C5 | number of syllables in the current word
C6 | Number of syllables in the next word
---- | ----
d1  |  前一个韵律词的音节数目
d2  |  当前韵律词的音节数目
d3  |  后一个韵律词的音节数目
d4  |  当前韵律词在韵律短语的位置（正序）
d5  |  当前韵律词在韵律短语的位置（倒序）
----------------------------------------------
D1 | Number of syllables of the previous prosodic word
D2 | number of syllables of the current prosodic word
D3 | Number of syllables of the next prosodic word
D4 | The position of the current prosody word in the prosodic phrase (positive order)
D5 | The position of the current prosody word in the prosodic phrase (reverse order)
---- | ----
e1  |  前一韵律短语的音节数目
e2  |  当前韵律短语的音节数目
e3  |  后一韵律短语的音节数目
e4  |  前一韵律短语的韵律词个数
e5  |  当前韵律短语的韵律词个数
e6  |  后一韵律短语的韵律词个数
e7  |  当前韵律短语在语句中的位置（正序）
e8  |  当前韵律短语在语句中的位置（倒序）
----------------------------------------------
E1 | Number of syllables of the previous prosodic phrase
E2 | Number of syllables of the current prosodic phrase
E3 | Number of syllables of the next prosodic phrase
E4 | Number of prosody words in the previous prosodic phrase
E5 | The number of prosody words in the current prosodic phrase
E6 | Number of prosody words in the last prosodic phrase
E7 | The position of the current prosodic phrase in the statement (positive order)
E8 | The position of the current prosodic phrase in the statement (reverse order)
---- | ----
f1  |  语句的语调类型
f2  |  语句的音节数目
f3  |  语句的词数目
f4  |  语句的韵律词数目
f5  |  语句的韵律短语数目
----------------------------------------------
F1 | tone type of statement
F2 | number of syllables of the statement
F3 | number of words in the statement
F4 | Number of prosodic words in the statement
F5 | Number of prosodic phrases in the statement