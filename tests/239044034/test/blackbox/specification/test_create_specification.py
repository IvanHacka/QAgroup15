import pytest

def test_create_bug_valid_input(bug_controller):
    bug = bug_controller.create(
        title="Login Crash",
        description="Crash occurs on login",
        priority="HIGH",
        status="OPEN",
        tester_id="staff01"
    )
    assert bug.title == "Login Crash"
    assert bug.priority.value == "HIGH"


def test_create_bug_empty_title(bug_controller):
    with pytest.raises(ValueError):
        bug_controller.create("", "desc", "LOW", "OPEN")


def test_create_bug_empty_description(bug_controller):
    with pytest.raises(ValueError):
        bug_controller.create("Title", "", "LOW", "OPEN")
