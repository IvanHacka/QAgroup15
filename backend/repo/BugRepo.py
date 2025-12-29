import json
import os
from typing import List, Optional

from backend.models.Bug import Bug, BugStatus, BugPriority


class BugRepo:
    """
    Repository layer for Bug persistence.
    Uses a JSON file as storage.
    """

    def __init__(self, file_path: str = "data/bugs.json"):
        self.file_path = file_path

        # Ensure data directory & file exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)


    def _load(self) -> List[Bug]:
        with open(self.file_path, "r") as f:
            raw = json.load(f)

        bugs = []
        for item in raw:
            bugs.append(Bug.from_dict(item))
        return bugs

    def _save(self, bugs: List[Bug]) -> None:
        with open(self.file_path, "w") as f:
            json.dump([b.to_dict() for b in bugs], f, indent=2)

    # read

    def list_all(self) -> List[Bug]:
        return self._load()

    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        for bug in self._load():
            if bug.id == bug_id:
                return bug
        return None

    # search

    def search_by_id(self, bug_id: str) -> List[Bug]:
        bug = self.get_by_id(bug_id)
        return [bug] if bug else []

    def search_by_title(self, keyword: str) -> List[Bug]:
        keyword = keyword.lower()
        return [
            bug for bug in self._load()
            if keyword in bug.title.lower()
        ]

    def search_by_status(self, status: BugStatus) -> List[Bug]:
        return [
            bug for bug in self._load()
            if bug.status == status
        ]

    def search_by_priority(self, priority: BugPriority) -> List[Bug]:
        return [
            bug for bug in self._load()
            if bug.priority == priority
        ]

    # create

    def create(self, bug: Bug) -> bool:
        bugs = self._load()
        bugs.append(bug)
        self._save(bugs)
        return True

    # update

    def update(self, updated_bug: Bug) -> bool:
        bugs = self._load()
        for i, bug in enumerate(bugs):
            if bug.id == updated_bug.id:
                bugs[i] = updated_bug
                self._save(bugs)
                return True
        return False

    #deletee

    def delete(self, bug_id: str) -> bool:
        bugs = self._load()
        new_bugs = [bug for bug in bugs if bug.id != bug_id]

        if len(new_bugs) == len(bugs):
            return False

        self._save(new_bugs)
        return True
