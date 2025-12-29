import json
import os
from typing import List, Optional
from backend.models.Bug import Bug


class BugRepo:
    def __init__(self, bug_file: str = "data/Bugs.json"):
        self.bug_file = bug_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        if not os.path.exists(self.bug_file):
            with open(self.bug_file, "w") as f:
                json.dump([], f)

    def read_all(self) -> List[dict]:
        try:
            with open(self.bug_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_all(self, bugs: List[dict]) -> bool:
        try:
            with open(self.bug_file, "w") as f:
                json.dump(bugs, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing bugs: {e}")
            return False

    # CRUD
    def create(self, bug: Bug) -> bool:
        bugs = self.read_all()
        if any(b["id"] == bug.id for b in bugs):
            return False
        bugs.append(bug.to_dict())
        return self.write_all(bugs)

    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        for b in self.read_all():
            if b.get("id") == bug_id:
                return Bug.from_dict(b)
        return None

    def list_all(self) -> List[Bug]:
        bugs: List[Bug] = []
        for b in self.read_all():
            try:
                bugs.append(Bug.from_dict(b))
            except Exception as e:
                print(f"Skipping invalid bug record {b.get('id')}: {e}")
        return bugs

    def update(self, bug: Bug) -> bool:
        bugs = self.read_all()
        for i, b in enumerate(bugs):
            if b.get("id") == bug.id:
                bugs[i] = bug.to_dict()
                return self.write_all(bugs)
        return False

    def delete(self, bug_id: str) -> bool:
        bugs = self.read_all()
        new_bugs = [b for b in bugs if b.get("id") != bug_id]
        if len(new_bugs) == len(bugs):
            return False
        return self.write_all(new_bugs)

    # Search here
    def search_by_id(self, keyword: str) -> List[Bug]:
        return [
            Bug.from_dict(b)
            for b in self.read_all()
            if keyword.lower() in b.get("id", "").lower()
        ]

    def search_by_title(self, keyword: str) -> List[Bug]:
        return [
            Bug.from_dict(b)
            for b in self.read_all()
            if keyword.lower() in b.get("title", "").lower()
        ]
