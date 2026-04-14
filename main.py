from pawpal_system import Owner, Pet, Task, Scheduler, suggest_tasks_for_pet, is_valid_task

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

# ---------------------------
# ✅ ADD: Initialize scheduler early (for AI + logging)
# ---------------------------
scheduler = Scheduler()

# ---------------------------
# 🤖 AI Task Suggestions (Week 8 Upgrade)
# ---------------------------
print("\n🤖 AI Task Suggestions for Mochi:")

suggestions = suggest_tasks_for_pet(pet1)

# initialize log if not present
if not hasattr(scheduler, "log"):
    scheduler.log = {
        "suggested": [],
        "accepted": [],
        "rejected": []
    }

for s in suggestions:

    if s not in scheduler.log["suggested"]:
        scheduler.log["suggested"].append(s)

    if not is_valid_task(s):
        print(f"⚠️ Skipped unsafe suggestion: {s}")
        continue

    print(f"- {s}")
    user_input = input("Accept this task? (y/n): ").strip().lower()

    if user_input == "y":

        # =====================================================
        # 🧠 FIX: AI uses dynamic free time instead of fixed time
        # =====================================================
        new_task = Task(
            title=s,
            task_type="AI",
            time=scheduler.get_free_time(owner),  # FIXED
            priority=2
        )

        pet1.add_task(new_task)

        scheduler.log["accepted"].append(s)
        print(f"✅ Added: {s}")

    else:
        scheduler.log["rejected"].append(s)
        print(f"❌ Rejected: {s}")

# 3. Create scheduler and generate schedule
schedule = scheduler.generate_daily_schedule(owner)

# 4. Print schedule
# 3. Create scheduler and generate schedule
schedule = scheduler.generate_daily_schedule(owner)

# =====================================================
# 🧪 TEST ONLY: auto mark all tasks complete
# =====================================================
for task in schedule:
    task.completed = True

# 4. Print schedule
print("\nToday's Schedule:")
for task in schedule:
    status = "✅" if task.completed else "❌"
    print(f"{task.time} - {task.title} (Pet: {task.pet.name}, Priority: {task.priority}) [{status}]")

# =====================================================
# 🧪 TEST ONLY: auto mark all tasks complete
# =====================================================
"""for task in schedule:
    task.completed = True"""

# 5. Test marking a recurring task complete
print("\nCompleting recurring task...")
t4.mark_complete()

# 6. Show updated tasks
print("\nUpdated tasks for Mochi:")
for task in pet1.tasks:
    print(f"{task.time} - {task.title} (Recurring: {task.recurring})")

# ---------------------------
# 📊 AI Reliability Summary
# ---------------------------
print("\n📊 AI Reliability Summary:")
print(f"Suggested: {len(scheduler.log['suggested'])}")
print(f"Accepted: {len(scheduler.log['accepted'])}")
print(f"Rejected: {len(scheduler.log['rejected'])}")