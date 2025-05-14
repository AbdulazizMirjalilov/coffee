from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class ErrorResponse:
    name: str
    code: int | None = None
    details: dict[str, Any] | None = None


@dataclass
class PaginationMetadata:
    page: int
    total_pages: int
    page_size: int


@dataclass
class Metadata:
    total: int
    pagination: PaginationMetadata


@dataclass
class BaseResponse(Generic[T]):
    success: bool
    message: str
    data: T | ErrorResponse
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: Metadata | None = None
