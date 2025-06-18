from typing import Any

from aws_lambda_powertools.utilities.parameters import SSMProvider
from shared.parameters.utils import raw_to_obj, raw_to_str


class Ssm:
    def __init__(self) -> None:
        self.ssm = SSMProvider()

    def get_parameter_obj(self, key: str) -> Any:
        """
        指定されたキーに対応するパラメータを Parameter Store から取得し、辞書型として返します。

        引数:
            key (str): 取得したいパラメータのキー。

        戻り値:
            Any: 取得されたパラメータの辞書。
        """
        raw = self.ssm.get(key)

        return raw_to_obj(raw)

    def get_parameter_str(self, key: str) -> str:
        """
        指定されたキーに対応するパラメータを Parameter Store から取得し、文字列として返します。

        引数:
            key (str): 取得したいパラメータのキー。

        戻り値:
            str: 取得されたパラメータの文字列。
        """
        raw = self.ssm.get(key)
        return raw_to_str(raw)
