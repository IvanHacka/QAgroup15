from typing import Optional, List
from datetime import datetime

from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    # Validation
    def validate_bug(self, bug: Bug) -> Bug:
        if not bug.title or bug.title.strip() == "":
            raise ValueError("Bug title is required")
        if len(bug.title) > 200:
            raise ValueError("Bug title cannot exceed 200 characters")

        if not bug.description or bug.description.strip() == "":
            raise ValueError("Bug description is required")
        if len(bug.description) > 2000:
            raise ValueError("Bug description cannot exceed 2000 characters")

        # Bug.status / Bug.priority 
        if not isinstance(bug.status, BugStatus):
            raise ValueError("Bug status is required")

        if not isinstance(bug.priority, BugPriority):
            raise ValueError("Bug priority is required")

        # screenshot
        if bug.screenshot is None:
            bug.screenshot = []
        if not isinstance(bug.screenshot, list):
            raise ValueError("Screenshot must be a list")

        return bug

    # Read
    def get_bug(self, bug_id: str) -> Bug:
        if not bug_id:
            raise ValueError("Bug ID is required")

        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")

        return bug

    def list_bugs(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> List[Bug]:
        bugs = self.repo.list_all()

        if status:
            bugs = [b for b in bugs if b.status and b.status.value == status]

        if priority:
            bugs = [b for b in bugs if b.priority and b.priority.value == priority]

        if assigned_to:
            # assigned_to by str
            bugs = [b for b in bugs if str(b.assigned_to) == str(assigned_to)]

        return bugs

    # Create
    def create_bug(self, bug: Bug) -> Bug:
        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()
        bug.updated_at = None 

        if self.repo.create(bug):
            return bug

        raise Exception("Failed to create bug")

    # Update (title/description)
    def update_bug_details(
        self,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Bug:
        bug = self.get_bug(bug_id)

        if title is not None:
            bug.title = title
        if description is not None:
            bug.description = description

        # use updated_at，dont use bug.updated
        bug.updated_at = datetime.now().isoformat()

        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug")


    # Update status (for /status route)
    def update_bug_status(self, bug_id: str, new_status: str) -> Bug:
        if not bug_id:
            raise ValueError("Bug id is required")
        if not new_status:
            raise ValueError("Bug status is required")

        bug = self.get_bug(bug_id)

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
        if current in allowed_next and status_enum not in allowed_next[current]:
            raise ValueError(f"Invalid status transition: {current.value} -> {status_enum.value}")

        bug.status = status_enum
        bug.updated_at = datetime.now().isoformat()

        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug status")

    # Assign (for /assign route)
    def assign_bug(self, bug_id: str, assigned_to: int) -> Bug:
        if not assigned_to:
            raise ValueError("assigned_to is required")

        bug = self.get_bug(bug_id)
        bug.assigned_to = assigned_to

        if bug.status == BugStatus.OPEN:
            bug.status = BugStatus.IN_PROGRESS

        bug.updated_at = datetime.now().isoformat()
        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to assign bug")

    # Delete
    def delete_bug(self, bug_id: str) -> bool:
        if not self.repo.delete(bug_id):
            raise ValueError("Bug not found")
        return True

    def count_bugs(self) -> int:
        return self.repo.count()
