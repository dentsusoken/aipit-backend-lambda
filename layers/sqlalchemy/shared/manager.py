from urllib.parse import quote_plus

from aws_lambda_powertools import Logger
from shared.parameters.secrets import Secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = Logger(service="SqlalchemyLayer")
secrets_instance = Secrets()


class DatabaseManager:
    def __init__(self) -> None:
        endpoint = secrets_instance.get_secret_str("/database/endpoint")
        port = secrets_instance.get_secret_str("/database/port")
        database = secrets_instance.get_secret_str("/database/name")
        secret_arn = secrets_instance.get_secret_str("/database/secret_arn")
        secret = secrets_instance.get_secret_obj(secret_arn)
        username = secret["username"]
        password = quote_plus(secret["password"])

        # DB に接続する
        logger.debug("RDS Connectiong ...")
        self.engine = create_engine(
            f"postgresql://{username}:{password}@{endpoint}:{port}/{database}"
        )
        logger.debug(f"Engine: {self.engine}")

        # セッションを作成する
        logger.debug("Session Creating ...")
        SessionClass = sessionmaker(self.engine)
        self.session = SessionClass()
        logger.debug(f"Secction: {self.session}")

    def insert(self, obj: object) -> None:
        """
        指定された SQLAlchemy モデルインスタンスをデータベースセッションに追加し、コミットします。

        引数:
            obj (object): データベースに挿入する SQLAlchemy の ORM モデルインスタンス。

        戻り値:
            なし
        """
        logger.debug("Insert Data")

        try:
            self.session.add(obj)
            self.session.commit()

            logger.debug(f"Insert Completed: {obj}")

        except Exception as e:
            logger.error(f"Insert failed: {e}")
            self.session.rollback()
