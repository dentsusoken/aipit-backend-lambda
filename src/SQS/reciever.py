import json
import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import SQSEvent

from modules.lambda_events import LambdaResponse


def lambda_handler(event: SQSEvent, context: Context) -> LambdaResponse:
    lambda_client = boto3.client('lambda')

    for message in event['Records']:
        try:
            body = json.loads(message['body']) if message['body'] is not None else {}
            object_name = body['object_name'] if 'object_name' in body else 'sqs.txt'

        except Exception:
            object_name = 'sqs.txt'

        params: dict[str, Any] = {
            'FunctionName': 'PutS3ObjectFunction',
            'Payload': json.dumps({
                'body': json.dumps({
                    'object_name': f'{object_name}'
                })
            })
        }

        try:
            response = lambda_client.invoke(**params)
            logging.info('Invocation response:', response)
        except ClientError as e:
            logging.error(f'Error invoking Lambda: {e}')
