import json
from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import SQSEvent
from botocore.exceptions import ClientError

logger = Logger(service="SQSRecieverFunction")


def lambda_handler(event: SQSEvent, context: Context) -> None:
    lambda_client = boto3.client("lambda")

    for message in event["Records"]:
        try:
            body = json.loads(message["body"]) if message["body"] is not None else {}
            object_name = body["object_name"] if "object_name" in body else "sqs.txt"

        except Exception:
            object_name = "sqs.txt"

        params: dict[str, Any] = {
            "FunctionName": "PutS3ObjectV1FunctionPattern2",
            "Payload": json.dumps(
                {"body": json.dumps({"object_name": f"{object_name}"})}
            ),
        }

        try:
            response = lambda_client.invoke(**params)
            logger.info("Invocation response:", response)
        except ClientError as e:
            logger.error(f"Error invoking Lambda: {e}")
