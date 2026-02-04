import pytest
from todo_app.manager import TodoManager
from todo_app.models import TaskStatus

@pytest.fixture
def manager():
    return TodoManager()

def test_add_task(manager):
    task = manager.add_task("Buy Milk", "2%")
    assert task.id == 1
    assert task.title == "Buy Milk"
    assert task.description == "2%"
    assert task.status == TaskStatus.PENDING
    assert len(manager.get_all_tasks()) == 1

def test_get_task_by_id(manager):
    manager.add_task("Task 1")
    task_2 = manager.add_task("Task 2")
    
    found = manager.get_task_by_id(2)
    assert found == task_2
    
    not_found = manager.get_task_by_id(99)
    assert not_found is None

def test_update_task(manager):
    manager.add_task("Old Title", "Old Desc")
    updated = manager.update_task(1, title="New Title", description="New Desc")
    
    assert updated.title == "New Title"
    assert updated.description == "New Desc"
    
    # Verify persistence
    fetched = manager.get_task_by_id(1)
    assert fetched.title == "New Title"

def test_delete_task(manager):
    manager.add_task("To Delete")
    assert manager.delete_task(1) is True
    assert len(manager.get_all_tasks()) == 0
    assert manager.delete_task(1) is False

def test_toggle_status(manager):
    task = manager.add_task("Toggle Me")
    assert task.status == TaskStatus.PENDING
    
    manager.toggle_task_status(1)
    assert task.status == TaskStatus.COMPLETED
    
    manager.toggle_task_status(1)
    assert task.status == TaskStatus.PENDING
