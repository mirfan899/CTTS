import re


def clean_line(line):
    line = re.sub("""。（[0-9]+）""", "", line)
    line = re.sub("""”（[0-9]+）""", "", line)
    line = re.sub("""。“（[0-9]+）""", "", line)
    line = re.sub("""？（[0-9]+）""", "", line)
    line = re.sub("""！“（[0-9]+）""", "", line)
    line = re.sub("""？“（[0-9]+）""", "", line)
    line = re.sub("""！（[0-9]+）""", "", line)
    line = re.sub("""[。，：“”！？. ]+""", "", line)
    line = re.sub("""“（[0-9]+）""", "", line)
    line = re.sub("""（[0-9]+）""", "", line)
    return line


def clean_name(name):
    name = re.sub("[.]+", "", name)
    return name
