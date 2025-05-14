import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
