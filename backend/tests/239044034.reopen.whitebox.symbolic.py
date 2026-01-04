import pytest

def test_bug_reopen_symbolic(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    controller.update_status(bug.id, "CLOSED")

    # As len(reason) >= 10
    reason = "S" * 10
    reopened = controller.reopen_bug(bug.id, "staff01", reason)

    # Reopen if constraint satisfy
    assert reopened.reopen_count == 1