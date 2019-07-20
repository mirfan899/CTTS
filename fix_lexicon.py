import os


# some unknown characters
"""
"我 ŋ o5" ŋ???
"記 ɡ eiɜ" ɜ???
"""


lexicon = open("misc/cantonese_mtts.lexicon", 'r', encoding='utf-8').readlines()
lines = list(set(lexicon))

file = open("misc/clean_cantonese_mtts.lexicon", 'w', encoding='utf-8')
for line in lines:
    file.write(line)
file.close()
exit()