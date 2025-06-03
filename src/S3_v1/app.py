import json
import os
import time

import boto3
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
from botocore.exceptions import ClientError

AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "api-northeast-1")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL", None)
BUCKET_NAME = os.environ.get(
    "BUCKET_NAME", "sample-bucket-8b902d87-1c66-4cb6-9eae-a180842c6351"
)
OBJECT_NAME = os.environ.get("OBJECT_NAME", "sample.txt")
logger = Logger(service="HelloWorldService")
metrics = Metrics(namespace="PutS3ObjectFucnction", service="PutObject")


@metrics.log_metrics
def lambda_handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger.info("start")
    start_time = time.time()

    try:
        s3_resource = boto3.resource(
            "s3", region_name=AWS_DEFAULT_REGION, endpoint_url=AWS_ENDPOINT_URL
        )

    except ClientError as e:
        message = "Can't create resource"
        logger.error(e)

        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    logger.info("create resource finish")

    try:
        body = json.loads(event["body"]) if event["body"] is not None else {}
        object_name = body.get("object_name") or OBJECT_NAME

    except Exception:
        message = "The body must be in JSON format."
        logger.error(message)

        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    json_obj = {"message": "This is sample"}

    try:
        s3_obj = s3_resource.Object(BUCKET_NAME, object_name)
        s3_obj.put(Body=json.dumps(json_obj))

    except ClientError as e:
        message = "Can't put a object"
        logger.error(e)

        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    logger.info("put object finish")

    message = "S3 hello world"

    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000

    metrics.add_metric(
        name="ProcessingTime", unit=MetricUnit.Milliseconds, value=duration_ms
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
