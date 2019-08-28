import glob
import os
import re

from utils.cleaner import clean_line, clean_name

utts = open("../data/cantonese_demo/cantonese_utts.txt", "w", encoding='utf-8')


def generate_utts_from_files():
    utts = open("../data/cantonese_demo/cantonese_utts.txt", "w", encoding='utf-8')
    for file in glob.glob("../data/txt/*.txt"):
        lines = open(file, encoding='utf-8').read().strip()
        base_name = os.path.basename(file)
        name = os.path.splitext(base_name)[0]
        sentence = "{} {}".format(name.strip(), lines.strip())
        sentence = re.sub(r"[﻿。，,.]+", "", sentence)
        utts.write(sentence + "\n")


def generate_utts_from_1000():
    utts = open("../data/cantonese_demo/cantonese_utts.txt", "w", encoding='utf-8')
    lines = open("../data/1000_uncleaned.txt", "r", encoding='utf8').readlines()
    for index, line in enumerate(lines):
        file, line = line.split("\t")
        line = clean_line(line)
        file = clean_name(file)
        utts.write("{} {}".format(file, line))
    utts.close()


if __name__ == "__main__":
    # generate_utts_from_files()
    generate_utts_from_1000()