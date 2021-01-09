# -*- coding: utf-8 -*-

import glob
import os 
import subprocess
import sys
import re
import pathlib
import module_path

# コマンドライン入力値
chart_speed_rate = str(sys.argv[1])

# ルートパス取得
PROJECT_ROOT_PATH:pathlib.Path = module_path.get_project_path()
IMPORT_DIR_PATH:pathlib.Path = PROJECT_ROOT_PATH / 'import'
EXPORT_DIR_PATH:pathlib.Path = PROJECT_ROOT_PATH / 'export'

# import/exportディレクトリの存在判定
if not IMPORT_DIR_PATH.exists():
    print('[INFO]:IMPORTディレクトリがありません。実行ファイルと同階層に空のIMPORTディレクトリを作成します。')
    IMPORT_DIR_PATH.mkdir()
if not EXPORT_DIR_PATH.exists():
    print('[INFO]:IMPORTディレクトリがありません。実行ファイルと同階層に空のIMPORTディレクトリを作成します。')
    EXPORT_DIR_PATH.mkdir()

# input内のファイル一覧を取得
input_audio_file_paths:list = []
input_chart_file_paths:list = []

for input_file in os.listdir(IMPORT_DIR_PATH):
    base, ext = os.path.splitext(input_file)
    if ext == ".ogg":
        input_audio_file_paths.append(IMPORT_DIR_PATH / input_file)
    elif ext == ".ksh":
        input_chart_file_paths.append(IMPORT_DIR_PATH / input_file)

## 譜面速度変更
for input_chart_file_path in input_chart_file_paths:
    output_chart_file_path = EXPORT_DIR_PATH / input_chart_file_path.name
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
        after_tempos.append("t=" + str(tempo*float(chart_speed_rate)))

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
for input_audio_file_path in input_audio_file_paths:
    output_audio_file_path:pathlib.Path = EXPORT_DIR_PATH / input_audio_file_path.name

    cmd = "ffmpeg -i " \
        + str(input_audio_file_path) \
        + " -vf setpts=PTS/" \
        + chart_speed_rate \
        + " -af atempo=" \
        + chart_speed_rate \
        + " " \
        + str(output_audio_file_path)

    subprocess.call(cmd)