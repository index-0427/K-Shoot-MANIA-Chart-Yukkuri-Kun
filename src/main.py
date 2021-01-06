# -*- coding: utf-8 -*-

import glob
import os 
import subprocess
import sys
import module_oggcontroller

if len(sys.argv) != 3:
    print("倍率を指定してください。")
    print("例：py main.py ./hogehoge.ogg 0.8")
    exit()

score_speed_rate = str(sys.argv[1])
input_audio_file = str(sys.argv[2])
# input_score_file = str(sys.argv[3])

target_audio_file = "./export/output.ogg"

print(score_speed_rate)

cmd1 = "ffmpeg -i " \
    + input_audio_file \
    + " -vf setpts=PTS/" \
    + score_speed_rate \
    + " -af atempo=" \
    + score_speed_rate \
    + " " \
    + target_audio_file

subprocess.call(cmd1)