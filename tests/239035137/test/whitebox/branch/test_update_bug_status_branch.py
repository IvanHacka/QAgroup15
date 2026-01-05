import pytest
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeRepo:
    def __init__(self, bug):
        self.bug = bug

    def get_by_id(self, bug_id):
        return self.bug

    def update(self, bug):
        return True


def make_bug(status):
    return Bug(
        title="Bug",
        description="desc",
        status=status,
        priority=BugPriority.HIGH,
        tester_id="u1",
        assigned_to=[]
    )


def test_branch_invalid_status_string():
    bug = make_bug(BugStatus.OPEN)
    service = BugService(FakeRepo(bug))

    with pytest.raises(ValueError):
        service.update_bug_status(bug.id, "NOT_A_STATUS")

def test_branch_closed_bug_blocked():
    bug = make_bug(BugStatus.CLOSED)
    service = BugService(FakeRepo(bug))

    with pytest.raises(ValueError):
        service.update_bug_status(bug.id, "IN_PROGRESS")

def test_branch_invalid_transition_open_to_failed():
    bug = make_bug(BugStatus.OPEN)
    service = BugService(FakeRepo(bug))

    with pytest.raises(ValueError):
        service.update_bug_status(bug.id, "FAILED")

def test_branch_valid_transition_open_to_closed():
    bug = make_bug(BugStatus.OPEN)
    service = BugService(FakeRepo(bug))

    updated = service.update_bug_status(bug.id, "CLOSED")
    assert updated.status == BugStatus.CLOSED
