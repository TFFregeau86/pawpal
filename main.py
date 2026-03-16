# main.py
from pawpal_system import Owner, Pet, Task, Scheduler

# 1. Create owner and pets
owner = Owner("Alice", "alice@email.com")
pet1 = Pet("Mochi", "dog", 3)
pet2 = Pet("Luna", "cat", 2)
owner.add_pet(pet1)
owner.add_pet(pet2)

# 2. Add tasks (some overlapping)
t1 = Task("Morning Walk", "walk", "08:00", priority=3)
t2 = Task("Feed Mochi", "feeding", "08:00", priority=2)  # conflict with t1
t3 = Task("Vet Appointment", "vet", "10:00", priority=1)
t4 = Task("Evening Walk", "walk", "18:00", priority=2, recurring=True, frequency="daily")

pet1.add_task(t1)
pet1.add_task(t2)
pet2.add_task(t3)
pet1.add_task(t4)

# 3. Create scheduler and generate schedule
scheduler = Scheduler()
schedule = scheduler.generate_daily_schedule(owner)

# 4. Print schedule
print("\nToday's Schedule:")
for task in schedule:
    status = "✅" if task.completed else "❌"
    print(f"{task.time} - {task.title} (Pet: {task.pet.name}, Priority: {task.priority}) [{status}]")

# 5. Test marking a recurring task complete
print("\nCompleting recurring task...")
t4.mark_complete()

# 6. Show updated tasks
print("\nUpdated tasks for Mochi:")
for task in pet1.tasks:
    print(f"{task.time} - {task.title} (Recurring: {task.recurring})")