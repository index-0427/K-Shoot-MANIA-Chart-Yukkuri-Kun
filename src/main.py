# -*- coding: utf-8 -*-

import glob
import os 
import subprocess
import sys
import re

if len(sys.argv) != 4:
    print("倍率を指定してください。")
    print("例：py main.py 0.8 ./hoge.ogg ./hoge_IN.ksh")
    exit()

# コマンドライン入力値
score_speed_rate = str(sys.argv[1])
input_audio_file_path = str(sys.argv[2])
input_chart_file_path = str(sys.argv[3])

# 出力先指定
output_audio_file_path = "./export/" + os.path.basename(input_audio_file_path)
output_chart_file_path = "./export/" + os.path.basename(input_chart_file_path)

## 譜面速度変更
# ファイルオープン
with open(input_chart_file_path, 'r') as f:
    input_chart = f.read()

# t=XXXの一覧を取得
previous_tempos = re.findall(r'^t=[\d.]+$', input_chart, re.MULTILINE)

# テンポ計算
after_tempos = []

for i in previous_tempos:
    print(i)
    tempo = float(re.search(r'[\d.]+$',i).group())
    after_tempos.append("t=" + str(tempo*float(score_speed_rate)))

print(after_tempos)

# テンポ置換
output_chart = input_chart
for previous_tempo,after_tempo in zip(previous_tempos, after_tempos):
    regex_string = r"^" + previous_tempo + r"$"
    output_chart = re.sub(regex_string, after_tempo, output_chart, flags=re.MULTILINE)

# ファイル出力
with open(output_chart_file_path, 'w') as f:
    f.write(output_chart)

## oggファイル書き出し
cmd1 = "ffmpeg -i " \
    + input_audio_file_path \
    + " -vf setpts=PTS/" \
    + score_speed_rate \
    + " -af atempo=" \
    + score_speed_rate \
    + " " \
    + output_audio_file_path

subprocess.call(cmd1)