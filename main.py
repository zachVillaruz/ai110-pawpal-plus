"""
Main script to demonstrate the PawPal+ scheduling system.
Creates sample data, generates a schedule, and displays it.
Demonstrates sorting and filtering functionality.
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import time


def main():
    """Run the PawPal+ scheduler demo."""
    
    # Create an owner
    owner = Owner(
        name="Jordan",
        email="jordan@example.com",
        phone="555-1234",
        preferences={"max_daily_minutes": 480}  # 8 hours max per day
    )
    print(f"Owner: {owner.get_name()}\n")
    
    # Create pets
    mochi = Pet(
        name="Mochi",
        species="dog",
        age=3,
        special_needs=["needs exercise", "allergic to chicken"]
    )
    
    whiskers = Pet(
        name="Whiskers",
        species="cat",
        age=5,
        special_needs=["requires medication at noon"]
    )
    
    # Add pets to owner
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    print(f"Pets: {', '.join([p.get_name() for p in owner.get_pets()])}\n")
    
    # Create tasks for Mochi - OUT OF ORDER
    task1 = Task(
        title="Playtime",
        duration_minutes=30,
        priority="medium",
        description="Interactive play with toys",
        frequency="daily"
    )
    task1.set_scheduled_time(time(14, 30))  # 2:30 PM
    
    task2 = Task(
        title="Morning walk",
        duration_minutes=20,
        priority="high",
        description="Energetic walk around the block",
        frequency="daily"
    )
    task2.set_scheduled_time(time(7, 0))  # 7:00 AM
    
    task3 = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        description="Feed Mochi dog food (no chicken)"
    )
    task3.set_scheduled_time(time(7, 0))  # 7:00 AM - SAME TIME AS MORNING WALK (CONFLICT!)
    
    # Create tasks for Whiskers - OUT OF ORDER
    task4 = Task(
        title="Medication",
        duration_minutes=10,
        priority="high",
        description="Give Whiskers noon medication",
        frequency="daily"
    )
    task4.set_scheduled_time(time(12, 0))  # 12:00 PM
    
    task5 = Task(
        title="Cat feeding",
        duration_minutes=5,
        priority="high",
        description="Feed Whiskers at usual time"
    )
    task5.set_scheduled_time(time(8, 0))  # 8:00 AM
    
    task6 = Task(
        title="Litter box cleaning",
        duration_minutes=15,
        priority="medium",
        description="Clean and refill litter box"
    )
    task6.set_scheduled_time(time(12, 0))  # 12:00 PM - SAME TIME AS MEDICATION (CONFLICT!)
    
    # Add tasks to pets (deliberately out of order)
    mochi.add_task(task1)  # Playtime first
    whiskers.add_task(task5)  # Cat feeding
    mochi.add_task(task2)  # Morning walk
    whiskers.add_task(task4)  # Medication
    mochi.add_task(task3)  # Breakfast
    whiskers.add_task(task6)  # Litter box
    
    # Mark some tasks as completed
    task3.mark_complete()  # Breakfast completed
    task5.mark_complete()  # Cat feeding completed
    
    print(f"Tasks created: {len(owner.get_all_tasks())} total\n")
    print("=" * 60)
    
    # Create scheduler
    scheduler = Scheduler(owner)
    
    # Demonstrate filtering and sorting
    print("\n🔍 FILTERING AND SORTING DEMONSTRATION 🔍\n")
    
    all_tasks = owner.get_all_tasks()
    
    # 0. DETECT TIME CONFLICTS
    print("0. CHECKING FOR TIME CONFLICTS:")
    print("-" * 60)
    conflicts = scheduler.detect_time_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  * No time conflicts detected!")
    
    # 1. Filter by completion status - get incomplete tasks
    print("\n1. INCOMPLETE TASKS:")
    print("-" * 60)
    incomplete_tasks = scheduler.filter_by_completion_status(all_tasks, completed=False)
    for task in incomplete_tasks:
        pet_name = task.pet.get_name() if task.pet else "Unknown"
        print(f"  [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min) - {pet_name}")
    
    # 2. Filter by completion status - get completed tasks
    print("\n2. COMPLETED TASKS:")
    print("-" * 60)
    completed_tasks = scheduler.filter_by_completion_status(all_tasks, completed=True)
    for task in completed_tasks:
        pet_name = task.pet.get_name() if task.pet else "Unknown"
        print(f"  [X] [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min) - {pet_name}")
    
    # 3. Filter by pet name - Mochi
    print("\n3. ALL TASKS FOR MOCHI:")
    print("-" * 60)
    mochi_tasks = scheduler.filter_by_pet_name(all_tasks, "Mochi")
    for task in mochi_tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"  {status} [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min)")
    
    # 4. Filter by pet name - Whiskers
    print("\n4. ALL TASKS FOR WHISKERS:")
    print("-" * 60)
    whiskers_tasks = scheduler.filter_by_pet_name(all_tasks, "Whiskers")
    for task in whiskers_tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"  {status} [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min)")
    
    # 5. Sort incomplete tasks by time
    print("\n5. INCOMPLETE TASKS SORTED BY TIME:")
    print("-" * 60)
    incomplete_sorted_by_time = scheduler.sort_by_time(incomplete_tasks)
    for task in incomplete_sorted_by_time:
        pet_name = task.pet.get_name() if task.pet else "Unknown"
        time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "UNSCHEDULED"
        print(f"  {time_str} - [{task.get_priority().upper()}] {task.get_title()} ({task.get_duration()} min) - {pet_name}")
    
    # 6. Generate full schedule
    print("\n" + "=" * 60)
    print("\nTODAY'S FULL SCHEDULE\n")
    
    schedule = scheduler.generate_schedule()
    
    if schedule["success"]:
        print(f"Owner: {schedule['owner']}")
        print(f"Total Tasks: {schedule['num_tasks']}")
        print(f"Total Time Required: {schedule['total_duration_minutes']} minutes\n")
        
        print("-" * 60)
        print("TASKS (Ordered by Priority):")
        print("-" * 60)
        for task in schedule["tasks"]:
            print(f"\n[{task['priority'].upper()}] {task['title']}")
            print(f"  Pet: {task['pet']}")
            print(f"  Duration: {task['duration']} minutes")
            if task['description']:
                print(f"  Description: {task['description']}")
        
        print("\n" + "=" * 60)
        print("\nPLAN EXPLANATION:")
        print("=" * 60)
        print(schedule["explanation"])
    else:
        print(f"Error: {schedule['message']}")


if __name__ == "__main__":
    main()
