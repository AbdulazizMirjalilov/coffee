from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.base.base_model import BaseModel


class StaticInfo(BaseModel):
    __tablename__ = "static_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(Text)
    working_hours: Mapped[str] = mapped_column(String(100))
    hotline_phone: Mapped[str] = mapped_column(String(20))
