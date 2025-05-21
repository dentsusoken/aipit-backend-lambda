import json
import time
from datetime import UTC, datetime
from unittest.mock import Mock

import requests
from aws_lambda_typing.events import APIGatewayProxyEventV1, SQSEvent

from src.SQS import reciever, sender


def test_sqs_sender() -> None:
    object_name = "test_sender.txt"

    event: APIGatewayProxyEventV1 = {
        "body": json.dumps(
            {
                "messageBody": {
                    "message": f"Test at {datetime.now(UTC)}",
                    "object_name": f"{object_name}",
                }
            }
        ),
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": ("1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"),
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,"
                "*/*;q=0.8"
            ),
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": ("aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA=="),
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
        "multiValueHeaders": {},
        "multiValueQueryStringParameters": {},
        "isBase64Encoded": False,
    }
    mock_context = Mock()

    sender.lambda_handler(event, mock_context)

    # SQS の処理を待つ
    time.sleep(5)

    s3_object = requests.get(f"http://localstack:4566/sample-bucket/{object_name}")
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete(f"http://localstack:4566/sample-bucket/{object_name}")


def test_sqs_reciever() -> None:
    object_name = "test_reciever.txt"

    event: SQSEvent = {
        "Records": [{"body": json.dumps({"object_name": f"{object_name}"})}]
    }
    mock_context = Mock()

    reciever.lambda_handler(event, mock_context)

    s3_object = requests.get(f"http://localstack:4566/sample-bucket/{object_name}")
    print(s3_object)
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete(f"http://localstack:4566/sample-bucket/{object_name}")
