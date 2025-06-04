import json
import time
from typing import Any

import boto3
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from botocore.exceptions import ClientError

logger = Logger(service="EventBridgeFunction")
metrics = Metrics(namespace="EventBridgeFunction", service="EventBridge")


def lambda_handler(event: APIGatewayProxyEventV1, context: Context) -> None:
    start_time = time.time()
    lambda_client = boto3.client("lambda")

    params: dict[str, Any] = {
        "FunctionName": "PutS3ObjectV1Function",
        "Payload": json.dumps(
            {"body": json.dumps({"object_name": "event_bridge.txt"})}
        ),
    }

    try:
        response = lambda_client.invoke(**params)
        logger.info("Invocation response:", response)

        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000

        metrics.add_metric(
            name="ProcessingTime", unit=MetricUnit.Milliseconds, value=duration_ms
        )
    except ClientError as e:
        logger.error(f"Error invoking Lambda: {e}")
