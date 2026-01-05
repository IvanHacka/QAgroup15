import pytest

from backend.controllers.BugController import BugController
from backend.services.BugService import BugService
from backend.repo.BugRepo import BugRepo

@pytest.fixture
def controller():
    repo = BugRepo()
    service = BugService(repo)
    controller = BugController(service)
    return controller