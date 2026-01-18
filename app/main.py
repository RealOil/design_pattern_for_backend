from app.services.user_service import UserService
from app.repositories.sqlite_user_repository import SQLiteUserRepository
from app.clients.http_notification_client import HttpNotificationClient
from app.policies.notification_strategies import (
    ProdSendPolicy,
    DevSkipPolicy,
    TestUserLogOnlyPolicy,
)


def create_user_service():
    user_repo = SQLiteUserRepository()
    notifier = HttpNotificationClient(base_url="https://external.api")

    # 예시: 환경에 따라 정책 선택
    policy = TestUserLogOnlyPolicy()

    return UserService(
        user_repo=user_repo,
        notifier=notifier,
        notification_policy=policy,
    )


# 👉 “어떤 정책을 쓸지”는 여기서만 결정합니다.
