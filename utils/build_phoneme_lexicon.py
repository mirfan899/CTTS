import pandas as pd

consonant_list = [
    'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'h', 'gw', 'kw', 'w', 'z', 'c', 's', 'j'
]


def separate_syllable(syllable):
    """separate syllable to consonant + ' ' + vowel """
    # if "/" in syllable:
    #     syllable = syllable.split("/")[0]
    assert syllable[-1].isdigit()
    if syllable[0:2] in consonant_list:
        # return syllable[0:2].encode('utf-8'),syllable[2:].encode('utf-8')
        return syllable[0:2] + " " + syllable[2:]
    elif syllable[0] in consonant_list:
        # return syllable[0].encode('utf-8'),syllable[1:].encode('utf-8')
        return syllable[0] + " " + syllable[1:]
    else:
        # return (syllable.encode('utf-8'),)
        return syllable


dictionary = pd.read_csv("/Users/mirfan/PycharmProjects/MTTS/src/dictionary/zhy_jyut_cantonese.tsv", sep='\t')

print(dictionary.columns)
chinese = dictionary[dictionary.columns[0]].values.tolist()
phonemes = dictionary[dictionary.columns[1]].values.tolist()

dic = {}
for ch, ph in zip(chinese, phonemes):
    ph_new = ph
    if "/" in ph:
        ph_new = ph.split("/")[0]
        dic[ph_new] = separate_syllable(ph_new)
        # dic[ch.strip()] = ph_new.strip()
    else:
        # dic[ch.strip()] = ph.strip()
        dic[ph] = separate_syllable(ph)

print(len(dic))

with open('misc/cantonese_mtts.lexicon', "w") as file:
    for key, val in dic.items():
        line = key + ' ' + val
        file.write(line.strip())
        file.write("\n")
file.close()
