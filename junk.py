import pandas as pd

dictionary = pd.read_csv("src/dictionary/zhy_jyut_cantonese.tsv", sep='\t', encoding='utf-8')
characters = dictionary[dictionary.columns[0]].values.tolist()[:10]
jyutping = dictionary[dictionary.columns[1]].values.tolist()[:10]

chinese = []
phonemes = []
# for ch, jyutping in zip(characters, jyutping):
#     # Call any command line lib to get console results in output variable
#     output = os.popen("echo '{}' | phonemize -l yue -b espeak -p ' ' -s '' -w ''".format(ch)).read()
#
#     if output:
#         chinese.append(ch.strip())
#         phonemes.append(output.strip())
#
# total = pd.DataFrame({"chinese": chinese, "jyut": phonemes})

with open('./junk.csv', "w") as csv_file:
    for ch, ph in zip(characters, jyutping):
        line = ch + ' ' + ph
        csv_file.write(line.strip())
        csv_file.write("\n")
csv_file.close()
# total.to_csv("./junk.csv", sep=' ', index=False, header=False, encoding='utf-8')
# for i, ch in enumerate(characters[:100]):
#     print(i, ch)
# output = os.popen("ls -l").read()
# print(output)
new_pinyin_list = []
for item in pinyin_list:
    if not item:
        logger.warning(
            '{} do not generate right pinyin'.format(numstr))
    if not item[0][-1].isdigit():
        # phone = item[0] + '5'
        phone = item[0] + '6'
        print(phone)
    else:
        phone = item[0]
    new_pinyin_list.append(phone)

new_pinyin_list = []
for item in pinyin_list:
    if not item:
        logger.warning(
            '{} do not generate right pinyin'.format(numstr))
    if not item[0][-1].isdigit():
        print(item([0][-1]))
        phone = item[0] + '5'
        # phone = item[0] + '6'
    else:
        # phone = item[0]
        phone = item[0].replace('v', 'u')
    new_pinyin_list.append(phone)

valid_txtlines = []
error_list = []
pattern = re.compile('(?!#(?=\d))(?![，。,.])[\W]')
line = "ASR14 整完香腸之後呢，我就煎蛋。咁我想整嗰啲滑蛋呢，個...我自己個秘訣就係要加左啲水先嘅，咁就可以令到嗰啲蛋滑少少。"
num, txt = line.split(' ', 1)
if bool(re.search('[A-Za-z]', txt)) or bool(
        re.search('(?<!#)\d', txt)):
    error_list.append(num)
else:
    # pinyin last phone is 4
    # txt = re.sub('[,.，。]', '#4', txt)
    # jyutping last phone is 6
    txt = re.sub('[,.，。]', '#6', txt)
    txt = pattern.sub('', txt)
    # 去除除了韵律标注'#'之外的所有非中文文本, 数字, 英文字符符号
    valid_txtlines.append(num + ' ' + txt)

from jieba import posseg
import re

prosody_txt = "ASR16 嗰一隻糭呢係豆沙糭嚟嘅，係馮曉立前一日喺超級市場嗰度買嘅。係一隻奇華嘅糭啦。咁佢就話拾三十分鐘食得不過最後我哋廿分鐘其實都好喇。"
prosody_words = re.split('#\d', prosody_txt)
rhythms = re.findall('#\d', prosody_txt)
txt = ''.join(prosody_words)
words = []
poses = []
for word, pos in posseg.cut(txt):
    words.append(word)
    poses.append(pos[0])
index = 0
insert_time = 0
length = len(prosody_words[index])
i = 0
while i < len(words):
    done = False
    while not done:
        if (len(words[i]) > length):
            # print(words[i], prosody_words[index])
            length += len(prosody_words[index + 1])
            rhythms[index] = ''
            index += 1
        elif (len(words[i]) < length):
            # print(' less than ', words[i], prosody_words[index])
            rhythms.insert(index + insert_time, '#0')
            insert_time += 1
            length -= len(words[i])
            i += 1
        else:
            # print('equal :', words[i])
            # print(rhythms)
            done = True
            index += 1
    else:
        if (index < len(prosody_words)):
            length = len(prosody_words[index])
        i += 1
# if rhythms[-1] != '#4':
if rhythms[-1] != '#6':
    # rhythms.append('#4')
    rhythms.append('#6')
rhythms = [x for x in rhythms if x != '']
print(words, poses, rhythms)

# print(rhythms)
consonant_list = [
    'b', 'P', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'h', 'gw', 'kw', 'w', 'z', 'c', 's', 'j'
]
syllable = "taan1"
assert syllable[-1].isdigit()
if syllable[0:2] in consonant_list:
    # return syllable[0:2].encode('utf-8'),syllable[2:].encode('utf-8')
    print(syllable[0:2], syllable[2:])
elif syllable[0] in consonant_list:
    # return syllable[0].encode('utf-8'),syllable[1:].encode('utf-8')
    print(syllable[0], syllable[1:])
else:
    # return (syllable.encode('utf-8'),)
    print(syllable)
