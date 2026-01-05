"""
White-box Testing - Statement Coverage
Function under test: _search_by_priority_complex
"""

from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bugs):
        self._bugs = bugs

    def search_by_priority(self, priority):
        return self._bugs


def make_bugs():
    return [
        Bug(
            title="Bug A",
            description="Desc",
            status=BugStatus.OPEN,
            priority=BugPriority.HIGH,
            tester_id="u1",
            assigned_to=[]
        ),
        Bug(
            title="Bug B",
            description="Desc",
            status=BugStatus.CLOSED,
            priority=BugPriority.HIGH,
            tester_id="u2",
            assigned_to=[]
        ),
    ]


def test_priority_statement_valid_string():
    """
    Statement coverage:
    Valid string input should execute the main path.
    """
    service = BugService(FakeBugRepo(make_bugs()))

    result = service._search_by_priority_complex("HIGH")

    assert len(result) == 2
    assert all(bug.priority == BugPriority.HIGH for bug in result)
