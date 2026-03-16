# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

1. Add a pet to their account so they can manage routines for each pet.

2. Schedule care tasks such as feeding, walks, medications, or vet appointments.

3. View a daily schedule of tasks to ensure pets receive proper care on time.

classDiagram
    class Task {
        +str title
        +str task_type
        +str time
        +int priority
        +bool recurring
        +bool completed
        +str frequency
        +Pet pet
        +mark_complete()
        +reschedule(new_time)
    }

    class Pet {
        +str name
        +str species
        +int age
        +list tasks
        +add_task(task)
        +remove_task(task)
        +list_tasks()
    }

    class Owner {
        +str name
        +str email
        +list pets
        +add_pet(pet)
        +view_pets()
        +get_all_tasks()
    }

    class Scheduler {
        +sort_tasks(tasks)
        +detect_conflicts(tasks)
        +generate_daily_schedule(owner)
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Task "1" --> "1" Pet : linked to
    Scheduler ..> Task : uses
    Scheduler ..> Owner : uses

**b. Design changes**

During the design review, I made the following changes:

- The Scheduler was made stateless; it no longer stores tasks internally. Instead, it operates on task lists provided by pets. This improves modularity and testability.
- Added recurring task logic in Task.mark_complete() instead of in Scheduler, so tasks self-manage recurrence.
- Clarified relationships: an Owner can have multiple Pets, each Pet can have multiple Tasks, and Tasks know their parent Pet.
- Introduced conflict detection in Scheduler to alert when tasks overlap in time for the same pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- Scheduler constraints:
  - **Time:** Tasks are sorted chronologically.
  - **Priority:** Higher-priority tasks are scheduled before lower-priority tasks if at the same time.
  - **Recurrence:** Recurring tasks generate new instances for future days automatically.
  - **Conflict detection:** Identifies overlapping tasks for the same pet.

- Reasoning: Time ensures tasks are in a logical order, while priority resolves overlaps. Recurrence reduces manual entry and conflict detection prevents scheduling errors.

**b. Tradeoffs**

- Tradeoff: When two tasks have the exact same time, the scheduler chooses the task with higher priority first, even if a lower-priority task was added first.
- Reasonable because pet care emergencies or important tasks (like vet visits) should take precedence over routine tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- Used AI to:
  - Draft class definitions for Task, Pet, Owner, and Scheduler.
  - Generate test cases for task completion, sorting, recurring tasks, and conflict detection.
  - Suggest Streamlit UI improvements for displaying schedules and marking tasks complete.
- Helpful prompts included:
  - "Write pytest unit tests for a pet scheduler with recurring tasks and conflict detection."
  - "Generate a Mermaid UML diagram for these classes."

**b. Judgment and verification**

- AI suggested storing recurring logic in Scheduler, but I moved it to Task.mark_complete() to reduce coupling.
- Verified suggestions by checking whether tasks were correctly marked complete and whether new recurring tasks were added.
- Used manual tests in Streamlit and pytest to ensure behavior matched expectations.

---

## 4. Testing and Verification

**a. What you tested**

- Tested task completion to ensure tasks could be marked complete.
- Tested task sorting by time and priority.
- Verified that completing recurring tasks creates new instances for the next day.
- Checked conflict detection for overlapping tasks.
- These tests are important because they validate that the core scheduling logic works correctly and prevents missed or duplicated tasks.

**b. Confidence**

- Confidence level: ★★★★☆ (4/5)  
- Edge cases to test further:
  - Multiple pets with overlapping tasks at the same time.
  - Tasks spanning midnight or multiple days.
  - Tasks with durations longer than the interval between scheduled tasks.

---

## 5. Reflection

**a. What went well**

- Successfully implemented a modular scheduler that handles time, priority, recurrence, and conflicts.
- Streamlit UI now displays tasks clearly, allows marking completion, and reflects real-time updates.
- Automated tests gave confidence that the system behaves correctly.

**b. What you would improve**

- Make the UI fully dynamic for multiple pets and allow editing tasks.
- Add notifications for upcoming tasks.
- Enhance scheduler to handle task duration, not just start times.

**c. Key takeaway**

- Clear class design and modularity are essential when working with AI suggestions. AI can generate code quickly, but human oversight ensures maintainable and correct design.
