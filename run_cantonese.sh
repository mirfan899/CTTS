#!/usr/bin/env bash

demo_voice=cantonese_demo
data_dir=data
demo_voice_path=${data_dir}/${demo_voice}

#mkdir -p $data_dir
python src/mtts.py ${demo_voice_path}/cantonese_utts.txt ${demo_voice_path}/wav ${demo_voice_path}/output