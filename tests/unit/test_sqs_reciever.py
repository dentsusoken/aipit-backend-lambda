import json
from unittest.mock import Mock

import requests
from aws_lambda_typing.events import SQSEvent

from src.SQS_v1 import reciever


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
