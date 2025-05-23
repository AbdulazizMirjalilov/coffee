from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")  # NOQA
