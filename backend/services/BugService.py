from datetime import datetime
from typing import Optional, List

from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo


    # Validation
    def validate_bug(self, bug: Bug) -> None:
        if not bug.title or len(bug.title) == 0:
            raise ValueError("Bug title is required")
        if len(bug.title) > 200:
            raise ValueError("Bug title can't exceed 200 characters")

        if not bug.description or len(bug.description) == 0:
            raise ValueError("Bug description is required")
        if len(bug.description) > 2000:
            raise ValueError("Bug description can't exceed 2000 characters")

        if not isinstance(bug.status, BugStatus):
            raise ValueError("Bug status is required")
        if not isinstance(bug.priority, BugPriority):
            raise ValueError("Bug priority is required")

    # getters
    def get_bug(self, bug_id: str) -> Optional[Bug]:
        if not bug_id:
            raise ValueError("Bug id is required")
        return self.repo.get_by_id(bug_id)

    # Create
    def create_bug(self, bug: Bug) -> Bug:
        self.validate_bug(bug)

        bug.created = datetime.now().isoformat()
        bug.updated = datetime.now().isoformat()

        if self.repo.create(bug):
            return bug

        raise Exception("Fail to create bug")

    # Update title / description  (#6)
    def update_bug_details(
        self,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Bug:

        if not bug_id:
            raise ValueError("Bug id is required")

        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")

        if title is not None:
            bug.title = title
        if description is not None:
            bug.description = description

        bug.updated = datetime.now().isoformat()
        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Fail to update bug")

    # Assign bug to developer
    def assign_bug(self, bug_id: str, assigned_to: int) -> Bug:
        if not bug_id:
            raise ValueError("Bug id is required")
        if assigned_to is None:
            raise ValueError("assigned_to is required")

        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")

        bug.assigned_to = int(assigned_to)
        bug.status = BugStatus.IN_PROGRESS
        bug.updated = datetime.now().isoformat()

        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Fail to assign bug")

    # Update status  (#13)
    def update_bug_status(self, bug_id: str, new_status: str) -> Bug:
        if not bug_id:
            raise ValueError("Bug id is required")
        if not new_status:
            raise ValueError("Bug status is required")

        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")

        try:
            status_enum = BugStatus(new_status)
        except ValueError:
            raise ValueError("Invalid bug status")

        allowed_next = {
            BugStatus.OPEN: {BugStatus.OPEN, BugStatus.IN_PROGRESS},
            BugStatus.IN_PROGRESS: {BugStatus.IN_PROGRESS, BugStatus.COMPLETED, BugStatus.FAILED},
            BugStatus.COMPLETED: {BugStatus.COMPLETED, BugStatus.CLOSED},
            BugStatus.FAILED: {BugStatus.FAILED, BugStatus.CLOSED},
            BugStatus.CLOSED: {BugStatus.CLOSED},
        }

        current = bug.status
        if status_enum not in allowed_next.get(current, set()):
            raise ValueError(
                f"Invalid status transition: {current.value} -> {status_enum.value}"
            )

        bug.status = status_enum
        bug.updated = datetime.now().isoformat()

        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Fail to update bug status")

    # View bugs assigned to developer  (#12)
    def get_bugs_assigned_to(
        self,
        developer_id: int,
        include_closed: bool = False
    ) -> List[Bug]:

        if developer_id is None:
            raise ValueError("Developer id is required")

        all_bugs = self.repo.read_all()
        result: List[Bug] = []

        for b in all_bugs:
            bug = Bug.parse_from_dict(b) if isinstance(b, dict) else b

            if bug.assigned_to == developer_id:
                if not include_closed and bug.status == BugStatus.CLOSED:
                    continue
                result.append(bug)

        return result
