import json
from typing import Any, Callable, Generator
from unittest.mock import Mock

import pytest
from aws_lambda_typing.events import APIGatewayProxyEventV1
from sample_model.SampleModel import SampleModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.Aurora_v1 import app


@pytest.fixture()
def apigw_event() -> (
    Generator[Callable[[dict[str, Any]], APIGatewayProxyEventV1], None, None]
):
    """Generates API GW Event"""

    def _apigw_event(body: dict[str, Any]) -> APIGatewayProxyEventV1:
        return {
            "body": json.dumps(body),
            "resource": "/db",
            "requestContext": {
                "resourceId": "123456",
                "apiId": "1234567890",
                "resourcePath": "/db",
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
            "queryStringParameters": {"name": "test"},
            "headers": {
                "Via": (
                    "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
                ),
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
                "X-Amz-Cf-Id": (
                    "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA=="
                ),
                "CloudFront-Is-Tablet-Viewer": "false",
                "Cache-Control": "max-age=0",
                "User-Agent": "Custom User Agent String",
                "CloudFront-Forwarded-Proto": "https",
                "Accept-Encoding": "gzip, deflate, sdch",
            },
            "pathParameters": {"proxy": "/db"},
            "httpMethod": "POST",
            "stageVariables": {"baz": "qux"},
            "path": "/db",
            "multiValueHeaders": {},
            "multiValueQueryStringParameters": {},
            "isBase64Encoded": False,
        }

    yield _apigw_event


@pytest.mark.parametrize(
    "body, expected_status, expected_data",
    [
        pytest.param(
            {"name": "test"},
            200,
            "test",
        ),
        pytest.param(
            None,
            400,
            "Invalid request body",
        ),
    ],
)
def test_lambda_handler(
    monkeypatch: pytest.MonkeyPatch,
    apigw_event: Callable[[dict[str, Any]], APIGatewayProxyEventV1],
    body: dict[str, Any],
    expected_status: int,
    expected_data: str,
) -> None:
    # 環境変数を設定する
    monkeypatch.setenv("DB_ENDPOINT", "localhost.localstack.cloud")
    monkeypatch.setenv("DB_PORT", "4510")
    monkeypatch.setenv("DB_NAME", "SampleDB")
    monkeypatch.setenv("DB_PASSWORD_SECRET_ARN", "rds/password")

    mock_context = Mock()

    ret = app.handler(apigw_event(body), mock_context)
    data = json.loads(ret["body"])

    # DB に接続する
    engine = create_engine(
        "postgresql://SampleUser:test@localhost.localstack.cloud:4510/SampleDB"
    )

    # セッションを作成する
    SessionClass = sessionmaker(engine)
    session = SessionClass()

    # テストで作成したレコードを取得する
    record = None
    if ret["statusCode"] == 200:
        record = (
            session.query(SampleModel).filter(SampleModel.name == body["name"]).first()
        )

    assert ret["statusCode"] == expected_status
    assert "message" in ret["body"]
    assert data["message"] == expected_data

    # 作成したデータが存在しているか
    if record:
        assert record.get_name() == expected_data

        # 作成したデータを削除する
        session.delete(record)
        session.commit()
