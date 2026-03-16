from pawpal_system import Owner, Pet, Task, Scheduler


# Create owner
owner = Owner("Taylor", "taylor@email.com")

# Create pets
dog = Pet("Buddy", "Dog", 5)
cat = Pet("Luna", "Cat", 3)

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create tasks
task1 = Task("Morning Walk", "walk", "07:00", priority=2)
task2 = Task("Breakfast", "feeding", "08:00")
task3 = Task("Medication", "medication", "08:00", priority=3)

# Assign tasks
dog.add_task(task1)
dog.add_task(task2)
cat.add_task(task3)

# Scheduler
scheduler = Scheduler()
schedule = scheduler.generate_daily_schedule(owner)

print("\nToday's Schedule")
print("-------------------")

for task in schedule:
    print(f"{task.time} - {task.title} ({task.task_type})")