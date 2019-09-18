import re


def clean_line(line):
    line = re.sub("""([0-9A-Za-z 。，：“”！？.\s（）、——；‘]+)""", "", line)
    return line


def clean_name(name):
    name = re.sub("[.]+", "", name)
    return name
