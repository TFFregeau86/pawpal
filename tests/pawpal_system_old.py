# tests/test_pawpal.py
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler

def test_task_completion():
    """Verify that marking a task as complete updates its status."""
    pet = Pet("Buddy", "dog", 2)
    task = Task("Feed", "feeding", "08:00")
    pet.add_task(task)
    task.mark_complete()
    assert task.completed is True

def test_add_task_increases_count():
    """Verify that adding a task to a pet increases the task count."""
    pet = Pet("Buddy", "dog", 2)
    initial_count = len(pet.tasks)
    task = Task("Walk", "walk", "09:00")
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1

def test_scheduler_sorting():
    """Verify that tasks are sorted by time and priority."""
    pet = Pet("Buddy", "dog", 2)
    t1 = Task("Morning Walk", "walk", "08:00", priority=1)
    t2 = Task("Feed", "feeding", "07:30", priority=3)
    pet.add_task(t1)
    pet.add_task(t2)
    owner = Owner("Test", "test@test.com")
    owner.add_pet(pet)
    scheduler = Scheduler()
    sorted_tasks = scheduler.generate_daily_schedule(owner)
    # Earliest time first
    assert sorted_tasks[0].title == "Feed"
    assert sorted_tasks[1].title == "Morning Walk"

def test_sort_by_priority_same_time():
    """Verify that tasks at the same time are sorted by descending priority."""
    pet = Pet("Buddy", "dog", 2)
    t1 = Task("Morning Walk", "walk", "08:00", priority=1)
    t2 = Task("Feed", "feeding", "08:00", priority=3)
    pet.add_task(t1)
    pet.add_task(t2)
    owner = Owner("Test", "test@test.com")
    owner.add_pet(pet)
    scheduler = Scheduler()
    sorted_tasks = scheduler.generate_daily_schedule(owner)
    assert sorted_tasks[0].priority > sorted_tasks[1].priority
    assert sorted_tasks[0].title == "Feed"
    assert sorted_tasks[1].title == "Morning Walk"

def test_recurring_task_creation():
    """Verify that completing a recurring task creates a new instance."""
    pet = Pet("Buddy", "dog", 2)
    task = Task("Evening Walk", "walk", "18:00", recurring=True, frequency="daily")
    pet.add_task(task)
    task.mark_complete()
    # After marking complete, should have original completed + new recurring task
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].recurring is True
    assert pet.tasks[1].title == "Evening Walk"

def test_conflict_detection(capsys):
    """Verify that the scheduler detects tasks scheduled at the same time."""
    owner = Owner("Alice", "alice@email.com")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)
    t1 = Task("Morning Walk", "walk", "08:00")
    t2 = Task("Feed Mochi", "feeding", "08:00")  # conflict
    pet.add_task(t1)
    pet.add_task(t2)
    scheduler = Scheduler()
    scheduler.generate_daily_schedule(owner)
    captured = capsys.readouterr()
    assert "overlaps" in captured.out