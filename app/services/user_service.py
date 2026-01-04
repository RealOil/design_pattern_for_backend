from app.repositories.user_repository import User, UserRepository
from app.clients.notification_client import NotificationClient

class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        notifier: NotificationClient,
    ) -> None:
        self.user_repo = user_repo
        self.notifier = notifier

    def create_user(self, user_id: int, name: str) -> None:
        user = User(id=user_id, name=name)

        # 오케스트레이션: 저장하고, 알림 요청
        self.user_repo.save(user)
        self.notifier.send_user_created(user)