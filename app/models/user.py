from enum import Enum as BaseEnum

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.base_model import BaseModel


class UserRole(str, BaseEnum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="user")  # NOQA
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")  # NOQA
    sent_messages: Mapped[list["SupportMessage"]] = relationship(  # NOQA
        back_populates="sender", foreign_keys="SupportMessage.sender_id"
    )
    received_messages: Mapped[list["SupportMessage"]] = relationship(  # NOQA
        back_populates="receiver", foreign_keys="SupportMessage.receiver_id"
    )

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False
    )
