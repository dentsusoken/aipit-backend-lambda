from typing import TypedDict


class LambdaResponse(TypedDict):
    statusCode: int
    headers: dict[str, str]
    body: str
