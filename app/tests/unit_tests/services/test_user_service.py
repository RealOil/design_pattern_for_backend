from app.services.user_service import UserService
from app.repositories.user_repository import User

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

def test_create_user_orchestrates_save_and_notify():
    repo = FakeUserRepo()
    notifier = FakeNotifier()
    service = UserService(repo, notifier)

    service.create_user(1, "Alice")

    assert len(repo.saved) == 1
    assert repo.saved[0].name == "Alice"
    assert len(notifier.sent) == 1
    assert notifier.sent[0].id == 1