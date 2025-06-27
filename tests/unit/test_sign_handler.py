import base64
import json
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.PKCS_v1 import app


@pytest.fixture
def context() -> Mock:
    """Lambdaのモックコンテキスト"""
    return Mock()


@pytest.fixture
def valid_event() -> Dict[str, Any]:
    """正しいPOSTリクエスト（message付き）"""
    return {
        "httpMethod": "POST",
        "path": "/pkcs-sign",
        "body": json.dumps({"message": "Hello, World!"}),
        "isBase64Encoded": False,
    }


@pytest.fixture
def missing_message_event() -> Dict[str, Any]:
    """messageのないbody"""
    return {
        "httpMethod": "POST",
        "path": "/pkcs-sign",
        "body": json.dumps({}),
        "isBase64Encoded": False,
    }


def test_sign_handler_success(valid_event: Dict[str, Any], context: Mock) -> None:
    """
    正常系: 正しいメッセージを送ったときに、署名が成功し
    '署名完了' と署名文字列が返ることを確認する
    """

    with patch("shared.manager.DatabaseManager.insert", MagicMock()):
        result = app.lambda_handler(valid_event, context)

    body = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert body["message"] == "署名完了"
    assert isinstance(body["signature"], str)
    assert base64.b64decode(body["signature"])


def test_sign_handler_missing_message(
    missing_message_event: Dict[str, Any], context: Mock
) -> None:
    """
    異常系: 'message' フィールドが欠けていた場合、
    400エラー（BadRequestError）が返ることを確認する
    """
    result = app.lambda_handler(missing_message_event, context)
    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert "Missing 'message' in body" in body["message"]


def test_sign_handler_exception_during_db_insert(
    valid_event: Dict[str, Any], context: Mock
) -> None:
    """
    異常系: 秘密鍵の読み込みに失敗した場合に、500エラー（InternalServerError）が返ることを確認する
    """
    with patch(
        "shared.manager.DatabaseManager.insert", side_effect=Exception("DB Error")
    ):
        result = app.lambda_handler(valid_event, context)
        body = json.loads(result["body"])

    assert result["statusCode"] == 500
    assert "Unexpected error occurred" in body["message"]
