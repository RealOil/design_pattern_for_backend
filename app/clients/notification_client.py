from __future__ import annotations
from typing import Protocol
from app.repositories.user_repository import User


class NotificationClient(Protocol):
    def send_user_created(self, user: User) -> None: ...
