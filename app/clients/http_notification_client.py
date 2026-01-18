import requests
from app.clients.notification_client import NotificationClient
from app.repositories.user_repository import User


class HttpNotificationClient(NotificationClient):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def send_user_created(self, user: User) -> None:
        resp = requests.post(
            f"{self.base_url}/v2/notify",
            json={"uid": user.id},
            timeout=3,
        )

        resp.raise_for_status()
        data = resp.json()

        if not data.get("ok"):
            raise RuntimeError("Notification API returned failure")
