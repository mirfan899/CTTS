import re

lines = open("../weekn.txt", "r", encoding='utf8').readlines()
lines = [line.strip() for line in lines if line.strip()]
print(lines)


for index, line in enumerate(lines):
    if index % 2 == 0:
        txt = open("../data/week6/{}.txt".format(line), "w", encoding='utf8')
    else:
        line = re.sub("，", "", line)
        line = re.sub("。", "", line)
        line = re.sub(", ", "", line)
        txt.write(line)
        txt.close()
