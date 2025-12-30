from typing import Optional, List, Dict
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

    # story 29
    def _assert_bug_editable(self, bug: Bug):
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


    # user story 21
    def search_bugs(self, mode: str, query) -> List[Bug]:
        """
        Extended search:
        - id
        - title
        - status
        - priority
        - person (created_by / assigned_to)
        """

        if not query:
            return self.repo.list_all()

        mode = mode.lower()

        # basic story
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

        # search by ppl
        if mode == "person":
            """
            query is expected to be a dict:
            {
                "created_by": Optional[str],
                "assigned_to": Optional[str],
                "include_unassigned": bool,
                "exclude_closed": bool,
                "same_person": bool,
                "keyword": Optional[str]
            }
            """

            bugs = self.repo.list_all()
            results = []

            created_by = query.get("created_by")
            assigned_to = query.get("assigned_to")
            include_unassigned = query.get("include_unassigned", False)
            exclude_closed = query.get("exclude_closed", False)
            same_person = query.get("same_person", False)
            keyword = query.get("keyword")

            for bug in bugs:
                # create geh filter
                if created_by and bug.tester_id != created_by:
                    continue

                #assigned_to filter
                if assigned_to:
                    if include_unassigned:
                        if bug.assigned_to not in (assigned_to, None):
                            continue
                    else:
                        if bug.assigned_to != assigned_to:
                            continue

                # same creator & assignee
                if same_person:
                    if not bug.tester_id or bug.tester_id != bug.assigned_to:
                        continue

                # exclude closed/completed
                if exclude_closed:
                    if bug.status in (BugStatus.CLOSED, BugStatus.COMPLETED):
                        continue

                # keyword search (optional)
                if keyword:
                    kw = keyword.lower()
                    if kw not in bug.title.lower() and kw not in bug.description.lower():
                        continue

                results.append(bug)

            return results

        # -fallback
        raise ValueError("Invalid search mode")

    # create
    def create_bug(self, bug: Bug) -> Bug:
        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()

        if self.repo.create(bug):
            return bug

        raise Exception("Failed to create bug")

    # update deatails 29
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

    # user story 29 and 30
    def update_bug_status(self, bug_id: str, new_status: str) -> Bug:
        bug = self.get_bug(bug_id)

        try:
            new_status_enum = BugStatus(new_status)
        except ValueError:
            raise ValueError("Invalid bug status")

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

    # assign 29
    def assign_bug(self, bug_id: str, users: List[str]) -> Bug:

        if not isinstance(users, list):
            raise TypeError("Assigned users must be a list or usernames")

        if len(users) == 0:
            raise ValueError("Bug must be assigned to a user")

        bug = self.get_bug(bug_id)
        self._assert_bug_editable(bug)

        if bug.assigned_to == None:
            bug.assigned_to = []

        empty_users = []
        for user in users:
            if not isinstance(user, str):
                raise TypeError("Assigned users must be a string")
            if "," in user:
                raise ValueError("Each user should be a single username")
            if not user in empty_users:
                empty_users.append(user)


        bug.assigned_to = empty_users
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to assign bug")

    # delete
    def delete_bug(self, bug_id: str) -> bool:
        if not self.repo.delete(bug_id):
            raise ValueError("Bug not found")
        return True

    # reopen user story 30
    def reopen_bug(self, bug_id: str, user: str, reason: str) -> Bug:
        bug = self.get_bug(bug_id)

        if bug.status not in (BugStatus.CLOSED, BugStatus.COMPLETED):
            raise ValueError("Bug is not closed or completed")

        allowed_users = {bug.assigned_to, bug.tester_id, "staff01", "staff02"}
        if user not in allowed_users:
            raise ValueError("User is not authorized to reopen this bug")

        if not reason or len(reason) < 10:
            raise ValueError("Reopen reason must be at least 10 characters")

        if bug.reopen_count >= 3:
            raise ValueError("Reopen limit exceeded")

        bug.status = BugStatus.REOPEN
        bug.reopen_count += 1
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to reopen bug")

    def mark_duplicate(self, bug_id: str, original_id: str) -> Bug: #user story 33
        bug = self.get_bug(bug_id)
        original = self.get_bug(original_id)

        if bug_id == original_id:
            raise ValueError("A bug cannot be a duplicate of itself")

        bug.status = BugStatus.DUPLICATE
        bug.duplicate_of = original.id
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug
        raise Exception("Failed to mark duplicate")

