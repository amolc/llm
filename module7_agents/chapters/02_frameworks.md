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

## **2. Real-World Analysis: Finance Use Case**

### **The Problem**
A financial analyst needs an agent to:
1.  Fetch the latest Q3 earnings for a company.
2.  Compare it against Q2 data from a local SQL database.
3.  Write a risk assessment report.
4.  **Loop back** if the data is incomplete or conflicting.

### **Framework Analysis**
- **LangChain**: Would struggle with step 4. If the model makes a mistake in step 2, the chain usually fails or returns a hallucination.
- **LlamaIndex**: Excellent at step 1 and 2 (Hybrid search across PDF and SQL), but the "looping back" logic would be custom-coded.
- **LangGraph**: Ideal. You can define a "Reviewer Node" that checks the report for accuracy and sends the agent back to the "Search Node" if metrics are missing.

---

## **3. LangGraph: Deep Dive into Stateful Reasoning**

LangGraph's power lies in its ability to maintain a **shared state** across multiple reasoning steps.

### **A. Advanced State Management Example**

```python
from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, END

# 1. Define the State Object
class AgentState(TypedDict):
    # 'messages' will accumulate over time (operator.add)
    messages: Annotated[List[str], operator.add]
    # 'data_points' tracks specific financial metrics found
    data_points: List[dict]
    # 'needs_more_info' is a boolean flag for the conditional edge
    needs_more_info: bool

# 2. Define Node Functions
def financial_researcher(state: AgentState):
    # Logic to call a search tool or query a DB
    print("--- RESEARCHING FINANCIALS ---")
    new_data = {"metric": "Revenue", "value": "$5.2B"}
    return {
        "messages": ["Found revenue data for Q3."],
        "data_points": [new_data],
        "needs_more_info": False # Change to True to trigger a loop
    }

def auditor(state: AgentState):
    # Logic to verify data consistency
    print("--- AUDITING DATA ---")
    if not state['data_points']:
        return {"needs_more_info": True, "messages": ["Audit failed: No data found."]}
    return {"needs_more_info": False, "messages": ["Audit passed."]}

# 3. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", financial_researcher)
workflow.add_node("auditor", auditor)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "auditor")

# Conditional Routing: If auditor says 'needs_more_info', go back to researcher
workflow.add_conditional_edges(
    "auditor",
    lambda x: "researcher" if x["needs_more_info"] else END
)

app = workflow.compile()
```

---

## **4. LlamaIndex: The "Data-First" Agent Approach**

LlamaIndex treats agents as intelligent interfaces to your data. Its **Router Agent** is the gold standard for multi-source retrieval.

### **Query Decomposition Analysis**
When a user asks: *"Compare the risk profile of Tesla in 2023 vs 2024,"* a LlamaIndex agent performs:
1.  **Sub-Question Query Engine**: Splits the query into "Tesla 2023 risks" and "Tesla 2024 risks."
2.  **Parallel Execution**: Fetches data from two different vector indices simultaneously.
3.  **Synthesis**: Uses a specific "Synthesizer" model to merge the results into a comparison table.

---

## **5. Summary: The Production Agent Stack**

In a professional environment, you often combine these:
- **LlamaIndex** for the retrieval logic (RAG).
- **LangGraph** for the agentic reasoning and tool execution loop.
- **LangChain** for the underlying utility components (parsers, prompt templates).

---

## **Recommended Reading**
1.  **[LangGraph: Multi-Agent Systems](https://langchain-ai.github.io/langgraph/)**
2.  **[LlamaIndex: Agentic RAG Patterns](https://docs.llamaindex.ai/en/stable/use_cases/agents/)**
3.  **[Agent Protocol: A standard for AI Agents](https://agentprotocol.ai/)**
