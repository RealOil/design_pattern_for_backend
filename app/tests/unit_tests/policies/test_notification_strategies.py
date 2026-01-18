from app.repositories.user_repository import User
from app.policies.notification_policy import NotificationAction
from app.policies.notification_strategies import (
    ProdSendPolicy,
    DevSkipPolicy,
    TestUserLogOnlyPolicy,
)


def test_prod_send_policy_sends_in_prod():
    policy = ProdSendPolicy()
    user = User(id=1, name="Alice")

    assert policy.decide(user, "prod") == NotificationAction.SEND


def test_prod_send_policy_skips_in_non_prod():
    policy = ProdSendPolicy()
    user = User(id=1, name="Alice")

    assert policy.decide(user, "dev") == NotificationAction.SKIP


def test_dev_skip_policy_skips_in_dev():
    policy = DevSkipPolicy()
    user = User(id=1, name="Alice")

    assert policy.decide(user, "dev") == NotificationAction.SKIP


def test_dev_skip_policy_sends_in_prod():
    policy = DevSkipPolicy()
    user = User(id=1, name="Alice")

    assert policy.decide(user, "prod") == NotificationAction.SEND


def test_test_user_policy_logs_only_when_name_starts_with_test_prefix():
    policy = TestUserLogOnlyPolicy()
    user = User(id=1, name="test_user_123")

    assert policy.decide(user, "prod") == NotificationAction.LOG_ONLY


def test_test_user_policy_sends_for_normal_user():
    policy = TestUserLogOnlyPolicy()
    user = User(id=1, name="Alice")

    assert policy.decide(user, "prod") == NotificationAction.SEND
