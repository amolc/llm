# Chapter 7.3: AutoGen, CrewAI & Multi-Agent Systems

When a task is too complex for a single agent, we use **Multi-Agent Systems (MAS)**.

---

## **1. Multi-Agent Architectures**
Different agents can have specialized roles, just like a human team.

- **Manager Agent**: Coordinates the workflow and delegates tasks.
- **Worker Agent**: Performs specific actions (e.g., Search Agent, Code Agent).
- **Critic Agent**: Reviews the output for errors or compliance.

---

## **2. Popular Multi-Agent Frameworks**

### **A. Microsoft AutoGen**
Focuses on **conversational** multi-agent interactions.
- **Key Concept**: Agents talk to each other to solve a problem.
- **Autonomous Coding**: One agent writes code, another executes it, and a third debugs it.

### **B. CrewAI: Role-Playing Agents**
Focuses on **collaborative** workflows.
- **Key Concept**: Define "Agents" with specific roles (e.g., Researcher, Writer) and assign them to "Tasks" in a "Crew."
- **Goal-Oriented**: Each agent has a clear goal and a set of tools.

---

## **3. Sample Code: A Simple CrewAI Crew**

```python
from crewai import Agent, Task, Crew, Process

# 1. Define Agents
researcher = Agent(
  role='Financial Researcher',
  goal='Analyze the Q3 earnings of Company X',
  backstory='Expert in reading balance sheets and identifying risks.',
  verbose=True,
  allow_delegation=False
)

writer = Agent(
  role='Financial Content Writer',
  goal='Summarize the research into a 3-bullet point report',
  backstory='Excellent at turning complex data into clear insights.',
  verbose=True,
  allow_delegation=True
)

# 2. Define Tasks
task1 = Task(description='Search for Company X Q3 earnings report.', agent=researcher)
task2 = Task(description='Summarize findings for a busy executive.', agent=writer)

# 3. Form the Crew
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  process=Process.sequential # Task 2 starts after Task 1 finishes
)

# 4. Kickoff!
result = crew.kickoff()
print(result)
```

---

## **Recommended Reading**
1.  **[AutoGen: Enabling Next-Gen LLM Applications](https://microsoft.github.io/autogen/)**
2.  **[CrewAI: Multi-Agent Systems for Developers](https://www.crewai.com/)**
