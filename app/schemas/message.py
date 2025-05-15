from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SupportMessageResponse(BaseModel):
    id: UUID
    message: str
    is_read: bool
    sender_id: UUID
    receiver_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
