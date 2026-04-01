from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime, time, date, timedelta


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
    due_date: Optional[date] = None  # CHANGED: Track when the task is due

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
        """Mark the task as completed and create next occurrence if recurring.
        
        For recurring tasks (daily or weekly):
        - Sets completed to True
        - Creates a new task instance with due_date = today + offset
        - Adds the new task to the pet's task list
        """
        self.completed = True
        
        # Handle recurring tasks
        if self.frequency in ("daily", "weekly") and self.pet is not None:
            next_task = self.create_next_occurrence()
            if next_task is not None:
                self.pet.add_task(next_task)

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next occurrence of a recurring task.
        
        For daily tasks: due_date = today + 1 day
        For weekly tasks: due_date = today + 7 days
        
        Returns:
            A new Task instance with the same attributes but:
            - completed = False
            - due_date updated based on frequency
            - Or None if frequency is "once" (not recurring)
        
        Uses datetime.timedelta for date calculations:
        - timedelta(days=1): for daily recurrence
        - timedelta(days=7): for weekly recurrence
        """
        if self.frequency == "once":
            return None
        
        # Calculate days to add based on frequency
        days_to_add = 1 if self.frequency == "daily" else 7
        today = date.today()
        
        # Calculate the new due date using timedelta
        new_due_date = today + timedelta(days=days_to_add)
        
        # Create a new task with the same attributes
        new_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            description=self.description,
            pet=None,  # Will be set when added to pet
            frequency=self.frequency,
            completed=False,  # New tasks start as incomplete
            scheduled_time=self.scheduled_time,
            due_date=new_due_date
        )
        
        return new_task

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

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time (earliest first).
        
        Uses a lambda function to handle None values by placing unscheduled 
        tasks at the end. Python's time objects are comparable, so we can 
        sort directly or use time.max as a fallback.
        """
        if not tasks:
            return []
        
        # Sort by scheduled_time, placing unscheduled tasks (None) at the end
        sorted_tasks = sorted(
            tasks,
            key=lambda t: t.scheduled_time if t.scheduled_time is not None else time.max
        )
        return sorted_tasks

    def filter_by_completion_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by completion status.
        
        Args:
            tasks: List of tasks to filter
            completed: True to get completed tasks, False to get incomplete tasks
            
        Returns:
            List of tasks matching the completion status
        """
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet_name(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name.
        
        Args:
            tasks: List of tasks to filter
            pet_name: Name of the pet to filter by
            
        Returns:
            List of tasks belonging to the specified pet
        """
        return [task for task in tasks if task.pet and task.pet.get_name().lower() == pet_name.lower()]

    def detect_time_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect lightweight scheduling conflicts without crashing.
        
        Checks for:
        1. Multiple tasks scheduled at the same time (globally)
        2. Same pet with multiple tasks at the same time (pet conflict)
        
        Args:
            tasks: List of tasks to check for conflicts
            
        Returns:
            List of warning messages describing conflicts found
        """
        warnings = []
        
        # Only consider tasks with scheduled times
        scheduled_tasks = [t for t in tasks if t.scheduled_time is not None]
        
        if not scheduled_tasks:
            return warnings
        
        # Check for global time conflicts (any two tasks at same time)
        time_groups = {}
        for task in scheduled_tasks:
            time_key = task.scheduled_time
            if time_key not in time_groups:
                time_groups[time_key] = []
            time_groups[time_key].append(task)
        
        # Flag times with multiple tasks
        for scheduled_time, tasks_at_time in time_groups.items():
            if len(tasks_at_time) > 1:
                time_str = scheduled_time.strftime("%H:%M")
                task_descriptions = []
                
                # Check if same pet has multiple tasks at this time
                pet_times = {}
                for task in tasks_at_time:
                    pet_name = task.pet.get_name() if task.pet else "Unknown"
                    if pet_name not in pet_times:
                        pet_times[pet_name] = []
                    pet_times[pet_name].append(task)
                    task_descriptions.append(f"{task.get_title()} ({pet_name})")
                
                # Warn about same pet conflicts (high priority)
                for pet_name, pet_tasks in pet_times.items():
                    if len(pet_tasks) > 1:
                        task_names = ", ".join([t.get_title() for t in pet_tasks])
                        warning = f"[CONFLICT] {pet_name} has multiple tasks at {time_str}: {task_names}"
                        warnings.append(warning)
                
                # Warn about global conflicts (lower priority, informational)
                if len(task_descriptions) > 1:
                    tasks_str = ", ".join(task_descriptions)
                    warning = f"[INFO] Multiple tasks scheduled at {time_str}: {tasks_str}"
                    warnings.append(warning)
        
        return warnings

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
