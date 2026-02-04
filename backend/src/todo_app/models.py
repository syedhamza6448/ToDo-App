from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    """Enumeration for Task completion states."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

@dataclass
class Task:
    """
    Represents a single Todo task.
    
    Attributes:
        id: Unique identifier.
        title: Short summary.
        description: Detailed info (optional).
        status: PENDING or COMPLETED.
        created_at: Creation timestamp.
        updated_at: Last modification timestamp.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def mark_completed(self) -> None:
        """Sets status to COMPLETED and updates timestamp."""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_pending(self) -> None:
        """Sets status to PENDING and updates timestamp."""
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.now()
        
    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Updates task attributes if provided.
        
        Args:
            title: New title (if not None).
            description: New description (if not None).
        """
        if title:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()