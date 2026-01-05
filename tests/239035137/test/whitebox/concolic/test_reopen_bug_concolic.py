"""
White-box Testing - Concolic Testing
Function: reopen_bug

Concrete execution + symbolic path negation
"""

import pytest
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bug):
        self.bug = bug

    def get_by_id(self, bug_id):
        return self.bug if self.bug.id == bug_id else None

    def update(self, bug):
        return True


def make_bug(status, tester="alice", assigned=None, reopen_count=0):
    return Bug(
        title="Bug",
        description="Valid description",
        status=status,
        priority=BugPriority.HIGH,
        tester_id=tester,
        assigned_to=assigned or [],
        reopen_count=reopen_count
    )


def test_concolic_success_path():
    """
    Concrete input triggers success path.
    Path condition:
    status ∈ {CLOSED, COMPLETED} ∧ authorized ∧ len(reason) ≥ 10 ∧ reopen_count < 3
    """
    bug = make_bug(BugStatus.CLOSED)
    service = BugService(FakeBugRepo(bug))

    result = service.reopen_bug(
        bug.id,
        user="alice",
        reason="this is a valid reopen reason"
    )

    assert result.status == BugStatus.REOPEN


def test_concolic_negate_authorization():
    """
    Negated path condition: ¬authorized
    """
    bug = make_bug(BugStatus.CLOSED, tester="alice")
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(
            bug.id,
            user="charlie",
            reason="this is a valid reopen reason"
        )


def test_concolic_negate_reason_length():
    """
    Negated path condition: len(reason) < 10
    """
    bug = make_bug(BugStatus.CLOSED)
    service = BugService(FakeBugRepo(bug))

    with pytest.raises(ValueError):
        service.reopen_bug(
            bug.id,
            user="alice",
            reason="short"
        )
