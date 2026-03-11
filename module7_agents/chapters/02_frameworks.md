# Chapter 7.2: Agent Frameworks – LangChain, LangGraph, LlamaIndex

Building complex agent workflows requires robust frameworks that handle state, memory, and routing. Each framework has a unique philosophy and use case.

---

## **1. Framework Decision Matrix: When to Use What?**

Choosing the right framework depends on the complexity of your reasoning loop and the nature of your data.

| Feature | LangChain | LangGraph | LlamaIndex |
| :--- | :--- | :--- | :--- |
| **Workflow Type** | Linear DAGs (A -> B -> C) | Cyclic Graphs (A -> B -> A) | Data-Centric Routing |
| **State Management** | Minimal (Chain-based) | Full State Machine (Nodes/Edges) | Index-based context |
| **Primary Goal** | Rapid Integration | Precise Control & Reliability | Advanced RAG & Retrieval |
| **Human-in-the-loop** | Difficult | Native Support (Checkpoints) | Supported via Agents |
| **Best For** | One-off tasks, simple bots | Production Agents, Coding bots | Research, Document QA |

---

## **2. Real-World Analysis: Finance Use Case Comparison**

**The Task**: An agent must:
1.  **Search** for Q3 Revenue of a company.
2.  **Compare** it with Q2 data in a SQL database.
3.  **Validate** the data. If the data is missing or mismatched, **Loop back** and search again.

### **A. LangChain Implementation (Linear/Chains)**
*LangChain excels at speed, but struggles with the "Loop Back" step. If the audit fails, the chain usually just ends or hallucinations start.*

```python
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
tools = [
    Tool(name="Search_Q3", func=lambda x: "Revenue: $5B", description="Get Q3 data"),
    Tool(name="Query_SQL_Q2", func=lambda x: "$4.8B", description="Get Q2 data from SQL")
]

# Simple ReAct agent - hard to enforce a strict 'audit and retry' loop
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Problem: If the search returns bad data, the agent might 'guess' or stop.
response = agent.run("Compare Q3 and Q2 revenue and audit for accuracy.")
```

---

### **B. LlamaIndex Implementation (Data-Centric)**
*LlamaIndex is the best for Step 1 and 2 (complex retrieval), but step 4 (looping) requires custom Python logic outside the library's primary agent classes.*

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool

# 1. Setup specialized query engines
q3_engine = QueryEngineTool.from_defaults(query_engine=vector_index, name="q3_data")
sql_engine = QueryEngineTool.from_defaults(query_engine=sql_index, name="sql_q2_data")

# 2. Setup Data Agent
agent = ReActAgent.from_tools([q3_engine, sql_engine], llm=llm, verbose=True)

# Problem: LlamaIndex is great at retrieval, but the 'loop back to researcher' 
# logic is not a first-class citizen like it is in a graph.
response = agent.chat("Compare Q3 vs Q2 and verify the numbers.")
```

---

### **C. LangGraph Implementation (Stateful/Cyclic)**
*LangGraph is **ideal** for this task. We define an explicit "Auditor" node that can force the graph back to the "Researcher" node if the data is incorrect.*

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# 1. Define State
class FinanceState(TypedDict):
    research_data: str
    audit_passed: bool
    iterations: int

# 2. Define Nodes
def researcher(state: FinanceState):
    print("--- Researcher: Searching for data ---")
    return {"research_data": "$5.2B (Mocked)", "iterations": state.get("iterations", 0) + 1}

def auditor(state: FinanceState):
    print("--- Auditor: Verifying data ---")
    # Custom logic: if it's the first try, force a loop to simulate a fix
    if state["iterations"] < 2:
        return {"audit_passed": False}
    return {"audit_passed": True}

# 3. Build Graph with Cycles
workflow = StateGraph(FinanceState)
workflow.add_node("research", researcher)
workflow.add_node("audit", auditor)

workflow.set_entry_point("research")
workflow.add_edge("research", "audit")

# CRITICAL: The Looping Logic
workflow.add_conditional_edges(
    "audit",
    lambda x: "research" if not x["audit_passed"] else END
)

app = workflow.compile()
# The agent WILL loop back to research until the auditor is satisfied.
```

---

## **3. Summary Analysis**

- **LangChain**: Best for simple, one-shot tools. **Error handling is implicit** (left to the LLM).
- **LlamaIndex**: Best for complex RAG. **Data routing is the priority**.
- **LangGraph**: Best for production. **Error handling is explicit** (defined in the graph architecture).

---

## **Recommended Reading**
1.  **[LangGraph: Why Graphs for Agents?](https://blog.langchain.dev/langgraph/)**
2.  **[LlamaIndex: Agentic RAG](https://docs.llamaindex.ai/en/stable/use_cases/agents/)**
3.  **[LCEL: The LangChain Expression Language Guide](https://python.langchain.com/docs/expression_language/)**
