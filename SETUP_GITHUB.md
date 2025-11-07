# GitHubリポジトリセットアップガイド

このドキュメントでは、プロジェクトをGitHubにプッシュし、CI/CDを有効化する手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- GitHubにSSHキーまたはPersonal Access Tokenを設定済みであること

## セットアップ手順

### 1. GitHubで新しいリポジトリを作成

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. 以下の情報を入力：
   - **Repository name**: `trill`（または任意の名前）
   - **Description**: BPM可変4つ打ちメトロノーム音声生成ツール
   - **Visibility**: PublicまたはPrivate
   - **Initialize this repository with**: 何もチェックしない（空のリポジトリ）
4. 「Create repository」をクリック

### 2. ローカルリポジトリをGitHubにプッシュ

```bash
# プロジェクトディレクトリに移動
cd /Users/tt/workspace/trill

# Gitの初期化（既に実行済み）
git init

# 全ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Metronome application with CI/CD"

# リモートリポジトリを追加（YOUR_USERNAMEを実際のユーザー名に置き換え）
git remote add origin git@github.com:YOUR_USERNAME/metronome.git

# または HTTPS の場合
# git remote add origin https://github.com/YOUR_USERNAME/trill.git

# デフォルトブランチ名を設定
git branch -M main

# プッシュ
git push -u origin main
```

### 3. README.mdのバッジURLを更新

`README.md`の3-6行目にあるバッジURLの`YOUR_USERNAME`を実際のGitHubユーザー名に置き換えてください：

```markdown
[![CI](https://github.com/honehaniwa/trill/actions/workflows/ci.yml/badge.svg)](https://github.com/honehaniwa/trill/actions/workflows/ci.yml)
[![Build](https://github.com/honehaniwa/trill/actions/workflows/build.yml/badge.svg)](https://github.com/honehaniwa/trill/actions/workflows/build.yml)
```

更新後、コミットしてプッシュ：

```bash
git add README.md
git commit -m "Update: GitHub badges with actual username"
git push
```

### 4. GitHub Actionsの確認

1. GitHubリポジトリページにアクセス
2. 「Actions」タブをクリック
3. CIワークフローが実行されていることを確認

初回プッシュ後、自動的にCIが実行され：
- Python 3.9, 3.10, 3.11, 3.12でテスト
- Ubuntu, macOS, Windowsでテスト
- コード品質チェック（Ruff）
- テストカバレッジ計測

### 5. リリースの作成（ビルド自動化）

バイナリを自動ビルドしてリリースを作成するには：

```bash
# バージョンタグを作成
git tag v0.1.0
git push origin v0.1.0
```

これにより、GitHub Actionsが自動的に：
1. Ubuntu, macOS, Windows用バイナリをビルド
2. GitHubリリースを作成
3. ビルドしたバイナリをアップロード

### 6. Codecov連携（オプション）

テストカバレッジをCodecovで可視化する場合：

1. [Codecov](https://codecov.io/)にサインアップ
2. GitHubリポジトリを連携
3. CodecovTokenを取得
4. GitHubリポジトリの Settings → Secrets and variables → Actions
5. 「New repository secret」をクリック
6. Name: `CODECOV_TOKEN`, Value: 取得したトークン
7. 保存

CIワークフローが自動的にカバレッジをアップロードします。

## トラブルシューティング

### GitHub Actionsが失敗する

**macOS でのビルド失敗:**
- Homebrew のffmpegインストールに時間がかかる場合があります
- 再実行すると成功することがあります

**Windows でのビルド失敗:**
- ffmpegのインストール確認
- PyInstallerの互換性確認

**テスト失敗:**
- ローカルでテストを実行して確認: `uv run pytest`
- ffmpegがインストールされているか確認

### リモートリポジトリへのプッシュができない

**認証エラー:**
```bash
# SSH設定を確認
ssh -T git@github.com

# または Personal Access Token を使用
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/trill.git
```

### Actions が実行されない

1. リポジトリの Settings → Actions → General
2. 「Actions permissions」が有効になっているか確認
3. 「Workflow permissions」で適切な権限が付与されているか確認

## 次のステップ

セットアップ完了後：

1. **README.mdを確認**: バッジが正しく表示されているか
2. **Actionsを確認**: CIが正常に動作しているか
3. **タグをプッシュ**: リリースビルドが自動実行されるか
4. **開発を継続**: [CONTRIBUTING.md](CONTRIBUTING.md)を参照

## 参考リンク

- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [PyInstaller ドキュメント](https://pyinstaller.org/)
- [pytest ドキュメント](https://docs.pytest.org/)
- [Ruff ドキュメント](https://docs.astral.sh/ruff/)
