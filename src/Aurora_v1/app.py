import os
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parameters import SecretsProvider
from aws_lambda_powertools.utilities.typing import LambdaContext
from sample_model.SampleModel import SampleModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = ApiGatewayResolver()
logger = Logger(service="InsertDataToAuroraFunction")
metrics = Metrics(namespace="InsertDataToAuroraFunction", service="Aurora")


def get_secret_str(key: str) -> str:
    """
    指定されたキーに対応するシークレットを SecretsProvider から取得し、文字列として返します。

    シークレットがバイト型（bytes）の場合は UTF-8 でデコードし、文字列型（str）の場合はそのまま返します。
    それ以外の型の場合は、予期しない型として ValueError を送出します。

    引数:
        key (str): 取得したいシークレットのキー。

    戻り値:
        str: 取得されたシークレットの文字列。

    例外:
        ValueError: シークレットの型が bytes または str 以外の場合に発生します。
    """

    secrets = SecretsProvider()
    value = secrets.get(key)
    if isinstance(value, bytes):
        return value.decode()
    elif isinstance(value, str):
        return value
    else:
        raise ValueError(f"Unexpected secret type for key '{key}': {type(value)}")


@app.post("/db")
def insert() -> Dict[str, Any]:
    """
    HTTP POST リクエストを受け取り、リクエストボディの情報を元にデータベースへレコードを挿入します。

    リクエストボディから `name` を取得し、環境変数と Secrets Manager を使って
    データベース接続情報を構成します。SQLAlchemy を用いて PostgreSQL に接続し、
    `SampleModel` のインスタンスを作成してデータベースに保存します。

    成功した場合は、挿入されたデータの `name` を含むメッセージを返します。

    戻り値:
        Dict[str, Any]: 挿入結果を示すメッセージ。

    例外:
        BadRequestError: リクエストボディが不正な場合に発生します。
    """

    try:
        body = app.current_event.json_body
        name = body.get("name", "sample")
    except Exception:
        raise BadRequestError("Invalid request body")

    username = os.environ["DB_USER_NAME"]
    endpoint = os.environ["DB_ENDPOINT"]
    port = os.environ["DB_PORT"]
    database = os.environ["DB_NAME"]
    secret_arn = os.environ["DB_PASSWORD_SECRET_ARN"]
    password = get_secret_str(secret_arn)

    # DB に接続する
    engine = create_engine(
        f"postgresql://{username}:{password}@{endpoint}:{port}/{database}"
    )

    # セッションを作成する
    SessionClass = sessionmaker(engine)
    session = SessionClass()

    # DB にデータを挿入する
    sample = SampleModel(name=name)
    session.add(sample)
    session.commit()

    # 結果を返す
    return {"message": f"{sample.get_name()}"}


@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    AWS Lambda 関数のエントリーポイント。

    Lambda が呼び出された際に実行され、メトリクスの記録やログ出力を行った後、
    アプリケーションのルーティング処理にイベントとコンテキストを渡します。

    メトリクスとして "MetricsTest"（単位: Count, 値: 1）を記録し、
    コールドスタートのメトリクスも自動的に収集されます。

    引数:
        event (Dict[str, Any]): Lambda に渡されるイベントデータ。
        context (LambdaContext): 実行時のコンテキスト情報。

    戻り値:
        Dict[str, Any]: アプリケーションのレスポンス。
    """

    logger.info("Hello Layer")
    metrics.add_metric(name="MetricsTest", unit=MetricUnit.Count, value=1)

    return app.resolve(event=event, context=context)
