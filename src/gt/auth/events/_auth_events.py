from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """
    Base class for domain events.
    """

    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserCreatedEvent(DomainEvent):
    """
    Event triggered when a new user is created.
    """

    user_id: int
    user_uuid: str
    email_token: str
    email_token_expiry_minutes: int
