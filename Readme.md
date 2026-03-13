# LLM & AI Systems: From Foundations to Agents

This repository is a comprehensive guide and toolkit for building production-grade LLM applications. It covers everything from the conceptual foundations of Large Language Models to the practical implementation of autonomous agents and automated lead generation.

---

## **📂 Project Modules**

### **1. Foundations of LLM Systems (`/chapters`)**
The theoretical core of the repository.
- **Workflow**: Understanding the pipeline from Text to Tokens to Embeddings.
- **Architecture**: Deep dive into Transformers, Self-Attention, and Embedding layers.
- **Scaling**: Chinchilla Laws and compute-optimal training science.
- **Economics**: Measuring accuracy, cost, and latency (The Tradeoff Triangle).

### **2. Prompt Engineering & Responsible AI (`/module5_prompt_engineering`)**
Advanced techniques for "programming" LLMs.
- **Prompt Patterns**: Few-shot, Chain-of-Thought, and ReAct patterns.
- **Testing & Versioning**: Systematic evaluation of prompt performance.
- **Guardrails**: Safety and alignment strategies for production.

### **3. Vector Databases & Embeddings (`/module6_vector_databases`)**
Building "External Memory" for LLMs using Retrieval-Augmented Generation (RAG).
- **Similarity Search**: Cosine similarity and Euclidean distance.
- **Vector Stores**: Practical use of Pinecone, FAISS, and ChromaDB.
- **Chunking**: Optimal data preparation for high-quality retrieval.

### **4. Agent Architectures & Tool Calling (`/module7_agents`)**
The shift from "models" to "autonomous systems."
- **ReAct Pattern**: Reasoning before Acting.
- **Tool Integration**: Native function calling with Gemini and GPT-4.
- **Multi-Agent Systems**: Collaborative workflows using AutoGen and CrewAI.

### **5. LinkedIn Research & Lead Generation (`/linkedinresearch`)**
A practical application of LLM agents for high-value sales and outreach.
- **Lead Gen Strategy**: Targeting high-intent signals (Complainer, Competitor, Group Mining).
- **Discovery Execution**: Step-by-step guide to finding "warm" leads.
- **Automation Engine**: A Playwright-powered stealth bot for automated LinkedIn outreach.

### **6. Agent Development Framework (`/azurefactory`)**
A specialized framework for building and deploying production agents.

---

## **🚀 The LinkedIn Lead Generation "3-Step" Workflow**

This module demonstrates a complete end-to-end automation for acquiring customers for portfolio tools.

### **Step 1: Strategy Definition**
Define your target persona and "Discovery Signals."
- **File**: [lead_generation_strategy.md](file:///Users/amolc/2026/llm/linkedinresearch/lead_generation_strategy.md)
- **Key Task**: Identify "complainer" signals (users unhappy with current tools) and competitor audiences.

### **Step 2: Discovery Execution**
Execute manual or semi-automated searches to validate your audience.
- **File**: [discovery_execution_guide.md](file:///Users/amolc/2026/llm/linkedinresearch/discovery_execution_guide.md)
- **Key Task**: Use the provided search strings to find high-intent targets like Prop Traders.

### **Step 3: Automated Outreach**
Use the automation bot to scale your outreach without being flagged.
- **File**: [linkedin_automation.py](file:///Users/amolc/2026/llm/linkedinresearch/linkedin_automation.py)
- **Key Task**: Configure keywords, customize the AI-generated message, and run the bot to collect leads and send connection requests.

---

## **🛠️ Final Sample Program: Bringing It Together**

The "Master Controller" demonstrates how to use LLM intelligence to personalize outreach based on the data collected by the automation bot.

### **How to Run the Final Sample**
1. Ensure your `.env` file has `LINKEDIN_USERNAME`, `LINKEDIN_PASSWORD`, and `GOOGLE_API_KEY`.
2. Install dependencies: `pip install playwright-stealth langchain-google-genai`.
3. Run the automation: `python3 linkedinresearch/linkedin_automation.py` to collect leads in `linkedin_leads.csv`.
4. Run the personalization script: `python3 linkedinresearch/main.py` (see implementation below).

---

*Based on the course: Generative AI Systems.*
