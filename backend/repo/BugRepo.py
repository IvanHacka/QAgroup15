import json
import os
from typing import List, Optional

from backend.models.Bug import Bug, BugStatus


class BugRepo:
    def __init__(self, bug_file:str = "data/Bugs.json"):
        self.bug_file = bug_file
        self.data_dir()

    def data_dir(self):
        # Make one if it doesnt exist
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        if not os.path.exists(self.bug_file):
            with open(self.bug_file, "w") as f:
                json.dump({}, f)

    def read_all(self) -> List[Bug]:
        # Read all bugs
        try:
            with open(self.bug_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            print(f"{self.bug_file} corruption detected.")
            return []

    def write_all(self, bugs: List[dict]) -> bool:
        # Write all bugs to the file
        # Using single file approach
        temp_file = self.bug_file + ".temp"
        try:
            with open(temp_file, "w") as f:
                json.dump(bugs, f, indent = 3)

            os.replace(temp_file, self.bug_file)
            return True
        except Exception as e:
            print(e)
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False



    @staticmethod
    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        bugs = self.read_all()

        for b in bugs:
            if b["id"] == bug_id:
                return Bug(
                    id = b["id"],
                    title = b["title"],
                    description = b["description"],
                    status = BugStatus(b["status"]),
                    screenshot = b.get("screenshot", [])
                )
        return None

    @classmethod
    def list(cls) -> list[Bug]:
        bugs = []
        if not os.path.exists(cls.BugFile):
            return bugs

        for file in os.listdir(cls.BugFile):
            if not file.endswith(".json"):
                continue
            path = os.path.join(cls.BugFile, file)

            with open(path, "r") as f:
                data = json.load(f)

            bug = Bug(**data)
            bugs.append(bug)

    @staticmethod
    def save(bug):
        with open(BugFile, "w") as f:
            bugs = json.load(f)
            for b in bugs:
                if b["id"] == bug.id:
                    b["screenshot"] = bug.screenshot
                    temp = BugFile + ".tmp"
                    with open(temp, "w") as f:
                        json.dump(bugs, f, indent=3)

                    os.replace(temp, BugFile)

