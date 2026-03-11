# Chapter 7.3: AutoGen, CrewAI & Multi-Agent Systems

When a task is too complex for a single agent to handle effectively, we use **Multi-Agent Systems (MAS)**. This mirrors a human organization where specialized roles collaborate to solve a problem.

---

## **1. Multi-Agent Architectures: Three Core Patterns**

### **A. Sequential Workflow (Linear Pipeline)**
Agents work in a pre-defined order. The output of one agent becomes the input for the next.

```text
[ Researcher ] --> [ Data Analyst ] --> [ Report Writer ]
```
- **Example**: A news aggregator where Agent 1 finds articles, Agent 2 summarizes them, and Agent 3 posts them to social media.

---

### **B. Hierarchical Workflow (Manager-Led)**
A central **Manager Agent** receives the high-level goal, breaks it into sub-tasks, and delegates them to specialized workers.

```text
          [ Manager Agent ]
          /       |       \
[ Researcher ] [ Coder ] [ Reviewer ]
```
- **Example**: A software project where the Manager assigns feature implementation to the Coder and quality check to the Reviewer.

---

### **C. Joint Collaboration (Conversational/Peer-to-Peer)**
Agents interact in a shared conversation space. They can debate, peer-review, and collectively decide on the best outcome.

```text
      [ Agent A ] <--> [ Agent B ]
          ^              ^
          |              |
          v              v
      [ Agent C ] <--> [ Agent D ]
```
- **Example**: A design brainstorm where a UI Agent, UX Agent, and Backend Agent negotiate the constraints of a new feature.

---

## **2. Framework Implementation Examples**

### **Example 1: Hierarchical Workflow with CrewAI**
*CrewAI excels at role-playing and managed delegation.*

```python
from crewai import Agent, Task, Crew, Process

# 1. Define specialized agents
researcher = Agent(
    role='Market Analyst',
    goal='Identify emerging trends in AI',
    backstory='Senior analyst with 10 years of experience in tech trends.'
)

writer = Agent(
    role='Content Strategist',
    goal='Create a viral LinkedIn post based on trends',
    backstory='Expert in digital marketing and social engagement.'
)

# 2. Form a Hierarchical Crew (using a Manager)
crew = Crew(
    agents=[researcher, writer],
    tasks=[...], # Define tasks for each agent
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4") # The Manager coordinates the delegation
)

result = crew.kickoff()
```

---

### **Example 2: Joint Collaboration with AutoGen**
*AutoGen is built for peer-to-peer conversation and autonomous problem solving.*

```python
import autogen

# 1. Define the User Proxy (The Human Interface)
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin who supervises the agents."
)

# 2. Define the Specialized Agents
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config={"config_list": config_list},
    system_message="I write Python code to solve tasks."
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="I execute the code written by the Coder and report results.",
    code_execution_config={"work_dir": "coding"}
)

# 3. Start a Group Chat (Joint Collaboration)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, executor], messages=[])
manager = autogen.GroupChatManager(groupchat=groupchat)

user_proxy.initiate_chat(manager, message="Calculate the 50-day moving average of TSLA.")
```

---

## **3. When to Use Multi-Agent Systems?**

Multi-agent systems add complexity (latency, cost). Use them only when:
1.  **Task Separation**: The task requires distinct, conflicting skillsets (e.g., Creative Writing vs. Strict Fact-Checking).
2.  **Scalability**: You need to parallelize sub-tasks across multiple models.
3.  **Reliability**: You need a "Critic" agent to independently verify the "Worker" agent's output.

---

## **Summary Analysis**

- **CrewAI**: Best for **structured workflows** (Sequential/Hierarchical). It feels like managing a team.
- **AutoGen**: Best for **open-ended reasoning** and **coding**. It feels like a chat room of experts.

---

## **Recommended Reading**
1.  **[CrewAI: Hierarchical Processes](https://docs.crewai.com/how-to/Hierarchical-Process/)**
2.  **[AutoGen: Group Chat Introduction](https://microsoft.github.io/autogen/docs/tutorial/groupchat)**
3.  **[Multi-Agent Systems: A Survey](https://arxiv.org/abs/2401.03428)**
