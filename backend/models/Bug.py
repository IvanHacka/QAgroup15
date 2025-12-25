from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Bug:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: dict) -> "Bug":
        return Bug(
            id=data["id"],
            created_at=data.get("created_at", datetime.now().isoformat())
        )