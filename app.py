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
    if st.session_state.owner and st.session_state.owner.pets:
        st.session_state.owner.pets[0].add_task(task)
    st.session_state.tasks.append(task)
    st.success(f"Added: **{task.name}** at {task.time} ({task.duration} min)")

# --- Current tasks: sorted by time via Scheduler ---
if st.session_state.tasks:
    # Use a temporary Scheduler just to get the sorted order
    _scheduler = Scheduler(
        tasks=st.session_state.tasks,
        owner=st.session_state.owner or Owner(name="", available_time=0),
    )
    sorted_tasks = _scheduler.sort_by_time()

    PRIORITY_LABEL = {1: "⬇ Low", 2: "↙ Low-Med", 3: "➡ Medium", 4: "↗ High-Med", 5: "⬆ High"}

    st.write("Current tasks (sorted by scheduled time):")
    st.table([{
        "Time": t.time,
        "Task": t.name,
        "Category": t.category,
        "Duration (min)": t.duration,
        "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
        "Frequency": t.frequency,
    } for t in sorted_tasks])
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

        # --- Conflict warnings ---
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error(
                f"⚠️ **{len(conflicts)} scheduling conflict{'s' if len(conflicts) > 1 else ''} found** — "
                "two or more tasks are booked at the same time. "
                "Review the conflicts below and edit a task's scheduled time before continuing."
            )
            for warning in conflicts:
                # warning format: "WARNING: 'A' and 'B' are both scheduled at HH:MM."
                st.warning(f"🕐 {warning}  \n*Tip: go back and change the scheduled time for one of these tasks.*")
            st.stop()
        else:
            st.success("No scheduling conflicts found.")

        # --- Generate and display plan ---
        schedule = scheduler.generate_plan(available_time=owner.available_time)

        if schedule and schedule.list_of_tasks:
            st.success(f"Schedule generated for **{owner.name}**!")

            # Sort scheduled tasks by time for display
            scheduled_sorted = sorted(schedule.list_of_tasks, key=lambda t: t.time)
            PRIORITY_LABEL = {1: "⬇ Low", 2: "↙ Low-Med", 3: "➡ Medium", 4: "↗ High-Med", 5: "⬆ High"}

            st.table([{
                "Time": t.time,
                "Task": t.name,
                "Category": t.category,
                "Duration (min)": t.duration,
                "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
                "Frequency": t.frequency,
            } for t in scheduled_sorted])

            # Time summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Available time", f"{owner.available_time} min")
            col2.metric("Scheduled", f"{schedule.total_time} min")
            col3.metric("Unused", f"{schedule.unused_time} min")

            # Show skipped tasks if any didn't fit
            scheduled_ids = {t.id for t in schedule.list_of_tasks}
            skipped = [t for t in st.session_state.tasks if t.id not in scheduled_ids]
            if skipped:
                with st.expander(f"⏭ {len(skipped)} task(s) skipped (didn't fit in available time)"):
                    for t in skipped:
                        st.markdown(f"- **{t.name}** — {t.duration} min (priority {t.priority})")
        else:
            st.warning("No tasks fit in the available time. Try increasing available time or reducing task durations.")
