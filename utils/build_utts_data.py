import glob
import os
import re

utts = open("../data/cantonese_demo/cantonese_utts.txt", "w", encoding='utf-8')
for file in glob.glob("../data/txt/*.txt"):
    lines = open(file, encoding='utf-8').read().strip()

    base_name = os.path.basename(file)
    name = os.path.splitext(base_name)[0]

    # sentence = "%s %s" % (name.strip(), str(lines.strip()))

    sentence = "{} {}".format(name.strip(), lines.strip())
    # Some weird space in chinese
    sentence = re.sub(r"﻿", "", sentence)
    sentence = re.sub(r"。", "", sentence)
    sentence = re.sub(r"，", "", sentence)
    sentence = re.sub(r",", "", sentence)
    sentence = sentence.replace(".", "")
    # sentence = re.sub(r".", "", sentence)
    utts.write(sentence + "\n")
