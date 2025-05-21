import json
import boto3
import logging

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1

from modules.lambda_events import LambdaResponse

REGION_NAME = 'ap-northeast-1'
ENDPOINT_URL = 'http://localstack:4566'
QUEUE_NAME = 'sampleQueue.fifo'

sqs = boto3.client('sqs', region_name=REGION_NAME, endpoint_url=ENDPOINT_URL)


def lambda_handler(event: APIGatewayProxyEventV1, context: Context) -> LambdaResponse:

    try:
        body = json.loads(event['body']) if event['body'] is not None else {}
        message = body['message'] if 'message' in body else ''

    except Exception:
        message = 'hello world!'

    try:
        # FIFO キューの URL を取得
        get_queur_url_response = sqs.get_queue_url(QueueName=QUEUE_NAME)
        queue_url = get_queur_url_response['QueueUrl']

        # メッセージ送信
        send_response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
            MessageGroupId="sampleSQS"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'sent {send_response['MessageId']}'})
        }

    except Exception as e:
        logging.error(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'some error happened'})
        }
