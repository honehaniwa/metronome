# メトロノーム音声生成ツール

[![CI](https://github.com/honehaniwa/metronome/actions/workflows/ci.yml/badge.svg)](https://github.com/honehaniwa/metronome/actions/workflows/ci.yml)
[![Build](https://github.com/honehaniwa/metronome/actions/workflows/build.yml/badge.svg)](https://github.com/honehaniwa/metronome/actions/workflows/build.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

BPM可変で4つ打ちのメトロノーム音声を生成し、MP3ファイルとして保存するPythonアプリケーションです。

## 機能

- **BPMを自由に設定可能**（20〜300）
- **4つ打ちパターン**（1拍目にアクセント付き）
- **可変長の音声生成**（10秒〜10分）
- **MP3形式で保存**
- **GUI/CUIの両方に対応**
- **簡単操作**

## 必要な環境

- Python 3.9以上
- uv（パッケージマネージャー）
- ffmpeg（MP3エンコードに必要）

### uvのインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

または

```bash
pip install uv
```

### ffmpegのインストール

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt-get install ffmpeg
```

#### Windows
[ffmpegの公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストール

## セットアップ

1. リポジトリをクローン：
```bash
git clone <repository-url>
cd metronome
```

2. 依存パッケージをインストール：
```bash
uv sync
```

## 使い方

### GUIモード（推奨）

グラフィカルインターフェースで直感的に操作できます：

```bash
uv run python gui_app.py
```

GUIでは以下の設定が可能です：
- **BPM**: 数値入力またはスライダーで20〜300まで調整可能
- **長さ**: 10秒〜600秒（10分）
- **サンプリングレート**: 22050/44100/48000 Hz
- **リズムパターン**: 4beat（4つ打ち）/ 4to8（4→8パターン）
- **出力ファイル名**: 参照ボタンで保存先を選択

### CUIモード（コマンドライン）

ターミナルから直接実行：

```bash
# 基本的な使用方法（BPM 120、60秒）
uv run python -m src.metronome.cli --bpm 120

# カスタムファイル名で保存
uv run python -m src.metronome.cli --bpm 140 --output my_practice.mp3

# 長さを指定（30秒）
uv run python -m src.metronome.cli -b 100 --duration 30 -o short.mp3
```

### コマンドラインオプション

- `-b`, `--bpm`: テンポ（Beats Per Minute）**必須**
  - 範囲: 20〜300
  - 例: 60, 120, 140, 180

- `-o`, `--output`: 出力ファイル名（オプション）
  - デフォルト: `metronome_bpmXXX_1min.mp3`
  - 拡張子を省略すると自動的に`.mp3`が付加されます

- `--duration`: 音声の長さ（秒）（オプション）
  - デフォルト: 60秒
  - 範囲: 10〜600秒

- `--sample-rate`: サンプリングレート（オプション）
  - デフォルト: 44100 Hz
  - 選択肢: 22050, 44100, 48000

- `--pattern`: リズムパターン（オプション）
  - デフォルト: 4beat
  - 選択肢:
    - `4beat`: 通常の4つ打ち
    - `4to8`: 4つ打ち2小節→8つ打ち1小節を繰り返し（12拍1サイクル）

### 使用例

```bash
# BPM 60で30秒のスローな練習用
uv run python -m src.metronome.cli -b 60 --duration 30

# BPM 180で2分のハイテンポ
uv run python -m src.metronome.cli -b 180 --duration 120 -o fast_practice.mp3

# BPM 120で標準的なテンポ、高品質
uv run python -m src.metronome.cli -b 120 --sample-rate 48000 -o hq_standard.mp3

# BPM 200で4→8パターン（4つ打ち2小節→8つ打ち1小節）
uv run python -m src.metronome.cli -b 200 --duration 60 --pattern 4to8 -o speed_training.mp3
```

## 仕様

- **リズムパターン**:
  - **4beat（4つ打ち）**: 通常の4つ打ちパターン
  - **4to8（4→8パターン）**: 4つ打ち2小節（8拍）→8つ打ち1小節（4拍）を繰り返し（12拍1サイクル）
- **周波数**:
  - 1拍目（頭拍）: 1600Hz（アクセント）
  - その他の拍: 800Hz（通常）
- **長さ**: 10秒〜600秒（可変）
- **音質**: 16bit, MP3 192kbps
- **サンプリングレート**: 22050/44100/48000 Hz（選択可能）
- **クリック音**: サイン波ベース
- **音の長さ**: 各クリック50ms

## プロジェクト構成

```
metronome/
├── src/
│   └── metronome/
│       ├── __init__.py       # パッケージ初期化
│       ├── core.py           # 音声生成ロジック
│       ├── io.py             # ファイル入出力
│       ├── cli.py            # コマンドラインインターフェース
│       └── gui.py            # GUIインターフェース
├── gui_app.py                # GUIアプリ起動スクリプト
├── pyproject.toml            # プロジェクト設定
└── README.md                 # このファイル
```

## ビルド（バイナリ実行ファイルの作成）

スタンドアロンの実行可能ファイルを作成できます：

```bash
./build.sh
```

ビルド後、以下の場所に実行ファイルが生成されます：

- **macOS**: `dist/Metronome.app`
  ```bash
  # アプリケーションを起動
  open dist/Metronome.app
  ```

- **Windows**: `dist/Metronome.exe`（Windowsでビルドした場合）

- **Linux**: `dist/Metronome`（Linuxでビルドした場合）

### ビルドの注意点

- ffmpegは実行時に必要です（バンドルされていません）
- 各OS用のバイナリは、そのOS上でビルドする必要があります
- アプリケーションサイズは約35MB程度です

## トラブルシューティング

### ffmpegが見つからないエラー

```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

→ ffmpegをインストールしてください（上記「ffmpegのインストール」参照）

### 音が小さい/大きい

音量は波形生成時に調整されています。必要に応じて[src/metronome/core.py](src/metronome/core.py:27)の`wave = wave * 0.5`の値を変更してください。

### 音の高さを変更したい

[src/metronome/core.py](src/metronome/core.py:6)の`frequency=1000`パラメータを変更してください。
- 高い音: 1500〜2000 Hz
- 低い音: 600〜800 Hz

### GUIが起動しない（macOS）

macOSでtkinterが動作しない場合、Pythonを再インストールしてください：
```bash
brew install python-tk@3.12
```

## 開発

開発に参加したい方は[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。

### テストの実行

```bash
# 開発用依存関係をインストール
uv sync --extra dev

# テストを実行
uv run pytest

# カバレッジ付きでテスト
uv run pytest --cov=src --cov-report=html
```

### コード品質チェック

```bash
# Ruffでリント
uv run ruff check src/ tests/

# 自動修正
uv run ruff check --fix src/ tests/
```

## CI/CD

このプロジェクトはGitHub Actionsを使用して自動化されています：

- **CI**: プッシュ・PR時に自動テスト（Python 3.9-3.12, Ubuntu/macOS/Windows）
- **Build**: タグプッシュ時に各OS用バイナリを自動ビルド・リリース

## ライセンス

MIT License
