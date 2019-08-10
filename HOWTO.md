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
mkdir ../temp
temp_dir=../temp
for i in *.wav; do
  ffmpeg -i ${i} -acodec pcm_s16le -ac 1 -ar 16000 ${temp_dir}/${i};
done
```

Copy converted wav files back to original location.
```shell
cd ../temp
rm wav/*.m4a
rm wav/*.wav
cp *.wav wav/
```