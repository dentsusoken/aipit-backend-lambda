from typing import Any, Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

app = ApiGatewayResolver()
logger = Logger(service="HelloWorldService")


@app.get("/hello")
def hello() -> Dict[str, str]:
    return {"message": "hello world"}


def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    logger.info("Hello Layer")
    return app.resolve(event=event, context=context)
