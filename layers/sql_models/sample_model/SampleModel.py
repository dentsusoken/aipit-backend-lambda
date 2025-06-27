from datetime import datetime

from base_model.BaseModel import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

# class Base(DeclarativeBase):
#     pass


class SampleModel(Base):
    __tablename__ = "SampleTable"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))

    def get_name(self) -> str:
        return f"{self.name}"


class SignatureModel(Base):
    __tablename__ = "SignatureTable"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    original_data: Mapped[str] = mapped_column(String(1024))
    signed_data: Mapped[str] = mapped_column(String(2048))
