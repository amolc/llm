# Essential AI Topics

This guide provides a compact, practical introduction to modern AI and how to turn ideas into working generative AI products. It is organized as three sections that build on each other: foundations, prompt engineering, and application development.

---

## 1) Introduction to AI

### Key Terms
- Artificial Intelligence (AI): Systems that perform tasks that normally require human intelligence such as perception, reasoning, and language.
- Machine Learning (ML): A subset of AI where models learn patterns from data rather than being explicitly programmed.
- Deep Learning (DL): A subset of ML that uses multi‑layer neural networks (e.g., transformers) to learn complex representations from large datasets.
- Artificial General Intelligence (AGI): A hypothetical system that can perform any intellectual task that humans can, across diverse domains without task‑specific training.

### Core Concepts
- Data → Features/Embeddings → Model → Prediction → Evaluation → Deployment → Monitoring.
- Supervised learning: map inputs to labeled outputs (classification, regression).
- Unsupervised learning: discover structure (clustering, dimensionality reduction).
- Reinforcement learning: learn actions from reward signals (policy optimization).

### Modern Language Models
- Pretraining: models learn general language patterns on large corpora.
- Instruction tuning: models are further trained to follow tasks from examples.
- Preference optimization: models align to human preferences for style and helpfulness.

Recommended foundations: attention mechanisms, tokenization, embeddings, and the transformer architecture. See the course materials in this repo for deep dives, such as [Module 6: Embeddings & Vector Databases](file:///Users/amolc/2026/llm/vectordb.md) and [Module 7: Agent Architectures](file:///Users/amolc/2026/llm/AGENTS.md).

---

## 2) Prompt Engineering & ChatGPT

### What Is Prompt Engineering
Prompt engineering is the practice of designing inputs to a language model to elicit reliable, high‑quality outputs. It combines instruction clarity, examples, constraints, and formatting to guide model behavior.

### Principles
- State the role and goal up front. Be explicit, concise, and unambiguous.
- Specify output format and constraints (length, tone, JSON schema).
- Provide high‑quality examples (few‑shot) when deterministic structure is needed.
- Use chain‑of‑thought for multi‑step reasoning when allowed, or solicit intermediate steps in a structured way.
- Iterate: measure prompt performance and refine based on error patterns.

### Useful Patterns
- Instruction + Context + Constraints + Output Format.
- Few‑shot examples: show inputs and correct outputs.
- Chain‑of‑thought: encourage reasoning before final answers.
- ReAct: interleave reasoning with tool usage in agents.

### ChatGPT/LLM Use Cases for Data Analysis
- Data cleaning instructions (e.g., mapping categories, dedup rules).
- Exploratory analysis: summarize trends from text, comments, or logs.
- SQL generation from natural language schemas.
- Report drafting: convert analytics into structured prose with charts or bullet points.
- Quality checks: validate outputs against rules, red‑flag anomalies.

Example prompt structure for analysis:

```
Role: Senior Data Analyst.
Task: Analyze the following sales notes and produce three insights and one risk.
Context: <paste notes>
Constraints: Use bullet points; max 120 words; no speculation.
Output:
- Insight 1:
- Insight 2:
- Insight 3:
- Risk:
```

### Guardrails & Safety
- Red‑team prompts: inject invalid inputs and ensure safe, robust responses.
- Grounding: require citations to provided context to reduce hallucinations.
- Filters: block PII and disallowed content where required.

---

## 3) Building Generative AI Applications

### Minimal Architecture
- Client/UI → API layer → Model layer → Optional Retrieval (RAG) → Observability.
- For knowledge‑centric apps, pair the model with a vector database for retrieval.

### Prototyping
- Start with a notebook and an SDK call to a small, fast model.
- Define a few “golden” examples that represent typical tasks and edge cases.
- Iterate prompts until the baseline is stable and measurable.

### From Prototype to Product
- Retrieval: index documents as embeddings; design chunking and metadata filters.
- Orchestration: manage multi‑step workflows (Prompt Flow, LangChain, LangGraph).
- Agents: use tool invocation for actions (search, calculators, APIs) and add memory when tasks span multiple steps. See [Agent Memory & Observability](file:///Users/amolc/2026/llm/module7_agents/chapters/04_memory_observability.md).
- Evaluation: create a golden set, measure accuracy, cost, latency, groundedness, and safety. See [LLM CI/CD & Prompt Regression Testing](file:///Users/amolc/2026/llm/chapters/11_llm_cicd_prompt_regression.md).

### Deployment
- Serverless endpoints for simple inference; GPUs for low latency and larger models.
- Caching and request deduplication to reduce cost.
- Monitor TTFT, tokens/sec, error rates, and output quality drift.

### Improving Performance
- Data strategies first: better retrieval, tighter prompts, output schemas.
- Parameter‑efficient tuning: LoRA/QLoRA adapters for task consistency and tone. See [Fine‑Tuning, LoRA, QLoRA](file:///Users/amolc/2026/llm/chapters/09_fine_tuning_lora_qlora.md).
- Compression: quantization/pruning for latency and memory. See [Model Compression & Distillation](file:///Users/amolc/2026/llm/chapters/10_model_compression_distillation.md).

### Evaluation Techniques for NLP Models
- Task metrics: exact match, F1, BLEU/ROUGE for structured outputs.
- LLM‑as‑a‑judge: rubric‑based scoring for style, helpfulness, and safety.
- Human review on a small but representative subset for ground truth.
- Regression tests: run golden sets on every change with automated gates for accuracy, latency, and cost.

---

## Quick Start Links in This Repo
- Vector databases and RAG concepts: [vectordb.md](file:///Users/amolc/2026/llm/vectordb.md)
- Agent architectures and tools: [AGENTS.md](file:///Users/amolc/2026/llm/AGENTS.md)
- CI/CD and regression testing for LLMs: [11_llm_cicd_prompt_regression.md](file:///Users/amolc/2026/llm/chapters/11_llm_cicd_prompt_regression.md)
