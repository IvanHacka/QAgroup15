"""
White-box Testing - Branch Coverage
Function under test: _search_by_priority_complex
"""

import pytest
from backend.services.BugService import BugService
from backend.models.Bug import BugPriority



class FakeBugRepo:
    def __init__(self, result):
        self.result = result

    def search_by_priority(self, priority):
        return self.result


def test_priority_branch_none_query():
    service = BugService(FakeBugRepo([]))
    with pytest.raises(ValueError):
        service._search_by_priority_complex(None)


def test_priority_branch_empty_string():
    service = BugService(FakeBugRepo([]))
    with pytest.raises(ValueError):
        service._search_by_priority_complex("")


def test_priority_branch_numeric_string():
    service = BugService(FakeBugRepo([]))
    with pytest.raises(ValueError):
        service._search_by_priority_complex("123")


def test_priority_branch_short_string():
    service = BugService(FakeBugRepo([]))
    with pytest.raises(ValueError):
        service._search_by_priority_complex("H")


def test_priority_branch_invalid_string():
    service = BugService(FakeBugRepo([]))
    with pytest.raises(ValueError):
        service._search_by_priority_complex("URGENT")


def test_priority_branch_enum_input():
    service = BugService(FakeBugRepo([]))
    result = service._search_by_priority_complex(BugPriority.HIGH)
    assert result == []


def test_priority_branch_repo_returns_none():
    class BadRepo:
        def search_by_priority(self, priority):
            return None

    service = BugService(BadRepo())
    with pytest.raises(RuntimeError):
        service._search_by_priority_complex("HIGH")
