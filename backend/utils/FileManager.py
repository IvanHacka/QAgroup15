from pathlib import Path
from typing import List, Dict, Any


class FileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def read_json(self, file: str) -> List[Dict[str, Any]]:
        path = Path(self.data_dir, file)
        filePath = self.data_dir / file

        if not filePath.exists():
            return []


        with open(filePath, "r") as f: