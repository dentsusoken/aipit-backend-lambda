import base64
import json
from datetime import UTC, datetime
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
)
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from sample_model.SampleModel import SignatureModel
from shared.manager import DatabaseManager

logger = Logger()
metrics = Metrics(namespace="SignatureService")
app = ApiGatewayResolver()


# ダミーRSA鍵生成関数
def generate_test_key() -> bytes:
    private_key: rsa.RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


# 暫定：テスト用の秘密鍵
PRIVATE_KEY_PEM = generate_test_key()


@app.post("/pkcs-sign")
def sign_handler() -> Dict[str, Any]:
    """
    Lambda function that signs message using PKCS#1 and saves it to DB.

    Layers used:
    - PowertoolsLayer (logging, metrics, event handler)
    - SqlalchemyLayer (SQLAlchemy library for DB)
    - SqlModelsLayer (custom DB model: SignatureModel)
    """
    try:
        logger.info("Event: %s", str(app.current_event))
        body = app.current_event.json_body
        logger.info("Body: %s", str(body))
        message = body.get("message")
        if not message:
            raise BadRequestError("Missing 'message' in body")

        logger.info("署名処理開始", extra={"custom_message": message})
        metrics.add_metric(name="SignRequest", unit=MetricUnit.Count, value=1)

        # 署名
        key = serialization.load_pem_private_key(PRIVATE_KEY_PEM, password=None)

        if not isinstance(key, rsa.RSAPrivateKey):
            raise TypeError("Expected RSAPrivateKey, but got different type")

        private_key: rsa.RSAPrivateKey = key

        signature = private_key.sign(
            message.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
        )

        signature_b64 = base64.b64encode(signature).decode("utf-8")

        # DB保存
        db_manager = DatabaseManager()
        record = SignatureModel(
            created_at=datetime.now(UTC),
            original_data=message,
            signed_data=signature_b64,
        )
        db_manager.insert(record)
        return {"message": "署名完了", "signature": signature_b64}
    except BadRequestError as e:
        logger.exception("BadRequestError: %s", str(e))
        raise e
    except Exception as e:
        logger.exception("Unexpected error: %s", str(e))
        raise InternalServerError("Unexpected error occurred")


def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Entrypoint for AWS Lambda
    """
    try:
        logger.info("Hello Entrypoint for AWS Lambda")
        return app.resolve(event, context)
    except BadRequestError as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
        }
