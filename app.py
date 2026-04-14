import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, suggest_tasks_for_pet, is_valid_task

# ---------------------------
# Initialize owner and pet
# ---------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Demo User", "demo@email.com")

if "pet" not in st.session_state:
    st.session_state.pet = Pet("Mochi", "dog", 2)
    st.session_state.owner.add_pet(st.session_state.pet)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# persistent scheduler
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# FIX: safe log init
if not hasattr(st.session_state.scheduler, "log"):
    st.session_state.scheduler.log = {
        "suggested": [],
        "accepted": [],
        "rejected": []
    }

# ---------------------------
# Page settings
# ---------------------------
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown("""
**PawPal+** is a pet care planning assistant.
It helps a pet owner plan tasks for their pet(s).
""")

# ---------------------------
# Owner & Pet Setup
# ---------------------------
st.subheader("Owner & Pet Setup")

owner_name_input = st.text_input("Owner name", value=st.session_state.owner.name)
pet_name_input = st.text_input("Pet name", value=st.session_state.pet.name)
species_input = st.selectbox("Species", ["dog", "cat", "other"], index=0)

if st.button("Create Owner & Pet"):
    st.session_state.owner = Owner(owner_name_input, f"{owner_name_input.lower()}@email.com")
    st.session_state.pet = Pet(pet_name_input, species_input, 2)
    st.session_state.owner.add_pet(st.session_state.pet)
    st.session_state.tasks = []
    st.success("Updated owner & pet")

st.divider()

# ---------------------------
# Add Tasks
# ---------------------------
st.subheader("Add Task")

col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

with col1:
    task_title = st.text_input("Task title", value="Morning Walk")

with col2:
    task_time = st.text_input("Time (HH:MM)", value="09:00")

with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

with col4:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

recurring = st.checkbox("Recurring task (daily)", value=False)

if st.button("Add Task to Pet"):
    priority_map = {"low": 1, "medium": 2, "high": 3}

    new_task = Task(
        title=task_title,
        task_type="general",
        time=task_time,
        priority=priority_map[priority_str],
        recurring=recurring,
        frequency="daily" if recurring else None
    )

    st.session_state.pet.add_task(new_task)
    st.success(f"Task '{task_title}' added")

st.divider()

# ---------------------------
# AI Suggestions
# ---------------------------
st.subheader("🤖 AI Task Suggestions")

if st.button("Generate AI Suggestions"):
    st.session_state.ai_suggestions = suggest_tasks_for_pet(st.session_state.pet)

if "ai_suggestions" in st.session_state:

    for i, s in enumerate(st.session_state.ai_suggestions):

        if s not in st.session_state.scheduler.log["suggested"]:
            st.session_state.scheduler.log["suggested"].append(s)

        if not is_valid_task(s):
            st.warning(f"Filtered unsafe suggestion: {s}")
            continue

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(s)

        with col2:
            if st.button("➕ Accept", key=f"accept_{i}"):

                # FIX: prevent duplicate AI tasks
                if not any(t.title == s for t in st.session_state.pet.tasks):

                    new_task = Task(
                        title=s,
                        task_type="AI",
                        time=st.session_state.scheduler.get_free_time(st.session_state.owner),
                        priority=2
                    )

                    st.session_state.pet.add_task(new_task)
                    st.session_state.scheduler.log["accepted"].append(s)

                    st.success(f"Added: {s}")
                    st.rerun()

            if st.button("❌ Reject", key=f"reject_{i}"):
                st.session_state.scheduler.log["rejected"].append(s)
                st.info(f"Rejected: {s}")

# ---------------------------
# Current Tasks
# ---------------------------
st.subheader("Current Tasks")

for i, task in enumerate(st.session_state.pet.tasks):
    col1, col2 = st.columns([4, 1])

    with col1:
        status = "✅" if task.completed else "❌"
        st.write(f"{task.time} - {task.title} {status}")

    with col2:
        if not task.completed:
            if st.button("Complete", key=f"c_{i}"):
                task.mark_complete()
                st.rerun()

# ---------------------------
# Schedule
# ---------------------------
st.subheader("Daily Schedule")

scheduler = st.session_state.scheduler
st.session_state.schedule = scheduler.generate_daily_schedule(st.session_state.owner)

for task in st.session_state.schedule:
    st.write(f"{task.time} - {task.title} ({task.pet.name})")

# ---------------------------
# Log
# ---------------------------
st.subheader("📊 AI Log")

log = st.session_state.scheduler.log
st.write(f"Suggested: {len(log['suggested'])}")
st.write(f"Accepted: {len(log['accepted'])}")
st.write(f"Rejected: {len(log['rejected'])}")