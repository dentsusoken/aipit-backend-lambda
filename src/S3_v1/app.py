import json

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
from botocore.exceptions import ClientError

from modules.constants import (
    AWS_DEFAULT_REGION,
    AWS_ENDPOINT_URL,
    BUCKET_NAME,
    OBJECT_NAME,
)

logger = Logger(service="HelloWorldService")


def lambda_handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger.info("start")

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

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
