from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    task_type: str
    time: str
    priority: int = 1
    recurring: bool = False
    completed: bool = False

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def reschedule(self, new_time: str):
        """Updates the scheduled time for the task."""
        self.time = new_time


@dataclass
class Pet:
    """Represents a pet owned by the user."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Removes a task from the pet."""
        self.tasks.remove(task)

    def list_tasks(self):
        """Returns all tasks for this pet."""
        return self.tasks


class Owner:
    """Represents the pet owner and manages pets."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

    def view_pets(self):
        """Returns all pets belonging to the owner."""
        return self.pets

    def get_all_tasks(self):
        """Returns tasks across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Organizes and manages tasks across pets."""

    def sort_tasks(self, tasks: List[Task]):
        """Sort tasks by time then priority."""
        return sorted(tasks, key=lambda t: (t.time, -t.priority))

    def detect_conflicts(self, tasks: List[Task]):
        """Find tasks scheduled at the same time."""
        conflicts = []
        seen_times = {}

        for task in tasks:
            if task.time in seen_times:
                conflicts.append((seen_times[task.time], task))
            else:
                seen_times[task.time] = task

        return conflicts

    def generate_daily_schedule(self, owner: Owner):
        """Generate a sorted list of all tasks for the owner."""
        tasks = owner.get_all_tasks()
        return self.sort_tasks(tasks)

"""from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    task_type: str
    time: str
    priority: int = 1
    recurring: bool = False

    def mark_complete(self):
        pass

    def reschedule(self, new_time):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def list_tasks(self):
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def view_pets(self):
        pass


class Scheduler:

    def sort_tasks(self, tasks: List[Task]):
        pass

    def detect_conflicts(self, tasks: List[Task]):
        pass

    def generate_daily_schedule(self, pets: List[Pet]):
        pass"""