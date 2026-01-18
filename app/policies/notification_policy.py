from enum import Enum
from typing import Protocol
from app.repositories.user_repository import User


class NotificationAction(Enum):
    SEND = "send"
    SKIP = "skip"
    LOG_ONLY = "log_only"


class NotificationPolicy(Protocol):
    def decide(self, user: User, env: str) -> NotificationAction: ...
