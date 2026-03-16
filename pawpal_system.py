from dataclasses import dataclass, field
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
        pass