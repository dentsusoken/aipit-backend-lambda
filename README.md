# 📦 localstack-app-devcontainer

[LocalStack](https://github.com/localstack/localstack) を [Dev Containers](https://containers.dev/) 上で構築し、AWS環境をローカルでエミュレーション・開発・テストできるテンプレートリポジトリです。

---

## ✅ 特長

- LocalStack（Pro対応可）による AWS サービスのエミュレーション
- Lambda、API Gateway、DynamoDB のローカル検証
- VS Code Dev Container による即時開発環境構築
- Python フォーマッタ・Linter（black, flake8, isort, mypy）を標準搭載

---

## 🛠️ セットアップ手順

### 1. クローン

```bash
git clone https://github.com/fcf-koga/localstack-app-devcontainer.git
cd localstack-app-devcontainer
```

### 2. Dev Container で開く（VS Code）
VS Code 上でコマンドパレットを開き、以下を実行します。
```yaml
Dev Containers: Reopen in Container
```
初回起動時に `requirements-dev.txt` のパッケージがインストールされます。

### 3.LocalStack 起動確認
```bash
curl http://localhost:4566/_localstack/health
```

## 📁 ディレクトリ構成
```bash
.
├── .devcontainer/           # DevContainer 設定
│   └── devcontainer.json
├── docker-compose.yml       # LocalStack サービス定義
├── requirements-dev.txt     # Python 開発ツール（Linterなど）
├── .editorconfig
├── .dockerignore
├── .gitattributes

```

## 🧪 開発用コマンド
```bash
# フォーマット
black .

# import 整理
isort .

# Lint
flake8 .

# 型チェック
mypy .
```

## 📦 使用技術
- LocalStack
- Docker / Docker Compose
- Dev Containers (VS Code)
- Python 3.11+
- black / isort / flake8 / mypy