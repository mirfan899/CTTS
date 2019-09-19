from jyutping import get_jyutping
import pandas as pd
import re


def clean_line(line):
    line = re.sub("""([0-9A-Za-z 。，：“”！？.\s（）、——；‘]+)""", "", line)
    return line


def clean_name(name):
    name = re.sub("[.]+", "", name)
    return name


def generate():
    names = []
    transcripts = []
    lines = open("../data/1000_uncleaned.txt", "r", encoding='utf8').readlines()
    lines = [line.strip() for line in lines if line.strip()]

    for index, line in enumerate(lines):
        name, transcript = line.split("\t")
        transcript = clean_line(transcript)
        name = clean_name(name)
        transcript = " ".join(get_jyutping(transcript))
        names.append(name)
        transcripts.append(transcript)
    data = pd.DataFrame({"id": names, "transcript": transcripts, "transcript_clean": transcripts})
    data.to_csv("../data/metadata.csv", index=False, header=False, sep="|")


if __name__ == "__main__":
    generate()
