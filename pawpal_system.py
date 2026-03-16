# pawpal_system.py
from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timedelta

@dataclass
class Task:
    title: str
    task_type: str
    time: str  # "HH:MM"
    priority: int = 1
    recurring: bool = False
    completed: bool = False
    frequency: str = None  # e.g., "daily"
    pet: 'Pet' = None

    def mark_complete(self):
        """Mark task complete and create a new recurring task if needed."""
        self.completed = True
        if self.recurring and self.frequency == "daily":
            next_day_time = datetime.strptime(self.time, "%H:%M") + timedelta(days=1)
            new_time_str = next_day_time.strftime("%H:%M")
            new_task = Task(
                title=self.title,
                task_type=self.task_type,
                time=new_time_str,
                priority=self.priority,
                recurring=True,
                frequency=self.frequency,
                pet=self.pet
            )
            if self.pet:
                self.pet.add_task(new_task)

    def reschedule(self, new_time: str):
        self.time = new_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task):
        self.tasks.remove(task)

    def list_tasks(self):
        return self.tasks


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def view_pets(self):
        return self.pets

    def get_all_tasks(self):
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    def sort_tasks(self, tasks: List[Task]):
        """Sort tasks by time (HH:MM) and descending priority."""
        return sorted(tasks, key=lambda t: (t.time, -t.priority))

    def detect_conflicts(self, tasks: List[Task]):
        """Return a list of tuples of conflicting Task objects."""
        conflicts = []
        seen_times = {}
        for task in tasks:
            key = (task.time, task.pet.name if task.pet else "")
            if key in seen_times:
                conflicts.append((seen_times[key], task))
            else:
                seen_times[key] = task
        return conflicts

    def generate_daily_schedule(self, owner: Owner):
        """Return sorted tasks for the owner."""
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