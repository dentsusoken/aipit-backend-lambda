from modules.lambda_events import LambdaResponse

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2


def handler(event: APIGatewayProxyEventV2, context: Context) -> LambdaResponse:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"message": "hello world"}',
    }
