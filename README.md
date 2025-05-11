# 📦 localstack-app-devcontainer

[LocalStack](https://github.com/localstack/localstack) を [Dev Containers](https://containers.dev/) 上で構築し、AWS環境をローカルでエミュレーション・開発・テストできるテンプレートリポジトリです。

---

## ✅ 特長

- LocalStack（Pro対応可）による AWS サービスのローカルエミュレーション
- Lambda, API Gateway, DynamoDB などをコンテナ内で検証可能
- VS Code Dev Container に対応：ワンクリックで開発環境を構築
- `black`, `isort`, `flake8`, `mypy`, `pytest`, `pre-commit` による高品質な Python 開発体験
- `TypedDict` による型安全な CloudFormation 出力ハンドリング
- `aws-lambda-typing` による Lambda イベントの型補完
- `types/` ディレクトリで型定義を一元管理（実装と分離）

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
├── src/                     # Lambdaアプリケーションコード
│   └── hello_world/
│       └── app.py
├── types/                   # TypedDict による型定義
│   ├── cloudformation.py    # CloudFormation describe_stacks の型
│   └── lambda_events.py     # Lambdaのレスポンス型
├── tests/                   # テストコード
│   ├── unit/
│   ├── integration/
│   └── conftest.py          # 共通fixture + 型安全fixture
├── .pre-commit-config.yaml  # pre-commitフック設定
├── .devcontainer/
│   └── devcontainer.json
├── requirements-dev.txt
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
mypy src tests types

# テスト実行
pytest
pre-commit run --all-files
```

## 🔐 型定義の使用例
```python
# src/hello_world/app.py
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.context import Context
from types.lambda_events import LambdaResponse

def handler(event: APIGatewayProxyEventV2, context: Context) -> LambdaResponse:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"message": "hello world"}'
    }
```

## 📦 使用技術
- LocalStack
- Docker / Docker Compose
- Dev Containers (VS Code)
- Python 3.11+
- black / isort / flake8 / mypy