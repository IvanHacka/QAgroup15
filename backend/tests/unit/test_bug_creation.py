import pytest
import tempfile
import os

from backend.controllers.UserController import UserController
from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService
from backend.services.UserService import UserService


#-------------------------------------
# Helper functions down here (the order matter btw)

def make_service_with_temp_repo():
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, "Bugs.json")
    repo = BugRepo(bug_file=tmp_file)
    service = BugService(repo)
    return service, repo


def create_sample_bug(service: BugService) -> Bug:
    bug = Bug(
        title="Initial title",
        description="Initial description",
        status=BugStatus.OPEN,
        priority=BugPriority.LOW,
        tester_id=1
    )
    return service.create_bug(bug)

def make_controller():
    service = UserService()
    return UserController(service), service
#-------------------------------------


# Tests for Create Bug (down)

def test_invalid_status_rejected():
    with pytest.raises(ValueError):
        BugStatus("BROKEN")


def test_description_required():
    service, _ = make_service_with_temp_repo()

    bug = Bug(
        title="Button not working",
        description="",
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
        description="a" * 2001,
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
#-------------------------------------

# Tests for Edit Bug (down here)

def test_update_bug_title_and_description_success():
    service, repo = make_service_with_temp_repo()

    created = create_sample_bug(service)
    bug_id = created.id

    updated = service.update_bug_details(
        bug_id=bug_id,
        title="Updated title",
        description="Updated description"
    )

    assert updated.title == "Updated title"
    assert updated.description == "Updated description"

    all_bugs = repo.read_all()
    assert len(all_bugs) == 1
    assert all_bugs[0]["id"] == bug_id
    assert all_bugs[0]["title"] == "Updated title"
    assert all_bugs[0]["description"] == "Updated description"


def test_update_bug_not_found():
    service, _ = make_service_with_temp_repo()

    with pytest.raises(ValueError, match="Bug not found"):
        service.update_bug_details(
            bug_id="NOT_EXIST_ID",
            title="New title"
        )


def test_update_bug_reject_empty_title():
    service, _ = make_service_with_temp_repo()

    created = create_sample_bug(service)

    with pytest.raises(ValueError):
        service.update_bug_details(
            bug_id=created.id,
            title=""
        )


def test_update_bug_reject_empty_description():
    service, _ = make_service_with_temp_repo()

    created = create_sample_bug(service)

    with pytest.raises(ValueError):
        service.update_bug_details(
            bug_id=created.id,
            description=""
        )
#-------------------------------------

#login tests


def test_wrong_username():
    controller, service = make_controller()
    with pytest.raises(ValueError):
        controller.login(username="wrong_username", password="password123")

def test_wrong_password():
    controller, service = make_controller()
    with pytest.raises(ValueError):
        controller.login(username="staff01", password="wrongpassword")
#after 3 incorrect attempts account should be locked
def test_lock_account():
    controller, service = make_controller()
    with pytest.raises(ValueError):
        controller.login(username="staff01", password="wrongpassword")
    with pytest.raises(ValueError):
        controller.login(username="staff01", password="wrongpassword")
    with pytest.raises(ValueError, match="Account is locked due to 3 failed attempts"):
        controller.login(username="staff01", password="wrongpassword")

# Reopen

def test_bug_reopen_valid(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    controller.update_status(bug.id, "CLOSED")

    reopened = controller.reopen(bug.id, "staff01", "A very detailed valid reason")
    assert reopened.status == BugStatus.REOPEN


def test_bug_reopen_reason_short(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    controller.update_status(bug.id, "CLOSED")
    with pytest.raises(Exception):
        controller.reopen(bug.id, "staff01", "bug")


# assign

def test_bug_assign_single_user(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    updated = controller.assign(bug.id, "staff01")
    assert "staff01" in updated.assigned_to


def test_bug_assign_multiple_user(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    updated = controller.assign(bug.id, ["staff01, staff02"]) #List
    assert len(updated.assigned_to) == 2

def test_bug_assign_empty_list(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    with pytest.raises(Exception):
        controller.assign(bug.id, [])


# reopoen symbolci
def test_bug_reopen_symbolic():
    service = BugService()
    bug = service.create_bug("Bug", "This is a test bug", "LOW", tester_id = "staff01")
    service.update_status(bug.id, "CLOSED")

    # As len(reason) >= 10
    reason = "S" * 10
    reopened = service.reopen_bug(bug.id, "staff01", reason)

    # Reopen if constraint satify
    assert reopened.reopen_count == 1