from base_model.BaseModel import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

# class Base(DeclarativeBase):
#     pass


class SampleModel(Base):
    __tablename__ = "SampleTable"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def get_name(self) -> str:
        return f"{self.name}"
