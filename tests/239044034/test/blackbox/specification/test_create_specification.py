import pytest

def test_create_bug_valid_input(controller):
    bug = controller.create(
        title="Login Crash",
        description="Crash occurs on login",
        priority="HIGH",
        status="OPEN",
        tester_id="staff01"
    )
    assert bug.title == "Login Crash"
    assert bug.priority.value == "HIGH"


def test_create_bug_empty_title(controller):
    with pytest.raises(ValueError):
        controller.create("", "desc", "LOW", "OPEN")


def test_create_bug_empty_description(controller):
    with pytest.raises(ValueError):
        controller.create("Title", "", "LOW", "OPEN")
