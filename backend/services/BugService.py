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
    def search_bugs(self, mode: str, query) -> List[Bug]:
        if not query:
            return self.repo.list_all()

        mode = mode.lower()

        # search by id
        if mode == "id":
            return self.repo.search_by_id(str(query))

        # search by tittle
        if mode == "title":
            return self.repo.search_by_title(str(query))

        # search by status
        if mode == "status":
            if isinstance(query, BugStatus):
                status = query
            else:
                try:
                    status = BugStatus[str(query).upper()]
                except KeyError:
                    raise ValueError("Invalid bug status")

            return self.repo.search_by_status(status)

        # search by priority
        if mode == "priority":
            if isinstance(query, BugPriority):
                priority = query
            else:
                try:
                    priority = BugPriority[str(query).upper()]
                except KeyError:
                    raise ValueError("Invalid bug priority")

            return self.repo.search_by_priority(priority)

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

    def update_bug_status(self, bug_id: str, new_status: str) -> Bug:
        bug = self.get_bug(bug_id)

        try:
            bug.status = BugStatus(new_status)
        except ValueError:
            raise ValueError("Invalid bug status")

        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to update bug status")

    def assign_bug(self, bug_id: str, assigned_to: str) -> Bug:
        bug = self.get_bug(bug_id)

        if not assigned_to:
            raise ValueError("Bug need to be assigned to a user")

        bug.assigned_to = assigned_to
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug
        raise Exception("Failed to assign bug")

    def delete_bug(self, bug_id: str) -> bool:
        if not self.repo.delete(bug_id):
            raise ValueError("Bug not found")
        return True
    
    #reopen #30 !ha
    def reopen_bug(self, bug_id: str, user: str, reason: str) -> Bug:

    #Reopen a closed or completed bug under strict conditions.
    #This method is intentionally designed with high cyclomatic complexity
    #for white-box testing and symbolic execution.
    #dont del my comments pls.


    # 1. Bug must exist
        bug = self.get_bug(bug_id)

        # 2. Bug status must be CLOSED or COMPLETED
        if bug.status not in (BugStatus.CLOSED, BugStatus.COMPLETED):
            raise ValueError("Bug is not closed or completed")

        # 3. User authorization
        allowed_users = {"staff01", "staff02", bug.assigned_to}

        if user not in allowed_users:
         raise ValueError("User is not authorized")


        # 4. Reason must exist
        if not reason:
            raise ValueError("Reopen reason is required")

        # 5. Reason length validation
        if len(reason) < 10:
            raise ValueError("Reopen reason must be at least 10 characters")

        # 6. Reopen count limit
        if bug.reopen_count >= 3:
            raise ValueError("Reopen limit exceeded")

        # 7. State transition logic
        if bug.status == BugStatus.COMPLETED:
            bug.status = BugStatus.IN_PROGRESS
        elif bug.status == BugStatus.CLOSED:
            bug.status = BugStatus.OPEN
        else:
            # Defensive programming (should never happen)
            raise ValueError("Invalid state transition")

        # 8. Update metadata
        bug.reopen_count += 1
        bug.updated_at = datetime.now().isoformat()

        # 9. Persist changes
        if self.repo.update(bug):
            return bug

        # 10. Persistence failure
        raise Exception("Failed to reopen bug")
    
