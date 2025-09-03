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
