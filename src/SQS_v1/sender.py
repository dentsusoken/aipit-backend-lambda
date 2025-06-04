import json
import os
import time

import boto3
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1

AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "api-northeast-1")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL", None)
QUEUE_NAME = os.environ.get("QUEUE_NAME", "sampleQueue.fifo")
sqs = boto3.client("sqs", region_name=AWS_DEFAULT_REGION, endpoint_url=AWS_ENDPOINT_URL)
logger = Logger(service="HelloWorldService")
metrics = Metrics(namespace="SQSSenderFunction", service="SQSSender")


def lambda_handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    start_time = time.time()

    try:
        body = json.loads(event["body"]) if event["body"] is not None else {}
        messageBody = (
            json.dumps(body["messageBody"]) if "messageBody" in body else "sample"
        )

    except Exception:
        messageBody = "hello world!"

    try:
        # FIFO キューの URL を取得
        get_queur_url_response = sqs.get_queue_url(QueueName=QUEUE_NAME)
        queue_url = get_queur_url_response["QueueUrl"]

        # メッセージ送信
        send_response = sqs.send_message(
            QueueUrl=queue_url, MessageBody=messageBody, MessageGroupId="sampleSQS"
        )

        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000

        metrics.add_metric(
            name="ProcessingTime", unit=MetricUnit.Milliseconds, value=duration_ms
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"sent {send_response['MessageId']}"}),
        }

    except Exception as e:
        logger.error(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "some error happened"}),
        }
