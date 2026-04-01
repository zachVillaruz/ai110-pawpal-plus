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

## Features

### Core Scheduling Algorithms

- **Priority-Based Sorting**: Tasks are ordered from high → medium → low priority, then by duration (short tasks first). This ensures critical pet care activities (medications, feeding) are scheduled before enrichment activities.

- **Time-Based Chronological Sorting**: Tasks can be sorted by their scheduled time to display the day's plan chronologically. Unscheduled tasks appear at the end.

- **Daily Recurrence Management**: When a recurring daily task is marked complete, the system automatically generates a new task instance for the next day, maintaining task continuity. Weekly recurrence supported.

- **Conflict Detection**: The scheduler detects two types of conflicts:
  - **Critical conflicts**: Same pet with multiple tasks scheduled at the exact same time
  - **Informational warnings**: Multiple pets requiring attention at the same time (resource planning)

### Filtering & Aggregation

- **Filter by Completion Status**: Distinguish between completed tasks (for history) and pending tasks (for scheduling)

- **Filter by Pet Name**: View all tasks for a specific pet across the entire schedule

- **Multi-Pet Task Aggregation**: Owner can access all tasks from all pets with a single call, enabling household-level scheduling

### Constraint Validation

- **Max Daily Time Limit**: Enforces maximum daily time budgets (default 480 min / 8 hours) to prevent overcommitment and burnout

- **Task Duration Validation**: Ensures all tasks have positive, realistic durations

- **Priority Constraint Checking**: Validates that priority values are valid ("low", "medium", "high")

- **Data Integrity Checks**: Verifies all required task fields are present before scheduling

### User Experience

- **Human-Readable Explanations**: The scheduler provides step-by-step explanation of the plan, showing why each task was selected and in what order

- **Interactive UI**: Streamlit app allows users to:
  - Add/manage multiple pets in a household
  - Add tasks with priority and duration
  - View tasks organized by pet or by time
  - Generate and visualize optimized daily schedules
  - See conflict warnings with resolution suggestions

### Testing Coverage

The project includes **19 unit tests** covering:

- Task completion and recurring task generation (daily/weekly)
- Task addition and pet management
- Time-based sorting correctness (chronological order)
- Conflict detection (same-pet and cross-pet)
- Constraint validation (duration, priority, time limits)
- Edge cases (empty lists, unscheduled tasks, orphaned tasks)

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


### Testing PawPal+

If you run "python -m pytest" it should tell you that all 19 tests have passed with flying colors. The test covers things like making sure a task completes or can be added, checking for task confliction, any sorting errors, and more. However, I will rate it 4 stars, as there is always room for error in a program, no matter what, and I don't think it would ever be possible to be 100% confident that a program will ALWAYS work as intended (which would be worthy of a 5 star rating).

### 📸 Demo
<a href="/course_images/ai110/final_streamlit_app.png" target="_blank"><img src='/course_images/ai110/final_streamlit_app.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>