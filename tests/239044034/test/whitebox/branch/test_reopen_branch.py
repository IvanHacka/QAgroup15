import pytest
from backend.models.Bug import BugStatus

def test_bug_reopen_valid(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    controller.update_status(bug.id, "CLOSED")

    reopened = controller.reopen(bug.id, "staff01", "A very detailed valid reason")
    assert reopened.status == BugStatus.REOPEN


def test_bug_reopen_reason_short(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    controller.update_status(bug.id, "CLOSED")
    with pytest.raises(Exception):
        controller.reopen(bug.id, "staff01", "bug")