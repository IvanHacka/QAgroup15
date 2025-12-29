from typing import Optional, List
from datetime import datetime
from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    # Validation
    def validate_bug(self, bug: Bug) -> Bug:
        if not bug.title:
            raise ValueError("Bug title is required")
        if len(bug.title) > 200:
            raise ValueError("Bug title cannot exceed 200 characters")

        if not bug.description:
            raise ValueError("Bug description is required")
        if len(bug.description) > 2000:
            raise ValueError("Bug description cannot exceed 2000 characters")

        if not isinstance(bug.status, BugStatus):
            raise ValueError("Bug status is required")

        if not isinstance(bug.priority, BugPriority):
            raise ValueError("Bug priority is required")

        return bug

    # read
    def get_bug(self, bug_id: str) -> Bug:
        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")
        return bug

    def list_bugs(self) -> List[Bug]:
        return self.repo.list_all()

    # Search
    def search_bugs(self, mode: str, query: str) -> List[Bug]:
        if not query:
            return self.repo.list_all()

        if mode == "id":
            return self.repo.search_by_id(query)

        if mode == "title":
            return self.repo.search_by_title(query)

        raise ValueError("Invalid search mode")

    # create
    def create_bug(self, bug: Bug) -> Bug:
        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()
        if self.repo.create(bug):
            return bug
        raise Exception("Failed to create bug")

    # update
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

        bug.updated_at = datetime.now().isoformat()
        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug")

    def delete_bug(self, bug_id: str) -> bool:
        if not self.repo.delete(bug_id):
            raise ValueError("Bug not found")
        return True
