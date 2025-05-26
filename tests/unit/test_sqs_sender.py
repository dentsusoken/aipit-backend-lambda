import json
from datetime import UTC, datetime
from typing import Generator
from unittest.mock import Mock

import boto3
import pytest
from aws_lambda_typing.events import APIGatewayProxyEventV1
from mypy_boto3_sqs import SQSClient
from mypy_boto3_sqs.type_defs import MessageTypeDef

from src.modules.constants import AWS_DEFAULT_REGION, AWS_ENDPOINT_URL, QUEUE_NAME
from src.SQS_v1 import sender


@pytest.fixture(scope="module", autouse=True)
def disable_event_source_mapping() -> Generator[None, None, None]:
    lambda_client = boto3.client(
        "lambda", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_DEFAULT_REGION
    )

    # 対象の Lambda 関数名を指定
    function_name = "SQSRecieverV1Function"  # ← ここを実際の関数名に置き換えてください

    # イベントソースマッピングの一覧を取得
    response = lambda_client.list_event_source_mappings(FunctionName=function_name)

    # SQS に関連するマッピングをフィルタ（1つだけと仮定）
    sqs_mappings = [
        mapping
        for mapping in response["EventSourceMappings"]
        if mapping["EventSourceArn"].startswith("arn:aws:sqs")
    ]

    if not sqs_mappings:
        raise Exception("SQS イベントソースマッピングが見つかりませんでした。")

    event_source_uuid = sqs_mappings[0]["UUID"]

    # 無効化
    lambda_client.update_event_source_mapping(UUID=event_source_uuid, Enabled=False)
    yield
    # 有効化
    lambda_client.update_event_source_mapping(UUID=event_source_uuid, Enabled=True)


def receive_message_with_retry(sqs: SQSClient, queue_url: str) -> MessageTypeDef:
    for _ in range(5):
        response = sqs.receive_message(
            QueueUrl=queue_url, WaitTimeSeconds=10, MaxNumberOfMessages=1
        )
        if "Messages" in response:
            return response["Messages"][0]

    raise TimeoutError("メッセージの取得に失敗しました")


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
    sqs = boto3.client(
        "sqs", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_DEFAULT_REGION
    )
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

    message = receive_message_with_retry(sqs, queue_url)
    assert "Body" in message

    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
