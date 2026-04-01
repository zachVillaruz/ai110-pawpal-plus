from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime, time


@dataclass
class Task:
    """Represents a pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    description: str = ""
    pet: Optional['Pet'] = None
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    scheduled_time: Optional[time] = None

    def get_title(self) -> str:
        """Return the task title."""
        return self.title

    def get_duration(self) -> int:
        """Return the duration in minutes."""
        return self.duration_minutes

    def get_priority(self) -> str:
        """Return the priority level."""
        return self.priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def set_scheduled_time(self, scheduled_time: time) -> None:
        """Set the scheduled time for this task."""
        self.scheduled_time = scheduled_time

    def get_priority_value(self) -> int:
        """Return numeric priority for sorting (higher = more urgent)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority.lower(), 0)


@dataclass
class Pet:
    """Represents a pet."""
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    owner: Optional['Owner'] = None
    tasks: List[Task] = field(default_factory=list)

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name

    def get_species(self) -> str:
        """Return the pet's species."""
        return self.species

    def get_age(self) -> int:
        """Return the pet's age."""
        return self.age

    def get_special_needs(self) -> List[str]:
        """Return the list of special needs."""
        return self.special_needs

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        task.pet = self
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Represents a pet owner."""
    name: str
    email: str = ""
    phone: str = ""
    preferences: Dict[str, any] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def get_name(self) -> str:
        """Return the owner's name."""
        return self.name

    def get_preferences(self) -> Dict[str, any]:
        """Return the owner's preferences."""
        return self.preferences

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        pet.owner = self
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all pending (incomplete) tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks


class Scheduler:
    """Handles scheduling of pet care tasks."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner: Owner = owner
        self.pets: List[Pet] = owner.pets
        self.tasks: List[Task] = self._collect_tasks()
        self.scheduled_tasks: List[Task] = []

    def _collect_tasks(self) -> List[Task]:
        """Collect all pending tasks from all pets."""
        return self.owner.get_all_pending_tasks()

    def generate_schedule(self) -> Dict:
        """Generate a schedule for all pending tasks."""
        # Refresh task list
        self.tasks = self._collect_tasks()

        # Sort tasks by priority
        sorted_tasks = self.optimize_tasks(self.tasks)

        # Check if constraints are satisfied
        if not self.check_constraints():
            return {
                "success": False,
                "message": "Cannot satisfy scheduling constraints",
                "tasks": []
            }

        # Build schedule
        self.scheduled_tasks = sorted_tasks

        return {
            "success": True,
            "owner": self.owner.get_name(),
            "num_tasks": len(sorted_tasks),
            "total_duration_minutes": sum(t.get_duration() for t in sorted_tasks),
            "tasks": [
                {
                    "title": t.get_title(),
                    "pet": t.pet.get_name() if t.pet else "Unknown",
                    "duration": t.get_duration(),
                    "priority": t.get_priority(),
                    "description": t.description
                }
                for t in sorted_tasks
            ],
            "explanation": self.explain_plan()
        }

    def optimize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Optimize and order tasks based on priority and constraints."""
        if not tasks:
            return []

        # Sort by priority (high to low), then by duration (short to long)
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (-t.get_priority_value(), t.get_duration())
        )
        return sorted_tasks

    def check_constraints(self) -> bool:
        """Check if constraints are satisfied."""
        # Basic constraint checks
        if not self.tasks:
            return True

        # Check 1: Ensure total duration is reasonable (e.g., < 480 mins = 8 hours)
        total_duration = sum(t.get_duration() for t in self.tasks)
        max_daily_minutes = self.owner.get_preferences().get("max_daily_minutes", 480)
        if total_duration > max_daily_minutes:
            return False

        # Check 2: Ensure all tasks have valid priority
        for task in self.tasks:
            if task.get_priority().lower() not in ["low", "medium", "high"]:
                return False

        # Check 3: Ensure all tasks have positive duration
        for task in self.tasks:
            if task.get_duration() <= 0:
                return False

        return True

    def explain_plan(self) -> str:
        """Explain the generated plan."""
        if not self.scheduled_tasks:
            return "No tasks are scheduled. All tasks may be completed or no pending tasks exist."

        explanation = f"Plan for {self.owner.get_name()}:\n"
        explanation += f"Total tasks scheduled: {len(self.scheduled_tasks)}\n"
        explanation += f"Total time required: {sum(t.get_duration() for t in self.scheduled_tasks)} minutes\n\n"

        explanation += "Task order (by priority):\n"
        for i, task in enumerate(self.scheduled_tasks, 1):
            pet_name = task.pet.get_name() if task.pet else "Unknown"
            explanation += f"{i}. [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min) - {pet_name}\n"
            if task.description:
                explanation += f"   Description: {task.description}\n"

        return explanation
