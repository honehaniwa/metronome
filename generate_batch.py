#!/usr/bin/env python3
"""
BPM範囲のメトロノームファイルを一括生成するスクリプト
"""

from src.metronome.core import generate_metronome
from src.metronome.io import save_as_mp3


def generate_batch_metronomes(start_bpm, end_bpm, step=10, duration=60, sample_rate=44100):
    """
    指定範囲のBPMでメトロノームファイルを一括生成

    Args:
        start_bpm: 開始BPM
        end_bpm: 終了BPM
        step: BPMの刻み幅
        duration: 各ファイルの長さ（秒）
        sample_rate: サンプリングレート
    """
    bpm_list = range(start_bpm, end_bpm + 1, step)
    total = len(list(bpm_list))

    print(f"BPM {start_bpm}〜{end_bpm} ({step}刻み) のメトロノームを生成します")
    print(f"合計: {total}ファイル")
    print(f"各ファイルの長さ: {duration}秒\n")

    generated_files = []

    for idx, bpm in enumerate(bpm_list, 1):
        print(f"[{idx}/{total}] BPM {bpm} を生成中...")

        # メトロノーム音声を生成
        wave_data = generate_metronome(
            bpm=bpm,
            duration_seconds=duration,
            sample_rate=sample_rate
        )

        # ファイル名を生成
        output_file = f"metronome_bpm{bpm:03d}_1min.mp3"

        # MP3として保存
        save_as_mp3(wave_data, sample_rate, output_file, bpm)

        generated_files.append(output_file)
        print(f"  ✓ {output_file}")

    print(f"\n完了！{total}個のファイルを生成しました:")
    for file in generated_files:
        print(f"  - {file}")


def main():
    """メイン処理"""
    # BPM 190〜270を10刻みで生成
    generate_batch_metronomes(
        start_bpm=190,
        end_bpm=270,
        step=10,
        duration=60,
        sample_rate=44100
    )


if __name__ == "__main__":
    main()
