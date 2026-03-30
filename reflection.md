# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I want there to be classes for pet tasks, daily plan, owner, and pet.

The owner has information pertaining to themselves and their account.
They have the ability to login and register their pet, as well as look at and edit information about their pet.
The pet should have information relevant to them like their breed, age, name, etc.
Pet tasks should contain a list of tasks that is associated with.
Pet tasks can be updated and can generate a summary/report.
The plan has a date, list of tasks, approximate time it takes.
Tasks can be added to the plan and displayed.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes to the plan I added a scheduler class because Claude suggested it and it made sense to have something that tracks all the individual plans. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Time and duration mattered the most because two tasks cannot be schedule at the same time. So the scheduler only really tracks the time tasks happens but not every what pet they belong to.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler will only fit in a task that has an ample amount of time to do. If the owner has scheduled 30 mins of walking but we only have 20 mins left, we will not implement the task at all even if the owner is fine with it. This feels okay however because it makes sense as most people would want the full duration.

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
