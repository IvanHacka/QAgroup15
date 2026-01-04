from backend.services.BugService import BugService


def test_bug_reopen_symbolic():
    service = BugService()
    bug = service.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    service.update_status(bug.id, "CLOSED")

    # As len(reason) >= 10
    reason = "S" * 10
    reopened = service.reopen_bug(bug.id, "staff01", reason)

    # Reopen if constraint satify
    assert reopened.reopen_count == 1