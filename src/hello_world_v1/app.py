from aws_lambda_powertools import Logger
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1

logger = Logger(service="HelloWorldService")


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger.info("Hello Layer")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"message": "hello world"}',
    }
