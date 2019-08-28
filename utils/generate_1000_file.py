from cleaner import clean_line, clean_name


def generate():
    lines = open("../data/1000_uncleaned.txt", "r", encoding='utf8').readlines()
    lines = [line.strip() for line in lines if line.strip()]

    for index, line in enumerate(lines):
        file, line = line.split("\t")
        line = clean_line(line)
        file = clean_name(file)
        txt = open("../data/txt/{}.txt".format(file), "w", encoding='utf8')
        txt.write(line)
        txt.close()


if __name__ == "__main__":
    generate()
