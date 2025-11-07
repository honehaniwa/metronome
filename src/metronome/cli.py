"""コマンドラインインターフェース"""

import argparse
from .core import generate_metronome
from .io import save_as_mp3


def main():
    """メインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description='4つ打ちメトロノーム音声生成ツール',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  uv run python -m metronome.cli --bpm 120
  uv run python -m metronome.cli --bpm 140 --output my_metronome.mp3
  uv run python -m metronome.cli -b 100 -o practice.mp3
        """
    )

    parser.add_argument(
        '-b', '--bpm',
        type=int,
        required=True,
        help='テンポ（Beats Per Minute）例: 120'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='出力ファイル名（デフォルト: metronome_bpmXXX_1min.mp3）'
    )

    parser.add_argument(
        '--sample-rate',
        type=int,
        default=44100,
        help='サンプリングレート（デフォルト: 44100 Hz）'
    )

    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='音声の長さ（秒）（デフォルト: 60秒）'
    )

    parser.add_argument(
        '--pattern',
        type=str,
        default='4beat',
        choices=['4beat', '4to8'],
        help='リズムパターン（デフォルト: 4beat）\n'
             '4beat: 通常の4つ打ち\n'
             '4to8: 4つ打ち2小節→8つ打ち1小節（12拍1サイクル）'
    )

    args = parser.parse_args()

    # BPMの妥当性チェック
    if args.bpm < 20 or args.bpm > 300:
        print("警告: BPMは通常20〜300の範囲です")

    pattern_name = "4つ打ち" if args.pattern == "4beat" else "4→8パターン"

    print(f"メトロノーム音声を生成中...")
    print(f"  BPM: {args.bpm}")
    print(f"  長さ: {args.duration}秒")
    print(f"  パターン: {pattern_name}")
    print(f"  サンプリングレート: {args.sample_rate} Hz")

    # メトロノーム音声を生成
    wave_data = generate_metronome(
        bpm=args.bpm,
        duration_seconds=args.duration,
        sample_rate=args.sample_rate,
        pattern=args.pattern
    )

    # MP3として保存
    output_file = save_as_mp3(wave_data, args.sample_rate, args.output, args.bpm)

    print(f"\n✓ メトロノーム音声を保存しました: {output_file}")
    print(f"  - BPM: {args.bpm}")
    print(f"  - 長さ: {args.duration}秒")
    print(f"  - パターン: {pattern_name}")


if __name__ == "__main__":
    main()
