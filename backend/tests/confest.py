import pytest
from backend.services.BugService import BugService
from backend.repo.BugRepo import BugRepo

@pytest.fixture
def bug_repo():
    return BugRepo()

@pytest.fixture
def bug_service(bug_repo):
    return BugService(bug_repo)