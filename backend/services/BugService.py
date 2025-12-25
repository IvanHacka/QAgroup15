from typing import Optional, List
from datetime import datetime
from backend.models.Bug import Bug
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    def create_bug(self, bug: Bug) -> Bug:
        """
        Create a new bug - only ID is saved

        Args:
            bug: Bug object (ID will be auto-generated if not provided)

        Returns:
            Created Bug object with ID

        Raises:
            Exception: If creation fails
        """
        # Update timestamp
        bug.created_at = datetime.now().isoformat()

        if self.repo.create(bug):
            return bug

        raise Exception("Failed to create bug")

    def get_bug(self, bug_id: str) -> Optional[Bug]:
        """Get a bug by ID"""
        if not bug_id:
            raise ValueError("Bug ID is required")
        return self.repo.get_by_id(bug_id)

    def list_bugs(self) -> List[Bug]:
        """Get all bugs"""
        return self.repo.list()

    def count_bugs(self) -> int:
        """Get total number of bugs"""
        return self.repo.count()