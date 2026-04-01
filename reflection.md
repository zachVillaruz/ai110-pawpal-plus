# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    I had a hierarchy where the Scheduler class was the highest class, with the Owner, Pet and Task classes inheriting from it. Each class had their own fields and their own methods.

- What classes did you include, and what responsibilities did you assign to each?
    I did the four that the specification asked me to add, namely:
    - Scheduler, which was responsible for generating a schedule for the pet owners to follow.
    - Owner, a class to represent a pet owner. It was responsible for telling the program who the pet belongs to.
    - Pet, a class to represent well... a pet. It's responsible for having information like its name, species, age, and more.
    - Task, a class to represent a task. This helps organize the schedule, and allow there to be tasks with their own title, duration, and more.

**b. Design changes**

- Did your design change during implementation?
    No, it stayed the same. We were required to use the four classes Owner, Pet, Task and Scheduler, and I decided those were fine enough. The AI suggested making a 5th class, Schedule (different from Scheduler), but I deemed that unnecessary.
- If yes, describe at least one change and why you made it.
    No change.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
