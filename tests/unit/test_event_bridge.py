from unittest.mock import Mock

import requests
from aws_lambda_powertools.utilities.parameters import get_parameter

from src.EventBridge_v1 import app

BUCKET_NAME = get_parameter("/sample/bucket_name")
print(BUCKET_NAME)


def test_lambda_handler() -> None:
    mock_event = Mock()
    mock_context = Mock()
    object_name = "event_bridge.txt"

    app.lambda_handler(mock_event, mock_context)

    s3_object = requests.get(f"http://localstack:4566/{BUCKET_NAME}/{object_name}")
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete(f"http://localstack:4566/{BUCKET_NAME}/{object_name}")
