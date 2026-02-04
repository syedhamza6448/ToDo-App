from typing import List, Optional
from .models import Task, TaskStatus

class TodoManager:
    """
    Manages the lifecycle of Todo tasks.
    
    This class handles the creation, retrieval, update, deletion,
    and status toggling of tasks. Currently uses in-memory storage.
    """
    
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = "") -> Task:
        """
        Creates and stores a new task.

        Args:
            title: The short summary of the task.
            description: Detailed information (optional).

        Returns:
            The created Task object.
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Returns a list of all tasks.

        Returns:
            A list of Task objects.
        """
        return self._tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Finds a task by its unique ID.

        Args:
            task_id: The integer ID of the task to find.

        Returns:
            The Task object if found, otherwise None.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Updates a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: The new title (optional).
            description: The new description (optional).

        Returns:
            The updated Task object if found, otherwise None.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.update(title, description)
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Removes a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """
        Toggles a task's status between PENDING and COMPLETED.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated Task object with the new status if found, otherwise None.
        """
        task = self.get_task_by_id(task_id)
        if task:
            if task.status == TaskStatus.PENDING:
                task.mark_completed()
            else:
                task.mark_pending()
            return task
        return None