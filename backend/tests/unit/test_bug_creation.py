import unittest
import pytest
from backend.models.Bug import Bug, BugStatus, BugPriority
import tempfile
import os
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

def test_invalid_status_rejected():
    with pytest.raises(ValueError):
        BugStatus("BROKEN")

def make_service_with_temp_repo():
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, "Bugs.json")
    repo = BugRepo(bug_file=tmp_file)
    service = BugService(repo)
    return service, repo


def test_description_required():
    service, _ = make_service_with_temp_repo()

    bug = Bug(
        title="Button not working",
        description="",  # for empty
        status=BugStatus.OPEN,
        priority=BugPriority.LOW,
        tester_id=1
    )

    with pytest.raises(ValueError, match="Bug description is required"):
        service.create_bug(bug)


def test_description_too_long_rejected():
    service, _ = make_service_with_temp_repo()

    bug = Bug(
        title="Button not working",
        description="a" * 2001,  #this is for too long
        status=BugStatus.OPEN,
        priority=BugPriority.LOW,
        tester_id=1
    )

    with pytest.raises(ValueError):
        service.create_bug(bug)


def test_create_bug_with_description_success():
    service, repo = make_service_with_temp_repo()

    bug = Bug(
        title="Login fails",
        description="Steps: 1) open app 2) login 3) error 500",
        status=BugStatus.OPEN,
        priority=BugPriority.MEDIUM,
        tester_id=1
    )

    created = service.create_bug(bug)


    all_bugs = repo.read_all()
    assert len(all_bugs) == 1
    assert all_bugs[0]["description"] == "Steps: 1) open app 2) login 3) error 500"
    assert created.description == "Steps: 1) open app 2) login 3) error 500"