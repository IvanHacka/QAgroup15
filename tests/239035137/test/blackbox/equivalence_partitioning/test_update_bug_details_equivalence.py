"""
Black-box Testing - Equivalence Partitioning
Function under test: update_bug_details

User Stories covered:
- #2 Add description and steps
- #6 Edit bug details after creation
- #29 Prevent editing when bug is closed (implicitly via validation)
"""

import pytest
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


def make_open_bug():
    return Bug(
        title="Valid title",
        description="Valid description",
        status=BugStatus.OPEN,
        priority=BugPriority.MEDIUM,
        tester_id="user1",
        assigned_to=[]
    )


def test_equivalence_valid_title_and_description():
    """
    Equivalence Class: Valid title & valid description
    Expected: Update succeeds
    """
    bug = make_open_bug()
    service = BugService(FakeBugRepo([bug]))

    updated = service.update_bug_details(
        bug.id,
        title="New valid title",
        description="New valid description"
    )

    assert updated.title == "New valid title"
    assert updated.description == "New valid description"


def test_equivalence_invalid_empty_title():
    """
    Equivalence Class: Empty title
    Expected: ValueError
    """
    bug = make_open_bug()
    service = BugService(FakeBugRepo([bug]))

    with pytest.raises(ValueError):
        service.update_bug_details(
            bug.id,
            title="",
            description="Still valid description"
        )


def test_equivalence_invalid_empty_description():
    """
    Equivalence Class: Empty description
    Expected: ValueError
    """
    bug = make_open_bug()
    service = BugService(FakeBugRepo([bug]))

    with pytest.raises(ValueError):
        service.update_bug_details(
            bug.id,
            title="Valid title",
            description=""
        )


def test_equivalence_bug_not_found():
    """
    Equivalence Class: Bug does not exist
    Expected: ValueError
    """
    service = BugService(FakeBugRepo([]))

    with pytest.raises(ValueError):
        service.update_bug_details(
            "non-existent-id",
            title="Valid title",
            description="Valid description"
        )
