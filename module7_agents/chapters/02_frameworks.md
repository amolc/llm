# Chapter 7.2: LangChain, LangGraph, LlamaIndex

Building complex agent workflows requires robust frameworks that handle state, memory, and routing.

---

## **1. LangChain: The Swiss Army Knife**
LangChain provides the building blocks for LLM applications. It uses **Chains** to link prompts, models, and tools.

- **LCEL (LangChain Expression Language)**: A declarative way to build complex chains.
- **Example**: `prompt | model | parser`

---

## **2. LangGraph: Cyclic Agent Workflows**
While LangChain is mostly linear (DAGs), **LangGraph** allows for **cyclic** workflows. This is essential for agents that need to:
1.  Attempt a task.
2.  Receive an error or feedback.
3.  **Go back** and retry or fix the error.

### **Stateful Agents**
LangGraph manages a shared `State` object that stores everything the agent has learned so far.

---

## **3. LlamaIndex: Data-Driven Agents**
While LangChain is "task-centric," **LlamaIndex** is "data-centric." It focuses on how an agent can intelligently query a complex index of data.

- **Query Engines**: Simple RAG.
- **Data Agents**: Intelligent routers that decide *which* index to query based on the user's intent.

---

## **4. Sample Code: Simple LangChain Tool Chain**

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool

# 1. Define a tool
def calculator(query: str):
    """Calculates a mathematical expression."""
    return eval(query)

# 2. Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key="YOUR_API_KEY")

# 3. Create a Tool object
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for when you need to answer questions about math."
    )
]

# 4. Initialize the agent
agent = initialize_agent(
    tools, 
    llm, 
    agent="zero-shot-react-description", 
    verbose=True
)

# 5. Run the agent
agent.run("What is 15% of 325?")
```

---

## **Recommended Reading**
1.  **[LangGraph: Multi-Agent Workflows](https://python.langchain.com/docs/langgraph/)**
2.  **[LlamaIndex: Agentic RAG](https://docs.llamaindex.ai/en/stable/use_cases/agents/)**
