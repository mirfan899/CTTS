import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

print(path)
from sppas import sppasTextNorm
# fileio = open("./cn.txt", "w")
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
    fileio = open("./temp.txt", "w")
    fileio.write(sentence)
    fileio.close()
    fileio = "./temp.txt"
    trs = ann.run([fileio])
    for tier in trs:
        if tier.get_name() == "Tokens":
            for a in tier:
                segments = a.serialize_labels(" ")
    return segments


# segments = segmentation('咁都真係天公做美啦，因為呢天氣真係好好，好涼爽。')
# print(segments)
