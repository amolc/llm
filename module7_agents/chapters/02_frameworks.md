# Chapter 7.2: Agent Frameworks – LangChain, LangGraph, LlamaIndex

Building complex agent workflows requires robust frameworks that handle state, memory, and routing. Each framework has a unique philosophy and use case.

---

## **1. LangChain: The Swiss Army Knife**
LangChain is the most mature framework, focusing on **chains** of operations.

### **A. LCEL (LangChain Expression Language)**
LCEL is a declarative way to build chains using the `|` operator. It handles async, streaming, and parallel execution out of the box.

```python
# Simple LCEL Chain
chain = prompt | model | output_parser
```

### **B. Why Use LangChain?**
- **Interoperability**: Connect to 100+ Vector DBs, Tools, and LLMs.
- **Pre-built Chains**: Ready-to-use chains for RAG, SQL, and API interaction.
- **Prompt Hub**: Access community-verified prompts.

---

## **2. LangGraph: Cyclic Agent Workflows**
While standard LangChain is linear (DAGs), **LangGraph** allows for **cyclic** workflows—essential for reasoning loops.

### **A. The State Machine Pattern**
LangGraph treats an agent as a state machine. Every node in the graph can read from and write to a shared `State` object.

```text
[ START ] --> [ Agent Node (Thought) ]
                    |
                    v
          { Should we use a Tool? }
          /           \
      [ Yes ]        [ No ]
        |              |
  [ Tool Node ]        v
        |          [ END ]
        \---(Loop)---/
```

### **B. Key Features**
- **Persistence**: Save and resume agent state across sessions (checkpoints).
- **Human-in-the-Loop**: Pause execution to get user approval before a tool runs.
- **Fine-grained Control**: Explicitly define the edges and nodes of your reasoning graph.

---

## **3. LlamaIndex: Data-Driven Agents**
While LangChain is "task-centric," **LlamaIndex** is "data-centric." It excels at building agents that can query massive, complex datasets.

### **A. Query Routing Architecture**
An agent acts as a router that decides which "Query Engine" is best suited for a specific question.

```text
User Query: "Compare Q3 vs Q4 financial risks"
       |
[ LlamaIndex Router Agent ]
       |
-----------------------
|          |          |
[ Q3 RAG ] [ Q4 RAG ] [ SQL DB ]
```

### **B. Agentic RAG**
Unlike simple RAG (Retrieve -> Answer), Agentic RAG allows the agent to:
1.  Decompose a query into sub-tasks.
2.  Search multiple indices sequentially.
3.  Synthesize a final answer from disparate sources.

---

## **4. Code Comparison: LangChain vs. LangGraph**

### **LangChain (Simple ReAct)**
```python
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
tools = [Tool(name="Search", func=search_func, description="Search the web")]

# One-liner, but less control over the loop
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
agent.run("What is the current price of Gold?")
```

### **LangGraph (Custom Reasoning Graph)**
```python
from langgraph.graph import StateGraph, END

# Define a more robust, stateful graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("action", "agent")

app = workflow.compile()
# Now you have full control over the 'should_continue' logic!
```

---

## **5. Summary Comparison**

| Framework | Best For | Philosophy |
| :--- | :--- | :--- |
| **LangChain** | Rapid prototyping, simple chains | Chains of components |
| **LangGraph** | Production agents, complex loops | State Machines & Graphs |
| **LlamaIndex** | Knowledge management, complex data | Data retrieval & Routing |

---

## **Recommended Reading**
1.  **[LangGraph: Why Graphs for Agents?](https://blog.langchain.dev/langgraph/)**
2.  **[LlamaIndex: Building Data Agents](https://docs.llamaindex.ai/en/stable/use_cases/agents/)**
3.  **[LCEL: The LangChain Expression Language Guide](https://python.langchain.com/docs/expression_language/)**
