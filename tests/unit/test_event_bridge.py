import requests
from unittest.mock import Mock

from src.EventBridge import app


def test_lambda_handler() -> None:
    mock_event = Mock()
    mock_context = Mock()

    app.lambda_handler(mock_event, mock_context)

    s3_object = requests.get('http://localstack:4566/sample-bucket/event_bridge.txt')
    print(s3_object)
    assert s3_object.json() == {"message": "This is sample"}

    s3_object = requests.delete('http://localstack:4566/sample-bucket/event_bridge.txt')
