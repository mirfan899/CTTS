# Tries to create an 80/20 split between train and test sets, with even distribution of the three groups
# radio ('FC-R...'), dialog_0 ('FC-0...'), and dialog_1 ('FC-1...')
# Based on https://cs230-stanford.github.io/train-dev-test-split.html

import os
import shutil
import random

src_dir = 'hkcancor-utf8/utf8/'
filenames = os.listdir(src_dir)
filenames_radio = [filename for filename in filenames if filename[:4] == 'FC-R']
filenames_0 = [filename for filename in filenames if filename[:4] == 'FC-0']
filenames_1 = [filename for filename in filenames if filename[:4] == 'FC-1']

train_filenames = []
test_filenames = []
random.seed(1000)
for fnames_list in (filenames_radio, filenames_0, filenames_1):
    fnames_list.sort()
    random.shuffle(fnames_list)
    split = int(0.8*len(fnames_list))
    train_filenames += fnames_list[:split]
    test_filenames += fnames_list[split:]

# Make dst folders if they don't exist
train_dir = './train_data/'
test_dir = './test_data/'
for dst_path in (train_dir, test_dir):
        os.makedirs(dst_path, exist_ok=True)


def copy_files(filenames_list, src, dst):
    for file in filenames_list:
        shutil.copy2(src+file, dst+file)


copy_files(train_filenames, src_dir, train_dir)
copy_files(test_filenames, src_dir, test_dir)
