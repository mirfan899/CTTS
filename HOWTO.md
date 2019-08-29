### Build the data for Cantonese
Convert the audios .m4a to .wav files
```shell
for entry in *.m4a
do
  filename=$(basename -- "$entry")
  filename="${filename%.*}"
  ffmpeg -i "${entry}" "${filename}.wav";
done
```

backup data
```shell
cp data/wav/*.wav backup
cp data/wav/*.m4a backup
```

Now make a temp directory and convert wav files to 16khz 16 bit wav files
```shell
mkdir wav
wav_dir=wav
for i in *.wav; do
  ffmpeg -i ${i} -acodec pcm_s16le -ac 1 -ar 16000 ${wav_dir}/${i};
done

rm *.wav
mkdir m4a
mv *.m4a m4a
```

Copy converted wav files back to original location.
```shell
cd ../temp
rm wav/*.m4a
rm wav/*.wav
cp *.wav wav/
```

### Train mfa to generate TextGrid files
I'm using `mfa_train_and_align` to generate textgrid files.
```shell
cd tools
./run_mfa.sh
```

### Build lab files
It will generate the necessary files for Merlin TTS. 
```shell
./run_cantonese.sh
```

### Build Question Set
Run following scripts to get questions for Cantonese.
```shell
python utils/c_questions.py
python utils/r_questions.py
python utils/l_questions.py
```
Copy the output of each file to question set file.
### Use frontend-tts for Ossian with Jyutping txts and wavs
### Use instance-2 for Merlin with labels and wavs.