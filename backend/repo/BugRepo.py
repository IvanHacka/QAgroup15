import json
import os
from typing import List, Optional
from backend.models.Bug import Bug


class BugRepo:
    def __init__(self, bug_file: str = "data/Bugs.json"):
        self.bug_file = bug_file
        self.data_dir()

    def data_dir(self):
        """Create data directory and file if they don't exist"""
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        if not os.path.exists(self.bug_file):
            with open(self.bug_file, "w") as f:
                json.dump([], f)

    def read_all(self) -> List[dict]:
        """Read all bugs from file"""
        try:
            with open(self.bug_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"{self.bug_file} corruption detected.")
            return []

    def write_all(self, bugs: List[dict]) -> bool:
        """Write all bugs to file"""
        temp_file = self.bug_file + ".temp"
        try:
            with open(temp_file, "w") as f:
                json.dump(bugs, f, indent=2)

            os.replace(temp_file, self.bug_file)
            return True
        except Exception as e:
            print(f"Error writing bugs: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        """Get a single bug by ID"""
        bugs = self.read_all()

        for b in bugs:
            if b["id"] == bug_id:
                return Bug.from_dict(b)
        return None

    def list(self) -> List[Bug]:
        """Get all bugs"""
        bugs_data = self.read_all()
        bugs = []

        for b in bugs_data:
            try:
                bug = Bug.from_dict(b)
                bugs.append(bug)
            except Exception as e:
                print(f"Error parsing bug {b.get('id')}: {e}")
                continue

        return bugs

    def create(self, bug: Bug) -> bool:
        """Create a new bug"""
        bugs = self.read_all()

        # Check if bug ID already exists
        if any(b["id"] == bug.id for b in bugs):
            print(f"Bug {bug.id} already exists.")
            return False

        bugs.append(bug.to_dict())
        return self.write_all(bugs)

    # Might want to display the total number of bugs
    def count(self) -> int:
        return len(self.read_all())