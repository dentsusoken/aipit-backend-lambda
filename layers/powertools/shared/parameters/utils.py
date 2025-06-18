import json
from typing import Any, Dict


def raw_to_obj(raw: str | bytes | Dict[str, Any] | None) -> Any:
    """
    引数を辞書型として返します。

    引数が文字列型（str）の場合は JSON としてパースして辞書型に変換します。
    すでに辞書型（dict）の場合はそのまま返します。
    それ以外の型の場合は、予期しない型として ValueError を送出します。

    引数:
        raw (str | bytes | Dict[str, Any] | None): 変換したいデータ

    戻り値:
        Any: JSON としてパースされたデータ

    例外:
        ValueError: 引数の型が bytes または str 以外の場合に発生します。
    """
    if isinstance(raw, str):
        return json.loads(raw)
    elif isinstance(raw, dict):
        return raw
    else:
        raise ValueError(f"Failed to parse: {type(raw)}")
