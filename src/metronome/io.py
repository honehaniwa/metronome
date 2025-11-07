"""ファイル入出力処理"""

import os

from pydub import AudioSegment
from scipy.io import wavfile


def save_as_wav(wave_data, sample_rate, output_filename):
    """
    波形データをWAVファイルとして保存する

    Args:
        wave_data: 波形データ
        sample_rate: サンプリングレート
        output_filename: 出力ファイル名
    """
    if not output_filename.endswith(".wav"):
        output_filename += ".wav"

    wavfile.write(output_filename, sample_rate, wave_data)
    return output_filename


def save_as_mp3(wave_data, sample_rate, output_filename=None, bpm=None):
    """
    波形データをMP3ファイルとして保存する

    Args:
        wave_data: 波形データ
        sample_rate: サンプリングレート
        output_filename: 出力ファイル名
        bpm: BPM値（ファイル名に含める、オプション）

    Returns:
        str: 保存されたファイル名
    """
    # 一時的にWAVファイルとして保存
    temp_wav = "temp_metronome.wav"
    wavfile.write(temp_wav, sample_rate, wave_data)

    # WAVファイルをMP3に変換
    audio = AudioSegment.from_wav(temp_wav)

    # ファイル名にBPMを含める
    if not output_filename:
        if bpm:
            output_filename = f"metronome_bpm{bpm}_1min.mp3"
        else:
            output_filename = "metronome_1min.mp3"
    elif not output_filename.endswith(".mp3"):
        output_filename += ".mp3"

    # MP3として保存
    audio.export(output_filename, format="mp3", bitrate="192k")

    # 一時ファイルを削除
    os.remove(temp_wav)

    return output_filename
