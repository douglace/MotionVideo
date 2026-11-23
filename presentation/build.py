#!/usr/bin/env python3
"""Montage "La présentation" : 6 images + clips voix -> MP4 1080x1920. Durées calées sur l'audio."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FPS, TEMPO, PAD = 30, 1.2, 0.25

def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def run(cmd): subprocess.run(cmd, check=True)

# scène -> (clips audio, zoom, [(fichier légende, clip index dont on affiche pendant)] )
scenes = [
  dict(img="g1", clips=["a1"], zoom="in"),
  dict(img="g2", clips=["a2"], zoom="in"),
  dict(img="g3", clips=["a3"], zoom="in"),
  dict(img="g4", clips=["a4"], zoom="out"),
  dict(img="g5", clips=["a5"], zoom="in"),
  dict(img="g6", clips=["a6l","a6e"], zoom="out"),
]
caps = {"a1":"caps_1.txt","a2":"caps_2.txt","a3":"caps_3.txt","a4":"caps_4.txt","a5":"caps_5.txt","a6l":"caps_6a.txt","a6e":"caps_6b.txt"}

os.makedirs("build", exist_ok=True)
# 1) accélérer légèrement les voix
for c in {c for s in scenes for c in s["clips"]}:
    run(["ffmpeg","-v","error","-y","-i",f"{c}.wav","-af",f"atempo={TEMPO}","build/%s_t.wav"%c])

# 2) timeline : début/fin de chaque clip et de chaque scène
t = 0.0; caption_windows = []; scene_len = []; audio_parts = []
for i, s in enumerate(scenes):
    start = t
    for c in s["clips"]:
        d = dur(f"build/{c}_t.wav")
        caption_windows.append((caps[c], t, t + d + PAD))
        audio_parts.append((c, t))
        t += d + PAD
    if i == len(scenes) - 1: t += 1.0      # tenue finale sur la chute
    scene_len.append(t - start)
total = t

# 3) piste audio : chaque clip placé à son début
ain = []; amix = ""
for k, (c, st) in enumerate(audio_parts):
    ain += ["-i", f"build/{c}_t.wav"]
    amix += f"[{k+len(scenes)}:a]adelay={int(st*1000)}|{int(st*1000)}[d{k}];"
amix += "".join(f"[d{k}]" for k in range(len(audio_parts))) + f"amix=inputs={len(audio_parts)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]"

# 4) vidéo : zoompan par scène (1 image en entrée), concat, légendes
filt = ""; vin = []
for i, s in enumerate(scenes):
    frames = int(round(scene_len[i] * FPS))
    z = "min(1.0+0.0007*on,1.12)" if s["zoom"] == "in" else "max(1.12-0.0007*on,1.0)"
    vin += ["-i", f"{s['img']}.png"]
    filt += f"[{i}:v]scale=2160:-1,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},setsar=1[v{i}];"
filt += "".join(f"[v{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=1:a=0[vc0];"
label = "vc0"
dt = f"fontfile={FONT}:borderw=6:bordercolor=black:fontcolor=white"
filt += f"[{label}]drawtext={dt}:textfile=hook.txt:fontsize=58:line_spacing=10:x=(w-text_w)/2:y=150[h];"
label = "h"
for j, (f, a, b) in enumerate(caption_windows):
    filt += f"[{label}]drawtext={dt}:textfile={f}:fontsize=44:line_spacing=12:x=(w-text_w)/2:y=1560:enable='between(t,{a:.2f},{b:.2f})'[c{j}];"
    label = f"c{j}"
filt += amix
run(["ffmpeg","-v","error","-y",*vin,*ain,"-filter_complex",filt,"-map",f"[{label}]","-map","[aout]",
     "-t",f"{total:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-b:a","192k",
     "-movflags","+faststart","build/la-presentation.mp4"])
print("durée", round(total,1), "s")
