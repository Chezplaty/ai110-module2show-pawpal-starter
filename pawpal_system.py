from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Pet:
    name: str
    type: str
    age: int
    special_notes: str = ""
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_profile(self) -> dict:
        """Return a dictionary of the pet's basic profile information."""
        pass


@dataclass
class Owner:
    name: str
    available_time: int
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, key: str, value) -> None:
        """Set or update a single preference entry by key."""
        pass

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        pass


@dataclass
class Task:
    id: str
    name: str
    duration: int
    priority: int
    category: str
    frequency: str
    time: str = "00:00"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task done and return a cloned Task with the next due date if Daily or Weekly, else None."""
        self.completed = True
        if self.frequency == "Daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency == "Weekly":
            next_due = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            id=f"{self.id}_next",
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            time=self.time,
            due_date=next_due,
        )

    def update_task(self, **kwargs) -> None:
        """Update one or more task fields using keyword arguments."""
        pass

    def get_summary(self) -> dict:
        """Return a dictionary summary of this task's fields."""
        pass


@dataclass
class Schedule:
    date: date
    available_time: int
    list_of_tasks: List[Task] = field(default_factory=list)
    total_time: int = 0
    unused_time: int = 0

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule and update time totals."""
        pass

    def calculate_total_time(self) -> int:
        """Sum the durations of all scheduled tasks and return the total."""
        pass

    def display_plan(self) -> str:
        """Return a formatted string showing all tasks and time remaining."""
        pass


@dataclass
class Scheduler:
    tasks: List[Task]
    owner: Owner

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by their HH:MM time attribute in ascending order."""
        return sorted(self.tasks, key=lambda task: task.time)

    def detect_conflicts(self) -> List[str]:
        """Check all tasks for time collisions and return a warning string for each conflict found."""
        seen = {}
        warnings = []
        for task in self.tasks:
            if task.time in seen:
                other = seen[task.time]
                warnings.append(
                    f"WARNING: '{task.name}' and '{other.name}' are both scheduled at {task.time}."
                )
            else:
                seen[task.time] = task
        return warnings

    def generate_plan(self, available_time: int) -> Schedule:
        """Greedily select tasks by descending priority, skipping any that exceed remaining time."""
        schedule = Schedule(date=date.today(), available_time=available_time)
        remaining = available_time
        for task in sorted(self.tasks, key=lambda t: t.priority, reverse=True):
            if task.duration <= remaining:
                schedule.list_of_tasks.append(task)
                schedule.total_time += task.duration
                remaining -= task.duration
        schedule.unused_time = available_time - schedule.total_time
        return schedule

    def explain_plan(self, schedule: Schedule, skipped: List[Task]) -> str:
        """Return a human-readable explanation of the plan and any skipped tasks."""
        pass
