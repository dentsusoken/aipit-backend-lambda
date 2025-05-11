# 📦 localstack-app-devcontainer

[LocalStack](https://github.com/localstack/localstack) を [Dev Containers](https://containers.dev/) 上で構築し、AWS環境をローカルでエミュレーション・開発・テストできるテンプレートリポジトリです。

---

## ✅ 特長

- LocalStack（Pro対応可）による AWS サービスのローカルエミュレーション
- Lambda, API Gateway, DynamoDB などをコンテナ内で検証可能
- VS Code Dev Container に対応：ワンクリックで開発環境を構築
- Python 開発者向けに以下の Lint/型チェックツールを標準搭載：
  - `black`, `isort`, `flake8`, `mypy`, `pytest`, `types-requests`

---

## 🛠️ セットアップ手順

### 1. このリポジトリをクローン

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
├── .devcontainer/           # DevContainer 設定（VS Code用）
│   └── devcontainer.json
├── docker-compose.yml       # LocalStack 含むサービス定義
├── requirements-dev.txt     # 開発用パッケージ
├── src/                     # アプリケーションコード
│   └── hello_world/
├── tests/                   # テストコード（unit/integration）
├── .editorconfig
├── .gitattributes
├── .dockerignore
└── README.md
```

## 🧪 開発用コマンド
```bash
# フォーマット
black .

# import 整理
isort .

# Lint チェック
flake8 .

# 型チェック
mypy src tests

# テスト実行
pytest
```

## 📦 使用技術
- LocalStack
- Docker / Docker Compose
- Dev Containers (VS Code)
- Python 3.11+
- black / isort / flake8 / mypy