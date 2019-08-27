import re

lines = open("../data/1000_uncleaned.txt", "r", encoding='utf8').readlines()
lines = [line.strip() for line in lines if line.strip()]

T1000 = []
for index, line in enumerate(lines):
    line = re.sub("""。（[0-9]+）""", "", line)
    line = re.sub("""”（[0-9]+）""", "", line)
    line = re.sub("""。“（[0-9]+）""", "", line)
    line = re.sub("""？（[0-9]+）""", "", line)
    line = re.sub("""！“（[0-9]+）""", "", line)
    line = re.sub("""？“（[0-9]+）""", "", line)
    line = re.sub("""！（[0-9]+）""", "", line)
    line = re.sub("""[。，：“”！？]+""", "", line)
    line = re.sub("""“（[0-9]+）""", "", line)
    T1000.append(line)
