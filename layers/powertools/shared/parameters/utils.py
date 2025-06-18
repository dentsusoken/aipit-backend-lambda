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


def raw_to_str(raw: str | bytes | Dict[str, Any] | None) -> str:
    """
    引数を文字列として返します。

    すでに文字列型（str）の場合はそのまま返します。
    引数が辞書型（dict）の場合は JSON をダンプして文字列に変換します。
    引数がバイト型 (bytes) の場合は bytes をデコードして文字列に変換します。
    それ以外の型の場合は、予期しない型として ValueError を送出します。

    引数:
        raw (str | bytes | Dict[str, Any] | None): 変換したいデータ

    戻り値:
        str: 文字列として変換されたデータ

    例外:
        ValueError: 引数の型が dict または bytes、str 以外の場合に発生します。
    """
    if isinstance(raw, str):
        return raw
    elif isinstance(raw, dict):
        return json.dumps(raw, ensure_ascii=False)
    elif isinstance(raw, bytes):
        return raw.decode("utf-8")
    else:
        raise ValueError(f"Failed to string: {type(raw)}")
