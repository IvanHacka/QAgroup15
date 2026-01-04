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
        mode = mode.lower()

        if query is None or (isinstance(query, str) and query.strip() == ""):
            raise ValueError("Search query cannot be empty")

        # basic story
        if mode == "id":
            return self.repo.search_by_id(str(query))

        if mode == "title":
            if not isinstance(query, str):
                raise ValueError("Keyword must be a string")

            keyword = query.strip()

            if len(keyword) < 2:
                raise ValueError("Keyword too short")

            if len(keyword) > 60:
                raise ValueError("Keyword too long")

            if keyword.isdigit():
                raise ValueError("Keyword cannot be numeric")

            if any(c in keyword for c in "*$%"):
                raise ValueError("Invalid characters in keyword")

            results = self.repo.search_by_title(keyword)

            if not results:
                raise ValueError("No matching bugs found")

            if len(results) > 20:
                return results[:20]

            return results

        if mode == "status":

            if isinstance(query, str):
                query = {
                    "status": query
                }

            bugs = self.repo.list_all()
            results = []

            ##
            status_str = query.get("status")
            include_reopen = query.get("include_reopen", False)
            exclude_completed = query.get("exclude_completed", False)
            priority = query.get("priority")
            assigned_to = query.get("assigned_to")
            created_by = query.get("created_by")
            keyword = query.get("keyword")
            only_active = query.get("only_active", False)

            # validate hee
            if not status_str:
                raise ValueError("Status is required")

            try:
                base_status = BugStatus[status_str.upper()]
            except KeyError:
                raise ValueError("Invalid status value")

            for bug in bugs:

                # 1. base statuss fillter
                if bug.status != base_status:
                    if include_reopen:
                        if not (base_status == BugStatus.OPEN and bug.status == BugStatus.REOPEN):
                            continue
                    else:
                        continue

                # 2. exclude compeleted bugs
                if exclude_completed:
                    if bug.status == BugStatus.COMPLETED:
                        continue

                # 3. only active bugs (OPEN / REOPEN)
                if only_active:
                    if bug.status not in (BugStatus.OPEN, BugStatus.REOPEN):
                        continue

                # 4. priority filter
                if priority:
                    try:
                        if bug.priority != BugPriority[priority.upper()]:
                            continue
                    except KeyError:
                        raise ValueError("Invalid priority value")

                # 5. assigned_to filter
                if assigned_to and assigned_to not in bug.assigned_to:
                    continue

                # 6. created_by filter
                if created_by and bug.tester_id != created_by:
                    continue

                # 7. keyword fillter
                if keyword:
                    kw = keyword.lower()
                    if kw not in bug.title.lower() and kw not in bug.description.lower():
                        continue

                results.append(bug)

            # 8. empty result handling
            if not results:
                raise ValueError("No bugs found with given status policies")

            return results

        if mode == "priority":
            return self._search_by_priority_complex(query)


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
                        if assigned_to not in bug.assigned_to:
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

    def add_comment(self, bug_id: str, user: str, text: str) -> Bug:
        if not text.strip():
            raise ValueError("Comment cannot be empty")

        bug = self.get_bug(bug_id)

        comment = {
            "user": user,
            "text": text,
            "created_at": datetime.now().isoformat()
        }

        bug.comments.append(comment)
        bug.updated_at = datetime.now().isoformat()

        if self.repo.update(bug):
            return bug

        raise Exception("Failed to add comment")
    
    def _search_by_priority_complex(self, query) -> List[Bug]:
        """
        User Story #20:
        Filter bug reports by priority with sufficient cyclomatic complexity.
        """

        # 1 query must exist
        if query is None:
            raise ValueError("Priority query cannot be None")

        # 2 empty string check
        if isinstance(query, str) and query.strip() == "":
            raise ValueError("Priority query cannot be empty")

        # 3️ already enum
        if isinstance(query, BugPriority):
            priority = query

        # 4️ string input
        elif isinstance(query, str):
            normalized = query.strip().upper()

            # 6️ numeric string
            if normalized.isdigit():
                raise ValueError("Priority cannot be numeric")
            
            # 5️ too short
            if len(normalized) < 3:
                raise ValueError("Priority string too short and not valid")

            # 7️ invalid enum name
            if normalized not in BugPriority.__members__:
                raise ValueError("Invalid bug priority")

            priority = BugPriority[normalized]

        # 8️ unsupported type
        else:
            raise TypeError("Unsupported priority query type")

        # 9️ repository failure guard
        bugs = self.repo.search_by_priority(priority)
        if bugs is None:
            raise RuntimeError("Repository returned None")

        # 10 empty result path
        if not bugs:
            return []

        # 1️1 defensive filtering
        filtered = []
        for bug in bugs:
            if bug.priority == priority:
                filtered.append(bug)
            else:
                continue

        return filtered

