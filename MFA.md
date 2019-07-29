### Install MFA
```shell
data_mfa_url=https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.0/montreal-forced-aligner_linux.tar.gz
if [ ! -d $mfa_path ]; then
    wget $data_mfa_url
    tar -zxvf montreal-forced-aligner_linux.tar.gz
fi
cd montreal-forced-aligner
bin/mfa_train_and_align /MTTS/data/cantonese_demo/wav /MTTS/misc/cantonese_mtts.lexicon  /MTTS/data/cantonese_demo/output/textgrid
```

### Run mfa_align_and_train
Generate TextGrid files to train model on merlin
```shell
cd tools/montreal-forced-aligner
bin/mfa_train_and_align 
bin/mfa_train_and_align /Users/mirfan/PycharmProjects/MTTS/data/cantonese_demo/wav /Users/mirfan/PycharmProjects/MTTS/misc/cantonese_mtts.lexicon  /Users/mirfan/PycharmProjects/MTTS/data/cantonese_demo/output/textgrid
```