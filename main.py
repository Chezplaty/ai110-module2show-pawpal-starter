from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler

# --- Create Pets ---
buddy = Pet(name="Buddy", type="Dog", age=3, special_notes="Needs extra walks")
whiskers = Pet(name="Whiskers", type="Cat", age=5, special_notes="Indoor only")

# --- Create Owner ---
alex = Owner(name="Alex", available_time=120, pets=[buddy, whiskers])

# --- Create Tasks (added out of order intentionally) ---
grooming = Task(
    id="t4",
    name="Brush Buddy",
    duration=15,
    priority=1,
    category="Grooming",
    frequency="Weekly",
    time="14:00",
)

playtime = Task(
    id="t3",
    name="Playtime with Whiskers",
    duration=20,
    priority=2,
    category="Enrichment",
    frequency="Daily",
    time="11:30",
)

feeding = Task(
    id="t2",
    name="Feed Buddy & Whiskers",
    duration=10,
    priority=5,
    category="Feeding",
    frequency="Daily",
    time="07:00",
)

morning_walk = Task(
    id="t1",
    name="Morning Walk with Buddy",
    duration=30,
    priority=3,
    category="Exercise",
    frequency="Daily",
    time="08:30",
)

# Intentional conflict: same time as feeding (07:00)
vet_meds = Task(
    id="t5",
    name="Give Whiskers Her Medicine",
    duration=5,
    priority=4,
    category="Health",
    frequency="Daily",
    time="07:00",
)

# --- Scheduler: detect conflicts before sorting ---
scheduler = Scheduler(tasks=[grooming, playtime, feeding, morning_walk, vet_meds], owner=alex)

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("--- Conflict Report ---")
    for warning in conflicts:
        print(warning)
    print()

sorted_tasks = scheduler.sort_by_time()

# --- Build Schedule from sorted tasks ---
schedule = Schedule(date=date.today(), available_time=alex.available_time)

for task in sorted_tasks:
    schedule.list_of_tasks.append(task)

schedule.total_time = sum(t.duration for t in schedule.list_of_tasks)
schedule.unused_time = schedule.available_time - schedule.total_time

# --- Print Today's Schedule ---
print(f"Today's Schedule — {schedule.date}")
print(f"Owner: {alex.name}  |  Available time: {alex.available_time} min")
print(f"Pets: {buddy.name} ({buddy.type}), {whiskers.name} ({whiskers.type})")
print("-" * 40)

for task in schedule.list_of_tasks:
    print(
        f"  {task.time}  [{task.category}] {task.name}"
        f"\n           Duration: {task.duration} min | Priority: {task.priority} | {task.frequency}"
    )

print("-" * 40)
print(f"Total scheduled: {schedule.total_time} min")
print(f"Unused time:     {schedule.unused_time} min")
