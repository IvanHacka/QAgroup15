from datetime import datetime
from typing import Optional, List

from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    def validate_bug(self, bug: Bug) -> Optional[Bug]:
        if not bug.title or len(bug.title) == 0:
            raise ValueError("Bug title is required")
        if len(bug.title) > 200:
            raise ValueError("Bug title can't be exceeding 200 characters")
        if not bug.description or len(bug.description) == 0:
            raise ValueError("Bug description is required")
        if len(bug.description) > 2000:
            raise ValueError("Bug description can't be exceeding 200 characters")

        if not isinstance(bug.status, BugStatus):
            raise ValueError("Bug status is required")
        if not isinstance(bug.priority, BugPriority):
            raise ValueError("Bug priority is required")


    def get_bug(self, bug_id: str) -> Optional[Bug]:
        if not bug_id:
            raise ValueError("Bug id is required")
        return self.repo.get_by_id(bug_id)

    # for filtering
    def list_bugs(self, status: Optional[str], priority: Optional[str],
                  assigned_to: Optional[str]) -> List[Bug]:
        bugs = self.repo.list(status = status)
        # Add other filtering here


        return bugs


    def create_bug(self, bug: Bug) -> Bug:
        """
           Create a new bug with validation

           Args:
               bug: Bug object to create

           Returns:
               Created Bug object

           Raises:
               ValueError: If validation fails
               Exception: If creation fails
       """
        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()
        bug.updated_at = datetime.now().isoformat()

        if self.repo.create(bug):
            return bug
        raise Exception(f"Fail to create bug")

    def assign_bug(self, bug_id: str, assigned_to: int) -> Bug:
        """
            Assign bug to a developer

            Args:
                bug_id: Bug ID (int)
                assigned_to: Developer ID to assign to (int)

            Returns:
                Updated Bug object
        """
        # Waiting for update_bug feature to be completed
        return self.update_bug(assigned_to, bug_id, status = "IN_PROGRESS")

    def delete_bug(self, bug_id: str) -> bool:
        deleted = self.repo.delete(bug_id)
        if not deleted:
            raise ValueError("Bug not found")
        return True
