import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

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

# ---------------------------
# Page settings
# ---------------------------
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------
# Scenario / Info
# ---------------------------
with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )
# ---------------------------
# Owner & Pet Setup
# ---------------------------
st.subheader("Owner & Pet Setup")
owner_name_input = st.text_input("Owner name", value=st.session_state.owner.name)
pet_name_input = st.text_input("Pet name", value=st.session_state.pet.name)
species_input = st.selectbox("Species", ["dog", "cat", "other"], index=0)

if st.button("Create Owner & Pet"):
    st.session_state.owner = Owner(owner_name_input, f"{owner_name_input.lower()}@email.com")
    st.session_state.pet = Pet(pet_name_input, species_input, 2)  # default age=2
    st.session_state.owner.add_pet(st.session_state.pet)
    st.session_state.tasks = []
    st.success(f"Created owner {owner_name_input} with pet {pet_name_input} ({species_input})")

st.divider()
# ---------------------------
# Add Tasks Section
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
    st.success(f"Task '{task_title}' added to {st.session_state.pet.name}")

st.divider()
# ---------------------------
# Display Current Tasks
# ---------------------------
if st.session_state.pet.tasks:
    st.subheader(f"Current Tasks for {st.session_state.pet.name}")
    for i, task in enumerate(st.session_state.pet.tasks):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{task.time} - {task.title} (Priority {task.priority}) {'🔁' if task.recurring else ''}")
        with col2:
            button_key = f"complete_{task.title}_{i}_{task.time}"
            if task.completed:
                st.write("✅ Completed")  # show completed instead of button
            else:
                if st.button("✅ Complete", key=button_key):
                    task.mark_complete()
                    st.success(f"Task '{task.title}' marked complete!")
# ---------------------------
# Generate / Display Schedule
# ---------------------------
st.divider()
st.subheader("Daily Schedule")

# Create scheduler and store schedule in session state
if "schedule" not in st.session_state or st.session_state.get("trigger_refresh", False):
    scheduler = Scheduler()
    st.session_state.schedule = scheduler.generate_daily_schedule(st.session_state.owner)

schedule = st.session_state.schedule  # now guaranteed

# Display tasks and allow completing them
if schedule:
    for i, task in enumerate(schedule):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{task.time} - {task.title} (Pet: {task.pet.name}, Priority {task.priority}) {'🔁' if task.recurring else ''}")
        with col2:
            if not task.completed:
                button_key = f"{task.title}_{task.time}_{i}"  # unique key
                if st.button("✅ Complete", key=button_key):
                    task.mark_complete()
                    # regenerate schedule after marking complete
                    st.session_state.schedule = Scheduler().generate_daily_schedule(st.session_state.owner)
                    # trigger rerun by toggling the refresh state
                    st.session_state.trigger_refresh = not st.session_state.trigger_refresh
                    st.stop()
else:
    st.info("No scheduled tasks yet.")