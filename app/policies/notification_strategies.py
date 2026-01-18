from app.repositories.user_repository import User
from app.policies.notification_policy import NotificationAction, NotificationPolicy


class ProdSendPolicy(NotificationPolicy):
    def decide(self, user: User, env: str) -> NotificationAction:
        if env == "prod":
            return NotificationAction.SEND
        return NotificationAction.SKIP


class DevSkipPolicy(NotificationPolicy):
    def decide(self, user: User, env: str) -> NotificationAction:
        if env == "dev":
            return NotificationAction.SKIP
        return NotificationAction.SEND


class TestUserLogOnlyPolicy(NotificationPolicy):
    def decide(self, user: User, env: str) -> NotificationAction:
        if user.name.startswith("test_"):
            return NotificationAction.LOG_ONLY
        return NotificationAction.SEND
