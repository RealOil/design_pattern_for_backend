from app.repositories.user_repository import User, UserRepository
from app.clients.notification_client import NotificationClient
import os
import logging

logger = logging.getLogger(__name__)


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

        # 1. 사용자 저장
        self.user_repo.save(user)

        # 2. ❌ 알림 정책 분기 (의도적으로 나쁘게)
        env = os.getenv("APP_ENV", "dev")

        if env == "prod":
            # 운영 환경: 실제 알림 전송
            self.notifier.send_user_created(user)

        elif env == "dev":
            # 개발 환경: 아무 것도 하지 않음
            logger.info("DEV environment: skip notification")

        elif name.startswith("test_"):
            # 테스트용 사용자: 로그만 남김
            logger.info(f"Test user created: {user.id}")

        else:
            # 기본 정책
            self.notifier.send_user_created(user)
