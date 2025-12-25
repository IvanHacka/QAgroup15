import tempfile
import os

from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


def make_service_with_temp_repo():
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, "Bugs.json")
    repo = BugRepo(bug_file=tmp_file)
    service = BugService(repo)
    return service, repo

def test_get_bugs_assigned_to_developer():
    service, repo = make_service_with_temp_repo()

    # create 3rd bugs
    bug1 = Bug(
        title="Bug 1",
        description="desc 1",
        status=BugStatus.OPEN,
        priority=BugPriority.LOW,
        tester_id=1
    )
    bug1.assigned_to = 1

    bug2 = Bug(
        title="Bug 2",
        description="desc 2",
        status=BugStatus.IN_PROGRESS,
        priority=BugPriority.MEDIUM,
        tester_id=1
    )
    bug2.assigned_to = 1

    bug3 = Bug(
        title="Bug 3",
        description="desc 3",
        status=BugStatus.OPEN,
        priority=BugPriority.HIGH,
        tester_id=1
    )
    bug3.assigned_to = 2  # asigns to a random develooper

    # repo
    service.create_bug(bug1)
    service.create_bug(bug2)
    service.create_bug(bug3)

    #function
    result = service.get_bugs_assigned_to(developer_id=1)

    assert len(result) == 2
    assert all(b.assigned_to == 1 for b in result)
