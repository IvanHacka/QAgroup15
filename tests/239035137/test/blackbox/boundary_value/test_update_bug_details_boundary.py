"""
Black-box Testing - Boundary Value Analysis
Function under test: update_bug_details

User Stories covered:
- #2 Add description and steps
- #6 Edit bug details after creation
- #29 Prevent editing when bug is closed (boundary condition tested here)
"""

import pytest
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


# for unit-style black-box testing
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


# create a valid OPEN bug
def make_open_bug():
    return Bug(
        title="Initial title",
        description="Initial description",
        status=BugStatus.OPEN,           # Boundary: editable status
        priority=BugPriority.LOW,
        tester_id="user1",
        assigned_to=[]
    )


# test caes
def test_update_bug_details_open_bug_success():
    """
    Boundary Value:
    Bug status = OPEN (editable boundary)

    Expected:
    - Title and description should be updated successfully
    """
    bug = make_open_bug()
    repo = FakeBugRepo([bug])
    service = BugService(repo)

    updated_bug = service.update_bug_details(
        bug_id=bug.id,
        title="Updated title",
        description="Updated description with enough length"
    )

    assert updated_bug.title == "Updated title"
    assert updated_bug.description == "Updated description with enough length"

def test_update_bug_details_closed_bug_fail():
    """
    Boundary Value:
    Bug status = CLOSED (non-editable boundary)

    Expected:
    - Updating details should raise ValueError
    """
    bug = Bug(
        title="Initial title",
        description="Initial description",
        status=BugStatus.CLOSED,          # Boundary: non-editable
        priority=BugPriority.LOW,
        tester_id="user1",
        assigned_to=[]
    )

    repo = FakeBugRepo([bug])
    service = BugService(repo)

    with pytest.raises(ValueError):
        service.update_bug_details(
            bug_id=bug.id,
            title="New title",
            description="New description"
        )
