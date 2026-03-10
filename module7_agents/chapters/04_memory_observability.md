# Chapter 7.4: Agent Memory & Observability

Building agents that "remember" and can be "debugged" is the biggest challenge in production.

---

## **1. Types of Agent Memory**

| Memory Type | Description | Best For |
| :--- | :--- | :--- |
| **Short-Term Memory** | Remembers the current conversation history. | Maintaining context in a chat. |
| **Long-Term Memory** | Stores facts or user preferences across sessions. | Personalization (e.g., "User prefers PDF reports"). |
| **Episodic Memory** | Remembers *how* a task was solved in the past. | Learning from past successes or failures. |
| **External Memory (RAG)** | Queries a Vector DB for external knowledge. | Facts not in the model's training data. |

---

## **2. Agent Observability**
Agents are non-deterministic. They can loop, hallucinate, or fail in ways you didn't expect. **Observability** is the process of seeing "inside the brain" of the agent.

### **A. Key Metrics to Track**
- **Token Usage**: How much did this agent run cost?
- **Latency**: How long did each "Thought" or "Action" take?
- **Traceability**: Which tool was called, and what was the exact output?

### **B. Observability Tools**
1.  **LangSmith**: Detailed traces of every step in a LangChain or LangGraph run.
2.  **Weights & Biases (W&B) Prompts**: Visualizing and versioning agent traces.
3.  **Arize Phoenix**: Open-source observability for RAG and Agents.

---

## **3. Sample Code: Tracing with LangSmith (Pseudo-code)**

```python
import os
from langsmith import Client

# 1. Initialize LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "YOUR_API_KEY"
client = Client()

# 2. Run your agent (LangChain will automatically trace to LangSmith)
# Every thought, tool call, and model response will be logged.

# 3. View the trace:
# Navigate to smith.langchain.com to see the visual "waterfall" 
# of your agent's reasoning process.
```

---

## **Recommended Reading**
1.  **[LangSmith: Tracing and Evaluation](https://docs.smith.langchain.com/)**
2.  **[Weights & Biases: LLM Observability](https://docs.wandb.ai/guides/prompts)**
3.  **[Memory in LangChain: ConversationSummaryMemory](https://python.langchain.com/docs/modules/memory/types/summary/)**
