# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The scheduler was extended with three features beyond basic task listing:

- **Priority-based plan generation** — `generate_plan()` sorts tasks by priority (1–5) in descending order and greedily fills the owner's available time, skipping any task whose duration no longer fits. Higher-priority tasks are always scheduled first.

- **Time conflict detection** — `detect_conflicts()` scans all tasks for collisions using a dictionary keyed by `HH:MM` time. If two tasks are scheduled at the same time, a warning message is returned instead of crashing. Conflicts are surfaced in both the terminal and the Streamlit UI before the schedule is displayed.

- **Automatic recurrence** — `mark_complete()` returns a new `Task` instance with an updated `due_date` when a recurring task is finished. Daily tasks roll forward by 1 day (`timedelta(days=1)`), weekly tasks by 7 days (`timedelta(weeks=1)`). One-time tasks return `None`.

## Testing PawPal+

### How to run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

Run from the `ai110-module2show-pawpal-starter/` directory. The `-v` flag shows each test name and its pass/fail result.

### What the tests cover

The suite contains **21 tests** across five areas:

| Area | What is verified |
|------|-----------------|
| **Sorting** | `sort_by_time()` returns tasks in `HH:MM` ascending order, handles single-task and empty lists, and never drops or duplicates tasks. |
| **Recurrence** | `mark_complete()` on a `Daily` task returns a new task due tomorrow; `Weekly` adds 7 days; `Once` returns `None`. The clone preserves all original fields and the original task is marked done. |
| **Conflict detection** | `detect_conflicts()` flags two tasks at the same time with one warning, produces no warnings when times differ, handles three-way conflicts, and includes task names in the warning text. |
| **Plan generation** | `generate_plan()` never exceeds available time, always picks the highest-priority task first when time is tight, returns an empty schedule when there are no tasks, and excludes any single task that is too long to fit. |
| **Pet edge cases** | A new `Pet` starts with an empty task list; adding the first task works correctly. |

### Confidence Level

**4 / 5 stars**

The three core scheduling behaviors — sorting, recurrence, and conflict detection — are fully implemented and all 21 tests pass. The rating is not 5 stars because several methods (`get_profile`, `update_preferences`, `add_task` on `Schedule`, `display_plan`, `explain_plan`) are still stubs (`pass`) and have no test coverage yet. Reliability of the full app depends on those being implemented and tested.
