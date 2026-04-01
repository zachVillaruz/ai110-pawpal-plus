"""
Main script to demonstrate the PawPal+ scheduling system.
Creates sample data, generates a schedule, and displays it.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


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
    
    # Create tasks for Mochi
    task1 = Task(
        title="Morning walk",
        duration_minutes=20,
        priority="high",
        description="Energetic walk around the block",
        frequency="daily"
    )
    
    task2 = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        description="Feed Mochi dog food (no chicken)"
    )
    
    task3 = Task(
        title="Playtime",
        duration_minutes=30,
        priority="medium",
        description="Interactive play with toys"
    )
    
    # Create tasks for Whiskers
    task4 = Task(
        title="Cat feeding",
        duration_minutes=5,
        priority="high",
        description="Feed Whiskers at usual time"
    )
    
    task5 = Task(
        title="Medication",
        duration_minutes=10,
        priority="high",
        description="Give Whiskers noon medication",
        frequency="daily"
    )
    
    task6 = Task(
        title="Litter box cleaning",
        duration_minutes=15,
        priority="medium",
        description="Clean and refill litter box"
    )
    
    # Add tasks to pets
    mochi.add_task(task1)
    mochi.add_task(task2)
    mochi.add_task(task3)
    
    whiskers.add_task(task4)
    whiskers.add_task(task5)
    whiskers.add_task(task6)
    
    print(f"Tasks created: {len(owner.get_all_tasks())} total\n")
    print("=" * 60)
    
    # Create scheduler and generate schedule
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    
    # Display results
    print("\n🐾 TODAY'S SCHEDULE 🐾\n")
    
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
