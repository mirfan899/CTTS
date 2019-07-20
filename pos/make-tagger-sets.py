import os


def strip_data(src_dir, dst_path, make_untagged=False):
    """
    Generates a TSV (tab-separated values) file from HKCanCor transcription data.
    :param src_dir:
    :param dst_path:
    :param make_untagged:
    :return:
    """
    # regex = re.compile("^([^/]*)/([^/]*)")  # will match word along with POS tag
    if not isinstance(make_untagged, bool):
        raise ValueError("make_untagged must be a boolean!")

    filenames = os.listdir(src_dir)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    stripped_text = ""
    for filename in filenames:
        with open(src_dir + filename, 'r') as og_file:
            lines = [line.strip() for line in og_file]
            in_sentence = False
            for line in lines:
                if line == '<sent_tag>':
                    in_sentence = True
                    continue
                elif line == '</sent_tag>':
                    in_sentence = False
                    stripped_text += '\n'
                    continue
                if in_sentence:
                    segment = line.split('/')
                    if not make_untagged:
                        stripped_text += '{}\t{}\n'.format(segment[0], segment[1])
                    else:
                        stripped_text += segment[0] + '\t'
    with open(dst_path, 'w') as stripped_file:
        stripped_file.write(stripped_text)


if __name__ == "__main__":
    train_dir = './train_data/'
    test_dir = './test_data/'
    strip_data(train_dir, './train_set.tsv', False)
    strip_data(test_dir, './test_set.tsv', False)
    # strip_data(test_dir, './test_untagged.txt', True)
