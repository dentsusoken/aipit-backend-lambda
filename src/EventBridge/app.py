import json
import logging
from typing import Any

import boto3
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from botocore.exceptions import ClientError

from modules.lambda_events import LambdaResponse


def lambda_handler(event: APIGatewayProxyEventV1, context: Context) -> LambdaResponse:
    lambda_client = boto3.client('lambda')

    params: dict[str, Any] = {
        'FunctionName': 'PutS3ObjectFunction',
        'Payload': json.dumps({
            'body': json.dumps({
                'object_name': 'event_bridge.txt'
            })
        })
    }

    try:
        response = lambda_client.invoke(**params)
        logging.info('Invocation response:', response)
    except ClientError as e:
        logging.error(f'Error invoking Lambda: {e}')
