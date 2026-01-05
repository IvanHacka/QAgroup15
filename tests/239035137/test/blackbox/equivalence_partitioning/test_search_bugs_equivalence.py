"""
Black-box Testing - Equivalence Partitioning
Function under test: search_bugs

User Stories covered:
- #19 Filter bugs by status
- #21 Filter bugs by developer
- #23 Search bugs by keyword
"""

import pytest
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeBugRepo:
    def __init__(self, bugs):
        self._bugs = bugs

    def list_all(self):
        return self._bugs

    def search_by_id(self, bug_id):
        return []

    def search_by_title(self, keyword):
        return [
            bug for bug in self._bugs
            if keyword.lower() in bug.title.lower()
        ]


def make_bugs():
    return [
        Bug(
            title="Login error",
            description="Login fails on Chrome",
            status=BugStatus.OPEN,
            priority=BugPriority.HIGH,
            tester_id="tester1",
            assigned_to=["alice"]
        ),
        Bug(
            title="UI glitch",
            description="Button misaligned",
            status=BugStatus.CLOSED,
            priority=BugPriority.LOW,
            tester_id="tester2",
            assigned_to=["bob"]
        ),
        Bug(
            title="Performance issue",
            description="Slow loading dashboard",
            status=BugStatus.OPEN,
            priority=BugPriority.MEDIUM,
            tester_id="tester3",
            assigned_to=["alice"]
        ),
    ]


class TestSearchBugsEquivalence:

    def test_equivalence_search_by_status(self):
        """Filter by status (OPEN)"""
        service = BugService(FakeBugRepo(make_bugs()))

        result = service.search_bugs(
            mode="status",
            query={"status": "open"}
        )

        assert all(bug.status == BugStatus.OPEN for bug in result)

    def test_equivalence_search_by_person_assigned_to(self):
        """EC-2: Filter by assigned developer"""
        service = BugService(FakeBugRepo(make_bugs()))

        result = service.search_bugs(
            mode="person",
            query={"assigned_to": "alice"}
        )

        assert all("alice" in bug.assigned_to for bug in result)

    def test_equivalence_search_by_title_keyword(self):
        """ Search by keyword (title mode)"""
        service = BugService(FakeBugRepo(make_bugs()))

        result = service.search_bugs(
            mode="title",
            query="login"
        )

        assert all(
            "login" in bug.title.lower()
            or "login" in bug.description.lower()
            for bug in result
        )

    def test_equivalence_search_status_empty_query(self):
        """EC-4: Empty query should raise ValueError"""
        service = BugService(FakeBugRepo(make_bugs()))

        with pytest.raises(ValueError):
            service.search_bugs(mode="status", query=None)
