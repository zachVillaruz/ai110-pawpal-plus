from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class Task:
    """Represents a pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    description: str = ""
    pet: Optional['Pet'] = None

    def get_title(self) -> str:
        """Return the task title."""
        pass

    def get_duration(self) -> int:
        """Return the duration in minutes."""
        pass

    def get_priority(self) -> str:
        """Return the priority level."""
        pass


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
        pass

    def get_species(self) -> str:
        """Return the pet's species."""
        pass

    def get_special_needs(self) -> List[str]:
        """Return the list of special needs."""
        pass

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        pass


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
        pass

    def get_preferences(self) -> Dict[str, any]:
        """Return the owner's preferences."""
        pass

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        pass


class Scheduler:
    """Handles scheduling of pet care tasks."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner: Owner = owner
        self.pets: List[Pet] = owner.pets
        self.tasks: List[Task] = []

    def generate_schedule(self) -> Dict:
        """Generate a schedule for all tasks."""
        pass

    def optimize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Optimize and order tasks based on constraints."""
        pass

    def check_constraints(self) -> bool:
        """Check if constraints are satisfied."""
        pass

    def explain_plan(self) -> str:
        """Explain the generated plan."""
        pass
