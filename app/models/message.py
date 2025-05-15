import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.base_model import BaseModel


class SupportMessage(BaseModel):
    __tablename__ = "support_messages"

    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)

    sender: Mapped["User"] = relationship(  # NOQA
        foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver: Mapped["User"] = relationship(  # NOQA
        foreign_keys=[receiver_id], back_populates="received_messages"
    )
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
