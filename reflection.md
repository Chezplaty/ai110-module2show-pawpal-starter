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

I used AI to help me brainstorm and draft out what I wanted. I found it helpful to ask what would look best and be most efficient when implementing someone since I am not too familiar with streamlit.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Claude had implemented the conflict scheduling without updating how it would affect actually saving the plan. I had to verify and test it myself and saw that it allowed schedules with conflicts to be saved. I reprompted it to fix it. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested almost all the behavior, especially when it came to creating a schedule. These tests were important because they are the main componenets of the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am pretty confident that it works correctly. I would maybe want to test owners with the same name and same pet name. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I most satisfied with how saving the plan and schedule worked at the end. The UI also feels pretty clean and not hard to understand.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would probably try to implement more options when adding tasks and different ways the owners are displayed. Owners should be logged in, not be added by someone else.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

That AI is very handy when it comes to implementing my features, but I still need to come up with them and always verify that they work. Sometimes the AI implements a feature without checking how it works with others.