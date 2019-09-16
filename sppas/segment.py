import os
import re
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from sppas import sppasTextNorm
# fileio = open("./temp.txt", "w")
# fileio.write('咁都真係天公做美啦，因為呢天氣真係好好，好涼爽。')
# fileio.close()
# fileio = "./cn.txt"
vocab = "../sppas/resources/vocab/yue.vocab"


lang = os.path.basename(vocab)[:3]
ann = sppasTextNorm(log=None)
ann.load_resources(vocab, lang=lang)


def segmentation(sentence=None):
    """Convert the sentence into words list
    :param sentence:
    :return: words list
    """
    segments = []
    # Create a temp file for segmentation for sppas
    fileio = open("temp.txt", "w")
    fileio.write(sentence)
    fileio.close()
    fileio = "temp.txt"
    trs = ann.run([fileio])
    for tier in trs:
        if tier.get_name() == "Tokens":
            for a in tier:
                segments = a.serialize_labels(" ")
    return segments


segments = segmentation('那是公元前二百四十六年至二百十年兩千多年前的事了')
print(segments)


def cline(line):
    line = re.sub("""([0-9A-Za-z 。，：“”！？.\s（）]+)""", "", line)
    return line


def cname(name):
    name = re.sub("[.]+", "", name)
    return name


def build_segmented_files():
    lines = open("../data/1000_uncleaned.txt", "r", encoding='utf8').readlines()
    lines = [line.strip() for line in lines if line.strip()]

    for index, line in enumerate(lines):
        file, line = line.split("\t")
        line = re.sub("""([0-9A-Za-z 。，：“”！？.\s（）]+)""", "", line)
        line = cline(line)
        file = cname(file)
        line = segmentation(sentence=line)
        print(line)
        txt = open("../data/segmentation/{}.txt".format(file), "w", encoding='utf8')
        txt.write(line)
        txt.close()


if __name__ == '__main__':
    build_segmented_files()
