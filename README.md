# Cantonese TTS Frontend

Cantonese/Chinese Text to Speech based on statistical parametric speech 
synthesis using merlin toolkit

This is only a demo of mandarin frontend which is lack of some parts like "text normalization" and "prosody prediction", and the phone set && Question Set this project use have not fully tested yet.

## How To Reproduce
1. First, you need data contain wav and txt (prosody mark is optional)
2. Second, generate HTS label using this project 
3. Using [merlin/egs/mandarin_voice](https://github.com/CSTR-Edinburgh/merlin/tree/master/egs/cantonese_voice) to train and generate Cantonese Voice

## Context related annotation & Question Set
* [Context related annotation](https://github.com/Jackiexiao/MTTS/blob/master/misc/mandarin_label.md)
* [Question Set](https://github.com/Jackiexiao/MTTS/blob/master/misc/questions-mandarin.hed)
* [Rules to design a Question Set](https://github.com/Jackiexiao/MTTS/blob/master/docs/mddocs/question.md)

## Install
Python : python3.6  
System: linux(tested on ubuntu16.04)  
```
sudo apt-get install libatlas3-base
```
Run `bash tools/install_mtts.sh`  
**Or** download file by yourself
* Download [montreal-forced-aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.0/montreal-forced-aligner_linux.tar.gz) and unzip to directory tools/  

**Run Demo**
```
bash run_demo.sh
```
## Usage
### 1. Generate HTS Label by wav and text
* Usage: Run `python src/mtts.py txtfile wav_directory_path output_directory_path` (Absolute path or relative path) Then you will get HTS label, if you have your own acoustic model trained by monthreal-forced-aligner, add`-a your_acoustic_model.zip`, otherwise, this project use thchs30.zip acoustic model as default
* Attention: Currently only support Chinese Character, txt should not have any
    Arabia number or English alphabet(不可包含阿拉伯数字和英文字符)

**txtfile example**
```
A_01 这是一段文本
A_02 这是第二段文本
```
**wav_directory example**(Sampleing Rate should larger than 16khz)
```
A_01.wav  
A_02.wav  
```

### 2. Generate HTS Label by text with or without alignment file
* Usage: Run `python src/mandarin_frontend.py txtfile output_directory_path` 
* or import mandarin_frontend
```
from mandarin_frontend import txt2label

result = txt2label('向香港特别行政区同胞澳门和台湾同胞海外侨胞')
[print(line) for line in result]

```
see [source
code](https://github.com/Jackiexiao/MTTS/blob/master/src/mandarin_frontend.py) for more information, but pay attention to the alignment file(sfs file), the format is `endtime phone_type` not `start_time, phone_type`(which is different from speech ocean's data)

### 3. Forced-alignment
This project use [Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) to do forced alignment, if you want to get a better alignment, use your data to train a alignment-model, see [mfa: algin-using-only-the-dataset](https://montreal-forced-aligner.readthedocs.io/en/latest/aligning.html#align-using-only-the-data-set)
1. We trained the acoustic model on our dataset.
2. If you want to use mfa's (montreal-forced-aligner) pre-trained mandarin model, this is the dictionary you need [mandarin-for-montreal-forced-aligner-pre-trained-model.lexicon](https://github.com/Jackiexiao/MTTS/blob/master/misc/mandarin-for-montreal-forced-aligner-pre-trained-model.lexicon)

## Prosody Mark
You can generate HTS Label without prosody mark. we assume that word segment is
smaller than prosodic word(which is adjusted in code)

## Improvement to be done in future
* Text Normalization
* Better Chinese word segment
* G2P: Polyphone Problem
* Better Label format and Question Set
* Improvement of prosody analyse
* Better alignment

## Contributor
* miran899
