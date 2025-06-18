from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from sample_model.SampleModel import SampleModel
from shared.manager import DatabaseManager
from shared.parameters.secrets import Secrets

app = ApiGatewayResolver()
logger = Logger(service="InsertDataToAuroraFunction")
metrics = Metrics(namespace="InsertDataToAuroraFunction", service="Aurora")
secrets_instance = Secrets()
db_manager = DatabaseManager()


@app.post("/db")
def insert() -> Dict[str, Any]:
    """
    HTTP POST リクエストを受け取り、リクエストボディの情報を元にデータベースへレコードを挿入します。

    リクエストボディから `name` を取得し、`SampleModel` のインスタンスを作成してデータベースに保存します。

    成功した場合は、挿入されたデータの `name` を含むメッセージを返します。

    戻り値:
        Dict[str, Any]: 挿入結果を示すメッセージ。

    例外:
        BadRequestError: リクエストボディが不正な場合に発生します。
    """

    try:
        logger.debug("### Parsing Request ###")
        logger.debug("Event: %s", str(app.current_event))
        body = app.current_event.json_body
        logger.debug("Body: %s", str(body))
        name = body.get("name", "sample")
        logger.debug("Name: %s", name)
    except Exception as e:
        logger.exception(e)
        raise BadRequestError("Invalid request body")

    # DB にデータを挿入する
    sample = SampleModel(name=name)
    db_manager.insert(sample)

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
