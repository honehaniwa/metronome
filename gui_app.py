#!/usr/bin/env python3
"""GUIアプリケーションのエントリーポイント"""

import sys

try:
    from src.metronome.gui import main
except ImportError as e:
    if "tkinter" in str(e) or "_tkinter" in str(e):
        print("エラー: tkinterがインストールされていません。")
        print("\nmacOSの場合:")
        print("  brew install python-tk@3.12")
        print("\nUbuntu/Debianの場合:")
        print("  sudo apt-get install python3-tk")
        print("\nまたは、CUIモードを使用してください:")
        print("  uv run python -m src.metronome.cli --bpm 120")
        sys.exit(1)
    else:
        raise

if __name__ == "__main__":
    main()
