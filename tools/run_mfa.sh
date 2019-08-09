#!/usr/bin/env bash
# get current working directory
tools_dir=$(dirname $0)
cd ${tools_dir}
echo ${tools_dir}

mfa_path="./montreal-forced-aligner"
data_mfa_url=https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.0/montreal-forced-aligner_linux.tar.gz

if [[ ! -d ${mfa_path} ]]; then
    wget ${data_mfa_url}
    tar -zxvf montreal-forced-aligner_linux.tar.gz
fi

cd ${mfa_path}
bin/mfa_train_and_align /MTTS/data/cantonese_demo/wav /MTTS/misc/cantonese_mtts.lexicon  /MTTS/data/cantonese_demo/output/textgrid
