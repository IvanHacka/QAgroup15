"""
White-box Testing - Branch Coverage
Function under test: reopen_bug
"""

import pytest
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bug):
        self.bug = bug

    def get_by_id(self, bug_id):
        return self.bug if self.bug and self.bug.id == bug_id else None

    def update(self, bug):
        return True


def make_bug(
    status,
    tester="alice",
    assigned=None,
    reopen_count=0
):
    return Bug(
        title="Bug",
        description="Description long enough",
        status=status,
        priority=BugPriority.HIGH,
        tester_id=tester,
        assigned_to=assigned or [],
        reopen_count=reopen_count
    )


def test_reopen_branch_invalid_status():
    bug = make_bug(BugStatus.OPEN)
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(bug.id, user="alice", reason="valid reason text")


def test_reopen_branch_unauthorized_user():
    bug = make_bug(BugStatus.CLOSED, tester="alice", assigned=["bob"])
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(bug.id, user="charlie", reason="valid reason text")


def test_reopen_branch_invalid_reason():
    bug = make_bug(BugStatus.CLOSED, tester="alice")
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(bug.id, user="alice", reason="short")


def test_reopen_branch_reopen_limit_exceeded():
    bug = make_bug(BugStatus.CLOSED, tester="alice", reopen_count=3)
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(bug.id, user="alice", reason="valid reason text")


def test_reopen_branch_success_creator():
    bug = make_bug(BugStatus.CLOSED, tester="alice")
    service = BugService(FakeBugRepo(bug))

    updated = service.reopen_bug(
        bug.id,
        user="alice",
        reason="this is a valid reopen reason"
    )

    assert updated.status == BugStatus.REOPEN
    assert updated.reopen_count == 1
