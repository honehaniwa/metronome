# 開発ガイド

## 開発環境のセットアップ

### 必要なツール

- Python 3.9以上
- uv（パッケージマネージャー）
- ffmpeg
- Git

### セットアップ手順

1. リポジトリをクローン：
```bash
git clone <repository-url>
cd trill
```

2. 依存パッケージをインストール（開発用含む）：
```bash
uv sync --extra dev
```

3. ffmpegをインストール：
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## 開発ワークフロー

### テストの実行

```bash
# 全テストを実行
uv run pytest

# カバレッジレポート付き
uv run pytest --cov=src --cov-report=html

# 特定のテストファイルのみ
uv run pytest tests/test_core.py

# 詳細出力
uv run pytest -v
```

### リンター（コード品質チェック）

```bash
# コードチェック
uv run ruff check src/ tests/

# 自動修正
uv run ruff check --fix src/ tests/

# フォーマット
uv run ruff format src/ tests/
```

### ローカルビルド

```bash
# macOS用アプリをビルド
./build.sh

# または手動で
uv run pyinstaller metronome.spec
```

## コード規約

- **Line length**: 100文字まで
- **Import順序**: 標準ライブラリ → サードパーティ → ローカル
- **命名規則**:
  - 関数/変数: `snake_case`
  - クラス: `PascalCase`
  - 定数: `UPPER_CASE`
- **型ヒント**: 推奨（必須ではない）
- **Docstring**: 公開API関数には必須

## テストの書き方

新機能を追加する際は、必ずテストを書いてください：

```python
# tests/test_feature.py
import pytest
from src.metronome.feature import new_function

def test_new_function():
    """Test description"""
    result = new_function(input_data)
    assert result == expected_output
```

### テストカバレッジ

- 目標: 80%以上
- コアロジック（`src/metronome/core.py`）: 100%

## プルリクエスト

1. 新しいブランチを作成：
```bash
git checkout -b feature/your-feature-name
```

2. 変更をコミット：
```bash
git add .
git commit -m "Add: 新機能の説明"
```

コミットメッセージプレフィックス：
- `Add:` 新機能追加
- `Fix:` バグ修正
- `Update:` 既存機能の改善
- `Refactor:` リファクタリング
- `Docs:` ドキュメント更新
- `Test:` テスト追加・修正

3. テストとリンターを実行：
```bash
uv run pytest
uv run ruff check src/ tests/
```

4. プッシュしてPRを作成：
```bash
git push origin feature/your-feature-name
```

## CI/CD

GitHub Actionsが以下を自動実行します：

### CI（Pull Request時）
- Python 3.9, 3.10, 3.11, 3.12でテスト
- Ubuntu, macOS, Windowsでテスト
- Ruffによるコード品質チェック
- テストカバレッジ計測

### ビルド（タグプッシュ時）
- 各OS用バイナリの自動ビルド
- GitHubリリースへの自動アップロード

## リリースプロセス

1. バージョン番号を更新（`pyproject.toml`）
2. CHANGELOGを更新
3. タグを作成してプッシュ：
```bash
git tag v0.1.0
git push origin v0.1.0
```

4. GitHub Actionsが自動的にビルドしてリリース作成

## 質問やサポート

- Issue: バグ報告や機能リクエスト
- Discussion: 質問や議論
- Pull Request: コード貢献

## ライセンス

MIT License
