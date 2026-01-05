from backend.services.BugService import BugService
from backend.models.Bug import Bug, BugStatus, BugPriority


class FakeRepo:
    def __init__(self, bug):
        self.bug = bug

    def get_by_id(self, bug_id):
        return self.bug

    def update(self, bug):
        return True


def test_update_bug_status_statement_open_to_in_progress():
    bug = Bug(
        title="Bug",
        description="desc",
        status=BugStatus.OPEN,
        priority=BugPriority.HIGH,
        tester_id="u1",
        assigned_to=[]
    )

    service = BugService(FakeRepo(bug))
    updated = service.update_bug_status(bug.id, "IN_PROGRESS")

    assert updated.status == BugStatus.IN_PROGRESS
