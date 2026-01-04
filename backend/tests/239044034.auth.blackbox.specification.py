import pytest


def test_bug_login_success(controller):
    user = controller.login("staff01", "password123")
    assert user.username == "staff01"
    assert user.attempt == 0


def test_bug_wrong_pw(controller):
    with pytest.raises(Exception):
        controller.login("staff01", "wrongpassword")

def test_bug_lock(controller):
    for _ in range(3):
        try:
            controller.login("staff01", "wrongpassword")
        except Exception:
            pass

    with pytest.raises(Exception):
        controller.login("staff01", "password123")

def test_bug_no_user(controller):
    with pytest.raises(Exception):
        controller.login("who", "password123")

