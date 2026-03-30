import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(id, name, time="08:00", duration=30, priority=3,
              category="General", frequency="Once", due_date=None):
    return Task(
        id=id,
        name=name,
        duration=duration,
        priority=priority,
        category=category,
        frequency=frequency,
        time=time,
        due_date=due_date or date.today(),
    )


def make_scheduler(*tasks):
    owner = Owner(name="Alex", available_time=120)
    return Scheduler(tasks=list(tasks), owner=owner)


# ---------------------------------------------------------------------------
# Existing tests (preserved)
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(id="t1", name="Walk", duration=30, priority=3, category="Exercise", frequency="Daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", type="Dog", age=3)
    task = Task(id="t2", name="Feed", duration=10, priority=5, category="Feeding", frequency="Daily")
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_happy_path():
    """Tasks added out of order are returned chronologically."""
    t1 = make_task("a", "Morning walk", time="07:00")
    t2 = make_task("b", "Lunch feed",   time="12:30")
    t3 = make_task("c", "Evening pill", time="18:00")
    scheduler = make_scheduler(t3, t1, t2)  # intentionally shuffled

    sorted_tasks = scheduler.sort_by_time()

    assert [t.time for t in sorted_tasks] == ["07:00", "12:30", "18:00"]


def test_sort_by_time_single_task():
    """A scheduler with one task returns a list containing just that task."""
    t = make_task("a", "Solo", time="09:00")
    scheduler = make_scheduler(t)

    assert scheduler.sort_by_time() == [t]


def test_sort_by_time_empty():
    """A scheduler with no tasks returns an empty list without errors."""
    scheduler = make_scheduler()

    assert scheduler.sort_by_time() == []


def test_sort_by_time_preserves_all_tasks():
    """sort_by_time must not drop or duplicate any tasks."""
    tasks = [make_task(str(i), f"Task{i}", time=f"{10+i:02d}:00") for i in range(5)]
    scheduler = make_scheduler(*reversed(tasks))

    result = scheduler.sort_by_time()

    assert len(result) == 5


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_mark_complete_daily_returns_next_day_task():
    """Completing a Daily task creates a new task due tomorrow."""
    today = date(2026, 3, 29)
    task = make_task("w1", "Walk", frequency="Daily", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_mark_complete_weekly_returns_next_week_task():
    """Completing a Weekly task creates a new task due 7 days later."""
    today = date(2026, 3, 29)
    task = make_task("b1", "Bath", frequency="Weekly", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_mark_complete_once_returns_none():
    """Completing a one-time task must return None (no recurrence)."""
    task = make_task("v1", "Vet visit", frequency="Once")

    result = task.mark_complete()

    assert result is None


def test_mark_complete_daily_preserves_fields():
    """The recurring task clone inherits all fields except id and due_date."""
    today = date(2026, 3, 29)
    task = make_task("p1", "Pill", time="08:00", duration=5,
                     priority=5, category="Health", frequency="Daily", due_date=today)

    next_task = task.mark_complete()

    assert next_task.name == task.name
    assert next_task.time == task.time
    assert next_task.duration == task.duration
    assert next_task.priority == task.priority
    assert next_task.category == task.category
    assert next_task.frequency == task.frequency


def test_mark_complete_sets_original_as_done():
    """The original task is marked completed regardless of frequency."""
    task = make_task("x1", "Walk", frequency="Daily")
    task.mark_complete()

    assert task.completed is True


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_duplicate_times():
    """Two tasks at the same time produce exactly one warning."""
    t1 = make_task("a", "Walk",  time="09:00")
    t2 = make_task("b", "Feed",  time="09:00")
    scheduler = make_scheduler(t1, t2)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_detect_conflicts_no_conflict():
    """Tasks at different times produce no warnings."""
    t1 = make_task("a", "Walk",  time="08:00")
    t2 = make_task("b", "Feed",  time="12:00")
    scheduler = make_scheduler(t1, t2)

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_three_at_same_time():
    """Three tasks at the same time raise at least one warning."""
    tasks = [make_task(str(i), f"Task{i}", time="10:00") for i in range(3)]
    scheduler = make_scheduler(*tasks)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) >= 1


def test_detect_conflicts_warning_contains_task_names():
    """Warning messages must reference the names of the conflicting tasks."""
    t1 = make_task("a", "Morning Walk", time="07:30")
    t2 = make_task("b", "Morning Feed", time="07:30")
    scheduler = make_scheduler(t1, t2)

    warnings = scheduler.detect_conflicts()

    assert "Morning Walk" in warnings[0] or "Morning Feed" in warnings[0]


# ---------------------------------------------------------------------------
# Pet edge cases
# ---------------------------------------------------------------------------

def test_pet_starts_with_no_tasks():
    """A newly created pet has an empty task list."""
    pet = Pet(name="Luna", type="Cat", age=2)

    assert pet.tasks == []


def test_pet_with_no_tasks_add_one():
    """Adding the first task to a pet with no prior tasks works correctly."""
    pet = Pet(name="Luna", type="Cat", age=2)
    task = make_task("f1", "Feed")
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


# ---------------------------------------------------------------------------
# Plan generation
# ---------------------------------------------------------------------------

def test_generate_plan_respects_available_time():
    """Tasks whose total duration exceeds available time are partially excluded."""
    t1 = make_task("a", "Walk",  duration=60, priority=5)
    t2 = make_task("b", "Bath",  duration=60, priority=4)
    t3 = make_task("c", "Play",  duration=60, priority=3)
    scheduler = make_scheduler(t1, t2, t3)

    plan = scheduler.generate_plan(available_time=120)

    assert plan.total_time <= 120


def test_generate_plan_selects_highest_priority_first():
    """When time is tight, the highest-priority task must be included."""
    low  = make_task("a", "Play",  duration=90, priority=1)
    high = make_task("b", "Meds",  duration=90, priority=10)
    scheduler = make_scheduler(low, high)

    plan = scheduler.generate_plan(available_time=90)

    assert high in plan.list_of_tasks
    assert low not in plan.list_of_tasks


def test_generate_plan_empty_tasks():
    """generate_plan with no tasks returns an empty schedule."""
    scheduler = make_scheduler()

    plan = scheduler.generate_plan(available_time=60)

    assert plan.list_of_tasks == []
    assert plan.total_time == 0
    assert plan.unused_time == 60


def test_generate_plan_task_too_long_excluded():
    """A single task longer than available time is excluded."""
    big = make_task("a", "Big task", duration=200, priority=10)
    scheduler = make_scheduler(big)

    plan = scheduler.generate_plan(available_time=60)

    assert big not in plan.list_of_tasks
    assert plan.total_time == 0
