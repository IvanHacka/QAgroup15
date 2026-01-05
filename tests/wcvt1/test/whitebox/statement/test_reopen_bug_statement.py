"""
White-box Testing - Statement Coverage
Function under test: reopen_bug
"""

from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bug):
        self.bug = bug

    def get_by_id(self, bug_id):
        return self.bug

    def update(self, bug):
        return True


def test_reopen_bug_statement_happy_path():
    bug = Bug(
        title="Bug",
        description="Long enough description",
        status=BugStatus.CLOSED,
        priority=BugPriority.HIGH,
        tester_id="alice",
        assigned_to=[],
        reopen_count=0
    )

    service = BugService(FakeBugRepo(bug))

    updated = service.reopen_bug(
        bug.id,
        user="alice",
        reason="this is a valid reopen reason"
    )

    assert updated.status == BugStatus.REOPEN
    assert updated.reopen_count == 1
