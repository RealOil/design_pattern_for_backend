from app.services.user_service import UserService
from app.repositories.user_repository import User
from app.policies.notification_policy import NotificationAction


class FakeUserRepo:
    def __init__(self):
        self.saved = []

    def save(self, user: User) -> None:
        self.saved.append(user)


class FakeNotifier:
    def __init__(self):
        self.sent = []

    def send_user_created(self, user: User) -> None:
        self.sent.append(user)


class AlwaysSendPolicy:
    def decide(self, user: User, env: str) -> NotificationAction:
        return NotificationAction.SEND


def test_create_user_calls_notifier_when_policy_says_send(monkeypatch):
    # env 고정(서비스 내부에서 os.getenv를 쓰므로)
    monkeypatch.setenv("APP_ENV", "prod")

    repo = FakeUserRepo()
    notifier = FakeNotifier()
    policy = AlwaysSendPolicy()

    service = UserService(repo, notifier, policy)
    service.create_user(1, "Alice")

    assert len(repo.saved) == 1
    assert len(notifier.sent) == 1


class AlwaysSkipPolicy:
    def decide(self, user: User, env: str) -> NotificationAction:
        return NotificationAction.SKIP


def test_create_user_does_not_call_notifier_when_policy_says_skip(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")

    repo = FakeUserRepo()
    notifier = FakeNotifier()
    policy = AlwaysSkipPolicy()

    service = UserService(repo, notifier, policy)
    service.create_user(1, "Alice")

    assert len(repo.saved) == 1
    assert len(notifier.sent) == 0
