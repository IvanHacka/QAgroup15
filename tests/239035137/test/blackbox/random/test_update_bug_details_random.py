"""
Black-box Testing - Random Testing
Function under test: update_bug_details
"""

import pytest
import random
import string
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bugs=None):
        self.bugs = bugs or []

    def get_by_id(self, bug_id):
        for bug in self.bugs:
            if bug.id == bug_id:
                return bug
        return None

    def update(self, bug):
        return True


def random_string(min_len=5, max_len=20):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def test_random_update_bug_details_multiple_runs():
    """
    Random-based testing:
    Randomly generate valid titles and descriptions and verify no exception is raised.
    """
    bug = Bug(
        title="Initial",
        description="Initial description",
        status=BugStatus.OPEN,
        priority=BugPriority.MEDIUM,
        tester_id="user1",
        assigned_to=[]
    )

    service = BugService(FakeBugRepo([bug]))

    for _ in range(10):  # 10 random trials
        title = random_string()
        description = random_string(10, 50)

        updated = service.update_bug_details(
            bug.id,
            title=title,
            description=description
        )

        assert updated.title == title
        assert updated.description == description
