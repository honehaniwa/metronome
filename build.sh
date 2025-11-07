#!/bin/bash
# メトロノームアプリのビルドスクリプト

set -e

echo "メトロノームアプリをビルドしています..."

# クリーンアップ
echo "1. 前回のビルドをクリーンアップ..."
rm -rf build dist

# PyInstallerでビルド
echo "2. PyInstallerでビルド中..."
uv run pyinstaller metronome.spec

echo ""
echo "✓ ビルド完了！"
echo ""
echo "macOS用アプリケーション:"
echo "  dist/Metronome.app"
echo ""
echo "実行方法:"
echo "  open dist/Metronome.app"
echo ""
