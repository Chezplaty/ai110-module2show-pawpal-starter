import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


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
