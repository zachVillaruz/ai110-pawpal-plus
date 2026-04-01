import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Settings")
owner_name = st.text_input("Owner name", value="Jordan", key="owner_name")

# Initialize owner in session state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        preferences={"max_daily_minutes": 480}
    )

owner = st.session_state.owner
owner.name = owner_name  # Keep owner name in sync with input

st.markdown("### Manage Pets")
st.caption("Add a new pet to the household.")

col1, col2, col3 = st.columns(3)
with col1:
    new_pet_name = st.text_input("New pet name", value="Whiskers", key="new_pet_name")
with col2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_species")
with col3:
    new_age = st.number_input("Age", min_value=0, max_value=50, value=1, key="new_age")

if st.button("Add Pet"):
    # Check if pet already exists
    existing_pet = None
    for p in owner.get_pets():
        if p.get_name().lower() == new_pet_name.lower():
            existing_pet = p
            break
    
    if existing_pet:
        st.warning(f"🐾 {new_pet_name} is already in the household!")
    else:
        # Create new pet using Pet class
        new_pet = Pet(
            name=new_pet_name,
            species=new_species,
            age=new_age
        )
        # Add pet to owner using Owner.add_pet() method
        owner.add_pet(new_pet)
        st.success(f"✅ {new_pet_name} ({new_species}) added to {owner.get_name()}'s household!")

# Display current pets
if owner.get_pets():
    st.write(f"**Pets in household:** {len(owner.get_pets())}")
    for pet in owner.get_pets():
        st.caption(f"🐾 {pet.get_name()} ({pet.get_species()}, age {pet.get_age()})")
        if pet.get_special_needs():
            st.caption(f"   Special needs: {', '.join(pet.get_special_needs())}")

st.markdown("### Tasks")
st.caption("Add a task for one of your pets.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
with col4:
    # Dropdown to select which pet gets the task
    pet_names = [p.get_name() for p in owner.get_pets()]
    if pet_names:
        selected_pet_name = st.selectbox("Pet", pet_names, key="task_pet")
    else:
        selected_pet_name = None

if st.button("Add Task"):
    if not owner.get_pets():
        st.warning("⚠️ No pets yet. Please add a pet first!")
    else:
        # Find the selected pet
        pet = None
        for p in owner.get_pets():
            if p.get_name() == selected_pet_name:
                pet = p
                break
        
        if pet:
            # Create task
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority
            )
            # Add task to pet using Pet.add_task() method
            pet.add_task(task)
            st.success(f"✅ Added '{task_title}' ({priority}) to {pet.get_name()}!")
        else:
            st.error("Could not find selected pet.")

# Display tasks from pets
if owner.get_all_tasks():
    st.write("Current tasks:")
    task_data = []
    for pet in owner.get_pets():
        for task in pet.get_tasks():
            task_data.append({
                "Pet": pet.get_name(),
                "Task": task.get_title(),
                "Duration (min)": task.get_duration(),
                "Priority": task.get_priority()
            })
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button will generate an optimized schedule based on your tasks.")

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("⚠️ No tasks added yet. Please add at least one task first.")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        if schedule["success"]:
            st.success("✅ Schedule generated successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", schedule["num_tasks"])
            with col2:
                st.metric("Total Time (min)", schedule["total_duration_minutes"])
            with col3:
                st.metric("Owner", schedule["owner"])
            
            st.markdown("### Scheduled Tasks")
            for i, task in enumerate(schedule["tasks"], 1):
                with st.expander(f"{i}. [{task['priority'].upper()}] {task['title']} ({task['pet']})"):
                    st.write(f"**Pet:** {task['pet']}")
                    st.write(f"**Duration:** {task['duration']} minutes")
                    st.write(f"**Priority:** {task['priority'].upper()}")
                    if task['description']:
                        st.write(f"**Description:** {task['description']}")
            
            st.markdown("### Plan Explanation")
            st.info(schedule["explanation"])
        else:
            st.error(f"❌ Error: {schedule['message']}")
