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

    # =========================
    # NEW ADDITION (Week 8)
    # =========================
    conflict: bool = False

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

                # =========================
                # OLD VERSION (kept for reference)
                # =========================
                # self.pet.add_task(new_task)

                # =========================
                # NEW FIX: prevent duplicate recurring tasks
                # =========================
                for t in self.pet.tasks:
                    if t.title == new_task.title and t.time == new_task.time:
                        return

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

        # =========================
        # OLD VERSION (kept)
        # =========================
        # self.tasks.append(task)

        # =========================
        # NEW FIX: prevent duplicates
        # =========================
        for t in self.tasks:
            if t.title == task.title and t.time == task.time:
                return

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

        # =========================
        # OLD VERSION (kept)
        # =========================
        # return self.sort_tasks(tasks)

        # =========================
        # NEW FIX: conflict resolution
        # =========================
        resolved = {}
        for t in tasks:
            key = t.time
            if key not in resolved or t.priority > resolved[key].priority:
                resolved[key] = t

        tasks = list(resolved.values())

        return self.sort_tasks(tasks)

    # =========================================================
    # 🧠 NEW ADDITION: WEEK 8 AI-AWARE SCHEDULER EXTENSIONS
    # (NO REMOVALS — JUST ADDING CAPABILITY)
    # =========================================================

    def get_used_times(self, owner: Owner):
        """Return all time slots already used by tasks."""
        return set(t.time for t in owner.get_all_tasks())

    def get_free_time(self, owner: Owner):
        """Find first available time slot in the day."""
        all_slots = [
            "08:00", "09:00", "10:00",
            "11:00", "12:00", "13:00",
            "14:00", "15:00", "16:00",
            "17:00", "18:00"
        ]

        used = self.get_used_times(owner)

        for slot in all_slots:
            if slot not in used:
                return slot

        return "12:00"  # fallback


# =========================
# AI SUGGESTION LAYER
# =========================

def suggest_tasks_for_pet(pet: Pet):
    suggestions = [
        f"Feed {pet.name}",
        f"Give water to {pet.name}",
        f"Play with {pet.name}"
    ]
    return suggestions


def is_valid_task(task_text: str):
    banned_keywords = ["kill", "ignore", "chocolate", "harm"]
    return not any(word in task_text.lower() for word in banned_keywords)


"""
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
"""