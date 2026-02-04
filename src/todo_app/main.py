import sys
from typing import Optional
from todo_app.manager import TodoManager
from todo_app.models import TaskStatus

def print_menu():
    """Displays the main menu to the console."""
    print("\n=== Todo App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Completion")
    print("6. Exit")

def get_int_input(prompt: str) -> Optional[int]:
    """
    Safely prompts for an integer input.
    
    Returns:
        Integer if valid, None otherwise.
    """
    try:
        return int(input(prompt))
    except ValueError:
        return None

def add_task_ui(manager: TodoManager):
    """Workflow for adding a new task via user input."""
    print("\n--- Add Task ---")
    title = input("Title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return
    
    description = input("Description: ").strip()
    task = manager.add_task(title, description)
    print(f"Task [{task.id}] created successfully.")

def view_tasks_ui(manager: TodoManager):
    """Workflow for displaying all tasks."""
    print("\n--- Task List ---")
    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status_symbol = "X" if task.status == TaskStatus.COMPLETED else " "
        print(f"[{task.id}] [{status_symbol}] {task.title} - {task.description}")

def update_task_ui(manager: TodoManager):
    """Workflow for updating an existing task's details."""
    print("\n--- Update Task ---")
    task_id = get_int_input("Task ID: ")
    if task_id is None:
        print("Error: Invalid ID.")
        return

    task = manager.get_task_by_id(task_id)
    if not task:
        print(f"Error: Task {task_id} not found.")
        return

    new_title = input(f"New Title (current: {task.title}): ").strip()
    new_desc = input(f"New Description (current: {task.description}): ").strip()

    # Apply changes only if user provided input
    update_title = new_title if new_title else None
    update_desc = new_desc if new_desc else None
    
    manager.update_task(task_id, title=update_title, description=update_desc)
    print(f"Task {task_id} updated successfully.")

def delete_task_ui(manager: TodoManager):
    """Workflow for deleting a task by ID."""
    print("\n--- Delete Task ---")
    task_id = get_int_input("Task ID: ")
    if task_id is None:
        print("Error: Invalid ID.")
        return

    if manager.delete_task(task_id):
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Error: Task {task_id} not found.")

def toggle_completion_ui(manager: TodoManager):
    """Workflow for toggling a task between pending and completed."""
    print("\n--- Toggle Completion ---")
    task_id = get_int_input("Task ID: ")
    if task_id is None:
        print("Error: Invalid ID.")
        return

    task = manager.toggle_task_status(task_id)
    if task:
        print(f"Task {task.id} status changed to {task.status.value}.")
    else:
        print(f"Error: Task {task_id} not found.")

def main():
    """Main entry point of the application."""
    manager = TodoManager()
    
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_task_ui(manager)
        elif choice == "2":
            view_tasks_ui(manager)
        elif choice == "3":
            update_task_ui(manager)
        elif choice == "4":
            delete_task_ui(manager)
        elif choice == "5":
            toggle_completion_ui(manager)
        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
