from typing import List, Optional
from .models import Task, TaskStatus

class TodoManager:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = "") -> Task:
        """Creates and stores a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Returns a list of all tasks."""
        return self._tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Finds a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Updates a task's title and/or description."""
        task = self.get_task_by_id(task_id)
        if task:
            task.update(title, description)
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """Removes a task by ID. Returns True if successful."""
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """Toggles a task's status between PENDING and COMPLETED."""
        task = self.get_task_by_id(task_id)
        if task:
            if task.status == TaskStatus.PENDING:
                task.mark_completed()
            else:
                task.mark_pending()
            return task
        return None
