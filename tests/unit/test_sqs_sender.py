import json
import time
import requests
from datetime import datetime, UTC
from unittest.mock import Mock

from aws_lambda_typing.events import APIGatewayProxyEventV2

from src.SQS import sender
from src.SQS import reciever


def test_sqs_sender() -> None:
    event: APIGatewayProxyEventV2 = {"body": json.dumps({
        "message": f"Test at {datetime.now(UTC)}"
    })}
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
