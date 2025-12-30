from typing import Optional, List
from datetime import datetime
from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo


class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    # validation
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

    # story29
    def _assert_bug_editable(self, bug: Bug):
        """
        CLOSED / COMPLETED bugs are NOT editable.
        Must REOPEN first.
        """
        if bug.status in (BugStatus.CLOSED, BugStatus.COMPLETED):
            raise ValueError(
                "Bug is CLOSED or COMPLETED. You must REOPEN the bug before editing."
            )

    # read
    def get_bug(self, bug_id: str) -> Bug:
        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")
        return bug

    def list_bugs(self) -> List[Bug]:
        return self.repo.list_all()

    # search
    def search_bugs(self, mode: str, query) -> List[Bug]:
        if not query:
            return self.repo.list_all()

        mode = mode.lower()

        if mode == "id":
            return self.repo.search_by_id(str(query))

        if mode == "title":
            return self.repo.search_by_title(str(query))

        if mode == "status":
            try:
                status = query if isinstance(query, BugStatus) else BugStatus[str(query).upper()]
            except KeyError:
                raise ValueError("Invalid bug status")
            return self.repo.search_by_status(status)

        if mode == "priority":
            try:
                priority = query if isinstance(query, BugPriority) else BugPriority[str(query).upper()]
            except KeyError:
                raise ValueError("Invalid bug priority")
            return self.repo.search_by_priority(priority)

        raise ValueError("Invalid search mode")

    # craete
    def create_bug(self, bug: Bug) -> Bug:
        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()

        if self.repo.create(bug):
            return bug

        raise Exception("Failed to create bug")

    # story 29
    def update_bug_details(
        self,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Bug:

        bug = self.get_bug(bug_id)
        self._assert_bug_editable(bug)

        if title is not None:
            bug.title = title
        if description is not None:
            bug.description = description

        bug.updated_at = datetime.now().isoformat()
        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug")

    # stat update story 29
    def update_bug_status(self, bug_id: str, new_status: str) -> Bug:
        bug = self.get_bug(bug_id)

        try:
            new_status_enum = BugStatus(new_status)
        except ValueError:
            raise ValueError("Invalid bug status")

        # CLOSED / COMPLETED can ONLY go to REOPEN
        if bug.status in (BugStatus.CLOSED, BugStatus.COMPLETED):
            if new_status_enum != BugStatus.REOPEN:
                raise ValueError(
                    "You must REOPEN the bug before changing its status."
                )

        bug.status = new_status_enum
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug status")

    # ---------------- Assign  story 29
    def assign_bug(self, bug_id: str, assigned_to: str) -> Bug:
        bug = self.get_bug(bug_id)
        self._assert_bug_editable(bug)

        if not assigned_to:
            raise ValueError("Bug must be assigned to a user")

        bug.assigned_to = assigned_to
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to assign bug")

    #delete
    def delete_bug(self, bug_id: str) -> bool:
        if not self.repo.delete(bug_id):
            raise ValueError("Bug not found")
        return True

    # reopen , 30 user story
    def reopen_bug(self, bug_id: str, user: str, reason: str) -> Bug:
        """
        Reopen a CLOSED or COMPLETED bug.
        This is the ONLY valid way to restore edit permissions.
        """

        # 1. Bug must exist
        bug = self.get_bug(bug_id)

        # 2. Status check
        if bug.status not in (BugStatus.CLOSED, BugStatus.COMPLETED):
            raise ValueError("Bug is not closed or completed")

        # 3. Authorization
        allowed_users = {bug.assigned_to, bug.tester_id, "staff01", "staff02"}
        if user not in allowed_users:
            raise ValueError("User is not authorized to reopen this bug")

        # 4. Reason required
        if not reason:
            raise ValueError("Reopen reason is required")

        # 5. Reason length
        if len(reason) < 10:
            raise ValueError("Reopen reason must be at least 10 characters")

        # 6. Reopen limit
        if bug.reopen_count >= 3:
            raise ValueError("Reopen limit exceeded")

        # 7. State transition → REOPEN
        bug.status = BugStatus.REOPEN

        # 8. Metadata
        bug.reopen_count += 1
        bug.updated_at = datetime.now().isoformat()

        # 9. Persist
        if self.repo.update(bug):
            return bug

        raise Exception("Failed to reopen bug")
