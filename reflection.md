# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

1. Add a pet to their account so they can manage routines for each pet.

2. Schedule care tasks such as feeding, walks, medications, or vet appointments.

3. View a daily schedule of tasks to ensure pets receive proper care on time.

### Main System Objects

Owner
Attributes:
- name
- email
- pets (list)

Methods:
- add_pet()
- view_pets()

Pet
Attributes:
- name
- species
- age
- tasks (list)

Methods:
- add_task()
- remove_task()
- list_tasks()

Task
Attributes:
- title
- task_type
- time
- priority
- recurring

Methods:
- mark_complete()
- reschedule()

Scheduler
Methods:
- sort_tasks()
- detect_conflicts()
- generate_daily_schedule()

**b. Design changes**

During the design review, I adjusted how the Scheduler class interacts with the system. 
Instead of storing tasks directly inside the Scheduler, the Scheduler operates on lists of tasks provided by Pets. 
This keeps the scheduler independent from the data storage and makes the design more modular.

I also confirmed the relationship structure where an Owner can have multiple Pets, and each Pet can contain multiple Tasks. 
This hierarchy made the system easier to reason about and reflects real-world pet ownership.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
