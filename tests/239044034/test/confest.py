import pytest
from backend.services.BugService import BugService
from backend.repo.BugRepo import BugRepo

@pytest.fixture
def controller():
    repo = BugRepo()              # real or in-memory repo
    service = BugService(repo)    # BugService REQUIRES repo
    return service