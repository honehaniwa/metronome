#!/usr/bin/env python3
"""
BPM範囲のメトロノームファイルを一括生成するスクリプト
パターンごとにディレクトリを分けて保存
"""

import os
from pathlib import Path
from src.metronome.core import generate_metronome
from src.metronome.io import save_as_mp3


def generate_batch_metronomes(start_bpm, end_bpm, step=10, duration=60, sample_rate=44100, pattern="4beat", output_dir="mp3"):
    """
    指定範囲のBPMでメトロノームファイルを一括生成

    Args:
        start_bpm: 開始BPM
        end_bpm: 終了BPM
        step: BPMの刻み幅
        duration: 各ファイルの長さ（秒）
        sample_rate: サンプリングレート
        pattern: リズムパターン（"4beat" or "4to8"）
        output_dir: 出力ディレクトリ
    """
    bpm_list = range(start_bpm, end_bpm + 1, step)
    total = len(list(bpm_list))

    pattern_name = "4つ打ち" if pattern == "4beat" else "4→8パターン"

    print(f"\n{'='*60}")
    print(f"BPM {start_bpm}〜{end_bpm} ({step}刻み) のメトロノームを生成します")
    print(f"パターン: {pattern_name}")
    print(f"合計: {total}ファイル")
    print(f"各ファイルの長さ: {duration}秒")
    print(f"出力先: {output_dir}/")
    print(f"{'='*60}\n")

    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for idx, bpm in enumerate(bpm_list, 1):
        print(f"[{idx}/{total}] BPM {bpm} を生成中...", end=" ", flush=True)

        try:
            # メトロノーム音声を生成
            wave_data = generate_metronome(
                bpm=bpm,
                duration_seconds=duration,
                sample_rate=sample_rate,
                pattern=pattern
            )

            # ファイル名を生成
            output_file = output_path / f"metronome_bpm{bpm:03d}_60sec.mp3"

            # MP3として保存
            save_as_mp3(wave_data, sample_rate, str(output_file), bpm)

            generated_files.append(str(output_file))
            print(f"✓ 完了")

        except Exception as e:
            print(f"✗ エラー: {e}")

    print(f"\n{'='*60}")
    print(f"完了！{len(generated_files)}/{total}個のファイルを生成しました")
    print(f"出力先: {output_dir}/")
    print(f"{'='*60}\n")

    return generated_files


def main():
    """メイン処理"""
    print("\n" + "="*60)
    print("メトロノーム音声一括生成ツール")
    print("="*60)

    # BPM 160〜300を10刻みで生成
    start_bpm = 160
    end_bpm = 300
    step = 10
    duration = 60
    sample_rate = 44100

    # 4beatパターンを生成
    print("\n【1/2】4beatパターンを生成中...")
    generate_batch_metronomes(
        start_bpm=start_bpm,
        end_bpm=end_bpm,
        step=step,
        duration=duration,
        sample_rate=sample_rate,
        pattern="4beat",
        output_dir="mp3/4beat"
    )

    # 4to8パターンを生成
    print("\n【2/2】4to8パターンを生成中...")
    generate_batch_metronomes(
        start_bpm=start_bpm,
        end_bpm=end_bpm,
        step=step,
        duration=duration,
        sample_rate=sample_rate,
        pattern="4to8",
        output_dir="mp3/4to8"
    )

    print("\n" + "="*60)
    print("全ての生成が完了しました！")
    print("="*60)
    print("\n出力ディレクトリ:")
    print("  mp3/4beat/  - 4つ打ちパターン")
    print("  mp3/4to8/   - 4→8パターン")
    print()


if __name__ == "__main__":
    main()
