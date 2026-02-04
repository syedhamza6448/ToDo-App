import pytest
from todo_app.manager import TodoManager
from todo_app.models import TaskStatus

@pytest.fixture
def manager():
    return TodoManager()

def test_initial_state(manager):
    """Test that the manager starts with no tasks."""
    assert len(manager.get_all_tasks()) == 0

def test_add_task(manager):
    """Test adding a task with title and description."""
    task = manager.add_task("Buy Milk", "2%")
    assert task.id == 1
    assert task.title == "Buy Milk"
    assert task.description == "2%"
    assert task.status == TaskStatus.PENDING
    assert len(manager.get_all_tasks()) == 1

def test_add_task_defaults(manager):
    """Test adding a task with default description."""
    task = manager.add_task("Simple Task")
    assert task.title == "Simple Task"
    assert task.description == ""
    assert task.status == TaskStatus.PENDING

def test_get_task_by_id(manager):
    """Test retrieving tasks by ID."""
    manager.add_task("Task 1")
    task_2 = manager.add_task("Task 2")
    
    found = manager.get_task_by_id(2)
    assert found == task_2
    
    not_found = manager.get_task_by_id(99)
    assert not_found is None

def test_update_task_full(manager):
    """Test updating both title and description."""
    manager.add_task("Old Title", "Old Desc")
    updated = manager.update_task(1, title="New Title", description="New Desc")
    
    assert updated.title == "New Title"
    assert updated.description == "New Desc"
    
    # Verify persistence
    fetched = manager.get_task_by_id(1)
    assert fetched.title == "New Title"

def test_update_task_partial(manager):
    """Test updating only title or only description."""
    task = manager.add_task("Old Title", "Old Desc")
    
    # Update title only
    manager.update_task(task.id, title="New Title")
    assert task.title == "New Title"
    assert task.description == "Old Desc"
    
    # Update description only
    manager.update_task(task.id, description="New Desc")
    assert task.title == "New Title"
    assert task.description == "New Desc"

def test_update_nonexistent_task(manager):
    """Test updating a task that doesn't exist."""
    result = manager.update_task(99, title="Ghost")
    assert result is None

def test_delete_task(manager):
    """Test deleting an existing task."""
    manager.add_task("To Delete")
    assert manager.delete_task(1) is True
    assert len(manager.get_all_tasks()) == 0

def test_delete_nonexistent_task(manager):
    """Test deleting a task that doesn't exist."""
    assert manager.delete_task(99) is False

def test_toggle_status(manager):
    """Test toggling task completion status."""
    task = manager.add_task("Toggle Me")
    assert task.status == TaskStatus.PENDING
    
    # Toggle to COMPLETED
    updated = manager.toggle_task_status(1)
    assert updated.status == TaskStatus.COMPLETED
    assert task.status == TaskStatus.COMPLETED
    
    # Toggle back to PENDING
    updated = manager.toggle_task_status(1)
    assert updated.status == TaskStatus.PENDING
    assert task.status == TaskStatus.PENDING

def test_toggle_nonexistent_task(manager):
    """Test toggling a task that doesn't exist."""
    assert manager.toggle_task_status(99) is None