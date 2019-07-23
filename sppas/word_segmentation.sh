#!/usr/bin/env bash


working_dir=$("pwd")
txt_dir=$working_dir/txt/

echo $working_dir
for entry in "$txt_dir"*.txt
do
  filename=$(basename -- "$entry")
  extension="${filename##*.}"
  filename="${filename%.*}"
#  filename="${filename%.*}"
#  echo $extension
#  echo $filename
#  fname=`basename $entry`
#  echo "$fname"
  python $working_dir/sppas/bin/normalize.py -i "$entry" -o $working_dir/output/$filename.csv -r $working_dir/resources/vocab/yue.vocab

done