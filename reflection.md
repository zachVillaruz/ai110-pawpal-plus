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
    The program considers constraints like time (max_daily_minutes being 480 minutes), scheduled_time (detecting conflicts when two tasks overlap) or even a due_date (tracking when tasks need to occur). The scheduler also considers things like priority levels or valid inputs for variables (tasks needing to have a positive number for duration, priority being valid, pending tasks only)
- How did you decide which constraints mattered most?
    We decided priority, duration, time conflicts and then max daily duration. We sorted the tasks from high to low (priority), then by the shorter tasks to the longer tasks, then detecting to see if any tasks have time conflicts, before adding a hard limit in the max daily duration, ending the scheduler early if the time limit is reached.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    The AI suggested making a simplified nested-loop version of the scheduler, which would make it far more readable to human readers while also using less memory. However, if the list of tasks was large, it becomes far slower, making the performance difference much more noticeable.
- Why is that tradeoff reasonable for this scenario?
    It isn't, which is why I chose not to make the tradeoff. Maybe for some people they have pets that are low-maintenance, and don't require a lot of tasks. But there is bound to be a lot of people with pets that require a lot of care and handling. In this case, it would be better to ensure that every pet owner has the best performance at all times, even if that means a less readable code or more memory taken up.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    It helped make the code for a lot of the project, like the classes, the methods inside each class, and even the small stuff like the commits. But I did at the very least skim over the changes to make sure they made sense, and if anything seemed wrong, then I would revert any changes and ask the AI to come up with something else that was more correct.
- What kinds of prompts or questions were most helpful?
    The ones that the specification hinted for me to give as prompts. Something like in Phase 1, when the specification recommended for me to ask CoPilot: "Based on my skeletons in #file:pawpal_system.py, how should the Scheduler retrieve all tasks from the Owner's pets?" I didn't have to worry if what I came up with to ask the AI was wrong or not, this was very easy to determine to ask.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    The AI suddenly asked me if it could make a virtual machine to test out the code, which I had not recalled seeing in the specification before. That was when I quickly knew that the AI was going off the rails, and that I had to go about a different approach.
- How did you evaluate or verify what the AI suggested?
    It was very easy. A virtual machine was not something we were expected to work with in this project. Not once does it show up in the specification, and although I have a broad understanding of it, I don't know virtual machines enough to be able to work with it. So I deleted the virtual machine it set up, and encouraged the AI to test the code a different way.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    As mentioned in the README, the tests test for things like making sure a task completes properly or can be added, checking for task confliction, any sorting errors, and other various things.
- Why were these tests important?
    Because they were a proper function that the AI was able to code on the application. We'd need to be able to test that that function works without any errors, so making a test to test these things is very important.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Mostly, but not entirely. The tests passed fine, but as I said in the README, there is no surefire way to ensure if a program will work 100% or not. It's just not possible in a human sense, and it's probably not possible in a technical sense either. There are always bugs, no matter what.
- What edge cases would you test next if you had more time?
    Probably the edge cases where if a task was just exactly on the limit. Like a task that takes 480 minutes exactly. I didn't have much time when I attempted this project, so I didn't have time to get to test this sadly.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    Making the classes stubs, because I felt like I understood everything that was going on in the code. I still do now, but to a bit of a lesser extent due to how long the code was getting.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I'd figure out how to improve performance, finding out if there's any ways to lower memory used up, so that people with lower-end devices can use this application without any slowdown.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    It's a lot of work. AI can get you far when doing things like this, but you still need to be a second eye to make sure it's not suggesting anything odd or incorrect.
