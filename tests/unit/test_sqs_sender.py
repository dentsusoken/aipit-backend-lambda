import json
import time
import requests
from datetime import datetime, UTC
from unittest.mock import Mock

from aws_lambda_typing.events import APIGatewayProxyEventV1

from src.SQS import sender
from src.SQS import reciever


def test_sqs_sender() -> None:
    event: APIGatewayProxyEventV1 = {
        "body": json.dumps(
            {
                "message": f"Test at {datetime.now(UTC)}",
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
    time.sleep(2)

    s3_object = requests.get('http://localstack:4566/sample-bucket/sqs.txt')
    print(s3_object)
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete('http://localstack:4566/sample-bucket/sqs.txt')


def test_sqs_reciever() -> None:
    mock_event = Mock()
    mock_context = Mock()

    reciever.lambda_handler(mock_event, mock_context)

    # SQS の処理を待つ
    time.sleep(1)

    s3_object = requests.get('http://localstack:4566/sample-bucket/sqs.txt')
    print(s3_object)
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete('http://localstack:4566/sample-bucket/sqs.txt')
