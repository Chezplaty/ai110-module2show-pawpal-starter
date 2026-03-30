import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Owner & Pet setup ---
st.subheader("Owner & Pet")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=120)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, type=species, age=0)
    st.session_state.owner = Owner(
        name=owner_name,
        available_time=available_time,
        pets=[pet],
    )
    st.success(f"Saved {owner_name} with pet {pet_name}!")

if st.session_state.owner:
    owner = st.session_state.owner
    st.caption(f"Current owner: **{owner.name}** | Pets: {', '.join(p.name for p in owner.pets)}")

st.divider()

# --- Add Task ---
st.subheader("Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=2)

col1, col2 = st.columns(2)
with col1:
    category = st.text_input("Category", value="Exercise")
with col2:
    task_time = st.time_input("Scheduled time", value=None)

frequency = st.selectbox("Frequency", ["Daily", "Weekly", "As needed"])

if st.button("Add Task"):
    task = Task(
        id=f"t{len(st.session_state.tasks) + 1}",
        name=task_title,
        duration=int(duration),
        priority=priority,
        category=category,
        frequency=frequency,
        time=task_time.strftime("%H:%M") if task_time else "00:00",
    )
    # Add task to the owner's first pet if one exists
    if st.session_state.owner and st.session_state.owner.pets:
        st.session_state.owner.pets[0].add_task(task)
    st.session_state.tasks.append(task)
    st.success(f"Added task: {task.name}")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([{
        "id": t.id, "name": t.name, "time": t.time, "duration": t.duration,
        "priority": t.priority, "category": t.category, "frequency": t.frequency
    } for t in st.session_state.tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if not st.session_state.owner:
        st.warning("Please save an Owner first.")
    elif not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        owner = st.session_state.owner
        scheduler = Scheduler(tasks=st.session_state.tasks, owner=owner)

        conflicts = scheduler.detect_conflicts()
        for warning in conflicts:
            st.warning(warning)

        schedule = scheduler.generate_plan(available_time=owner.available_time)

        if schedule and schedule.list_of_tasks:
            st.success("Schedule generated!")
            for task in schedule.list_of_tasks:
                st.markdown(f"- **[{task.category}]** {task.name} — {task.duration} min (priority {task.priority}, {task.frequency})")
            st.markdown(f"**Total scheduled:** {schedule.total_time} min | **Unused:** {schedule.unused_time} min")
        else:
            st.warning("Scheduler returned an empty plan. Implement generate_plan() in pawpal_system.py to populate it.")
