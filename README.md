# 📦 localstack-app-devcontainer

[LocalStack](https://github.com/localstack/localstack) を [Dev Containers](https://containers.dev/) 上で構築し、AWS環境をローカルでエミュレーション・開発・テストできるテンプレートリポジトリです。

---

## ✅ 特長

- LocalStack（Pro対応可）による AWS サービスのローカルエミュレーション
- Lambda, API Gateway, SQS などをコンテナ内で検証可能
- VS Code Dev Container に対応：ワンクリックで開発環境を構築
- `black`, `isort`, `flake8`, `mypy`, `pytest`, `pre-commit` による高品質な Python 開発体験
- `TypedDict` による型安全な CloudFormation 出力ハンドリング
- `aws-lambda-typing` による Lambda イベントの型補完 (`aws-powertools`へ置き換え予定)
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
├── .devcontainer                     # Dev Container
│   ├── .env
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── docker-compose.yml
├── .dockerignore
├── .editorconfig
├── .flake8                          # flake8 設定
├── .gitattributes
├── .github                          # Github Actions
│   └── workflows
│       └── deploy-to-aws.yaml
├── .gitignore
├── .isort.cfg                       # isort 設定
├── .pre-commit-config.yaml          # pre-commitフック設定
├── .vscode
│   └── settings.json
├── README.md
├── layers                           # Lambda レイヤー
│   └── powertools
│       └── requirements.txt
├── mypy.ini                         # mypy 設定
├── openapi.yml                      # openapi 定義 (現状未使用)
├── pytest.ini                       # pytest 設定
├── requirements-dev.txt
├── samconfig.toml                   # sam コマンド設定
├── src                              # Lambda アプリケーションコード
│   ├── EventBridge_v1               # EventBridge + Lambda
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── S3_v1                        # S3 (Api Gateway + Lambda)
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── SQS_v1                       # SQS
│   │   ├── __init__.py
│   │   ├── reciever.py              # SQS + Lambda
│   │   ├── requirements.txt
│   │   └── sender.py                # SQS (Api Gateway + Lambda)
│   ├── __init__.py
│   ├── hello_world_v1               # Api Gateway + Lambda
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── requirements.txt
│   └── modules                      # TypedDict による型定義 (現状未使用)
│       └── __init__.py
├── template.yaml
└── tests                            # テストコード
    ├── __init__.py
    ├── requirements.txt
    └── unit
        ├── __init__.py
        ├── test_event_bridge.py     # src/EventBridge/app.py
        ├── test_hello.py            # src/hello_world/app.py
        ├── test_s3.py               # src/S3/app.py
        ├── test_sqs_reciever.py     # src/SQS/reciever.py
        └── test_sqs_sender.py       # src/SQS/sender.py
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

### aws_pwoertools

```python
# src/hello_world/app.py
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext

app = ApiGatewayResolver()
logger = Logger(service="HelloWorldService")
metrics = Metrics(namespace="HelloWorldFunction", service="HelloWorld")


@app.get("/hello")
def hello() -> Dict[str, str]:
    return {"message": "hello world"}


@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    logger.info("Hello Layer")
    metrics.add_metric(name="MetricsTest", unit=MetricUnit.Count, value=1)
    return app.resolve(event=event, context=context)
```

### aws_lambda_typing (aws_powertools へ置き換え予定)
```python
# src/hello_world/app.py (aws_lambda_typing ver)
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
- Python 3.13+
- black / isort / flake8 / mypy
