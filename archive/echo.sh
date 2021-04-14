#!/bin/bash
echo $1
opdate=$(date '+%Y-%m-%d')
mkdir -p ~/highlights/$opdate
INPUT=$1

youtube-dl $1 -o "~/highlights/$opdate/%(title)s.%(ext)s" --restrict-filenames -f HTTP_CLOUD_MOBILE-221 --no-check-certificate
s=$(ls -t ~/highlights/$opdate | head -1)
filename="$(b=${s##*/}; echo ${b%.*})"
#echo $filename
i=$((${#filename}-10))
#echo ${filename:$i:10}
if [[ ${filename:$i:10} = "HIGHLIGHTS" ]]; then
        :
else
        ffmpeg -ss 0:0:1.2 -i ~/highlights/$opdate/$s -filter:v fps=fps=30 -maxrate 2000k -bufsize 1835k ~/highlights/$opdate/$filename-HIGHLIGHTS.mp4
        rm ~/highlights/$opdate/$s
fi
#echo $s
#ffmpeg -ss 0:0:1.2 -i ~/highlights/$opdate/$s -filter:v fps=fps=30 -maxrate 2000k -bufsize 1835k ~/highlights/$opdate/$filename-HIGHLIGHTS.mp4
#rm ~/highlights/$opdate/$s