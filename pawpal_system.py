from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Pet:
    name: str
    type: str
    age: int
    special_notes: str = ""

    def get_profile(self) -> dict:
        pass


@dataclass
class Owner:
    name: str
    available_time: int
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, key: str, value) -> None:
        pass

    def get_available_time(self) -> int:
        pass


@dataclass
class Task:
    id: str
    name: str
    duration: int
    priority: int
    category: str
    frequency: str

    def update_task(self, **kwargs) -> None:
        pass

    def get_summary(self) -> dict:
        pass


@dataclass
class Schedule:
    date: date
    available_time: int
    list_of_tasks: List[Task] = field(default_factory=list)
    total_time: int = 0
    unused_time: int = 0

    def add_task(self, task: Task) -> None:
        pass

    def calculate_total_time(self) -> int:
        pass

    def display_plan(self) -> str:
        pass


@dataclass
class Scheduler:
    tasks: List[Task]
    owner: Owner

    def generate_plan(self, available_time: int) -> Schedule:
        pass

    def explain_plan(self, schedule: Schedule, skipped: List[Task]) -> str:
        pass
