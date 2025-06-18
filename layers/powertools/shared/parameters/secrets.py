from typing import Any

from aws_lambda_powertools.utilities.parameters import SecretsProvider
from shared.parameters.utils import raw_to_obj, raw_to_str


class Secrets:
    def __init__(self) -> None:
        self.secrets = SecretsProvider()

    def get_secret_obj(self, key: str) -> Any:
        """
        指定されたキーに対応するシークレットを SecretsProvider から取得し、辞書型として返します。

        引数:
            key (str): 取得したいシークレットのキー。

        戻り値:
            Any: 取得されたシークレットの辞書。
        """

        raw = self.secrets.get(key)

        return raw_to_obj(raw)

    def get_secret_str(self, key: str) -> str:
        """
        指定されたキーに対応するシークレットを SecretsProvider から取得し、文字列として返します。

        引数:
            key (str): 取得したいシークレットのキー。

        戻り値:
            Any: 取得されたシークレットの文字列。
        """

        raw = self.secrets.get(key)

        return raw_to_str(raw)
