import json
import logging

import boto3
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
from botocore.exceptions import ClientError

from modules.constants import (AWS_DEFAULT_REGION, AWS_ENDPOINT_URL,
                               BUCKET_NAME, OBJECT_NAME)


def lambda_handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logging.info("start")

    try:
        s3_resource = boto3.resource(
            "s3", region_name=AWS_DEFAULT_REGION, endpoint_url=AWS_ENDPOINT_URL
        )

    except ClientError as e:
        message = "Can't create resource"
        logging.error(e)

        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    logging.info("create resource finish")

    try:
        body = json.loads(event["body"]) if event["body"] is not None else {}
        bucket_name = body["bucket_name"] if "bucket_name" in body else BUCKET_NAME
        object_name = body["object_name"] if "object_name" in body else OBJECT_NAME

    except Exception:
        message = "The body must be in JSON format."
        logging.error(message)

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
        s3_obj = s3_resource.Object(bucket_name, object_name)
        s3_obj.put(Body=json.dumps(json_obj))

    except ClientError as e:
        message = "Can't put a object"
        logging.error(e)

        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    logging.info("put object finish")

    message = "S3 hello world"

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
