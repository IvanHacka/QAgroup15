import pytest
from backend.services.UserService import UserService


def test_bug_login_success():
    service = UserService()
    user = service.login("staff01", "password123")
    assert user.username == "staff01"
    assert user.attempt == 0


def test_bug_wrong_pw():
    service = UserService()
    with pytest.raises(Exception):
        service.login("staff01", "wrongpassword")

def test_bug_lock():
    service = UserService()
    for _ in range(3):
        try:
            service.login("staff01", "wrongpassword")
        except Exception:
            pass

    with pytest.raises(Exception):
        service.login("staff01", "password123")

def test_bug_no_user():
    service = UserService()
    with pytest.raises(Exception):
        service.login("who", "password123")

