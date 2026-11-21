#!/usr/bin/env bash
# Montage "Fais comme tu veux" : 6 images clés + dialogue -> MP4 1080x1920
set -euo pipefail
cd "$(dirname "$0")"
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
FPS=30
# image  durée(s)  zoom (in|out)
SCENES=("s1 3.5 in" "s2 5.5 in" "s3 4.7 in" "s4 3.8 out" "s5 2.1 in" "s6 3.0 out")
mkdir -p build
inputs=(); filt=""; i=0
for sc in "${SCENES[@]}"; do
  set -- $sc; img=$1; dur=$2; dir=$3
  frames=$(awk "BEGIN{printf \"%d\", $dur*$FPS}")
  if [ "$dir" = in ]; then z="min(1.0+0.0007*on,1.12)"; else z="max(1.12-0.0007*on,1.0)"; fi
  inputs+=(-i "assets/$img.png")
  filt+="[$i:v]scale=2160:-1,zoompan=z='$z':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$frames:s=1080x1920:fps=$FPS,setsar=1[v$i];"
  i=$((i+1))
done
cat_in=""; for ((k=0;k<i;k++)); do cat_in+="[v$k]"; done
filt+="${cat_in}concat=n=$i:v=1:a=0[vc];"
filt+="[vc]drawtext=fontfile=$FONT:textfile=assets/hook.txt:fontsize=58:fontcolor=white:borderw=6:bordercolor=black:x=(w-text_w)/2:y=150[vout]"
ffmpeg -v error -y "${inputs[@]}" -i assets/dialogue.wav -filter_complex "$filt" \
  -map "[vout]" -map "$i:a" -af "apad,loudnorm=I=-16:TP=-1.5" -c:v libx264 -pix_fmt yuv420p -crf 18 \
  -c:a aac -b:a 192k -shortest -movflags +faststart build/fais-comme-tu-veux.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 build/fais-comme-tu-veux.mp4
