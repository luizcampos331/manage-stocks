import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(kw_only=True)
class Entity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None
