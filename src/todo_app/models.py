from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def mark_completed(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_pending(self) -> None:
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.now()
        
    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        if title:
            self.title = title
        if description is not None: # Allow empty string to clear description if needed, or just update
            self.description = description
        self.updated_at = datetime.now()
