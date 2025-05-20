import json
from typing import Any, Dict


def get_response(statusCode: int, message: str) -> Dict[str, Any]:
    return {
        "statusCode": statusCode,
        "body": json.dumps({
            "message": message,
        }),
    }
