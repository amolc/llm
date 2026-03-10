# Module 1: Foundations of LLM Systems – Learning Guide

Welcome to the **Foundations of Large Language Model (LLM) Systems**. This module is designed to take you from the conceptual basics of how an LLM processes text to the practical engineering decisions required for production-grade AI applications.

Whether you are a developer, a student, or an AI enthusiast, this guide provides a structured pathway to understanding the "magic" behind models like Gemini, GPT-4, and Llama. Each chapter includes deep-dive explanations, visual diagrams (ASCII), hands-on Python code samples, and curated reference articles for further study.

---

## **📚 Course Roadmap**

Explore the chapters below in sequence for the best learning experience:

1.  **[Chapter 1: LLM Workflow – From Prompt to Prediction](./chapters/01_llm_workflow.md)**
    *   The Pipeline: Text → Tokens → Embeddings → Transformer → Prediction.
    *   *Includes: Tokenization code with Gemini and tiktoken.*

2.  **[Chapter 2: Core Architecture Components](./chapters/02_architecture_components.md)**
    *   Deep dive into Embeddings, Self-Attention, and Transformer layers.
    *   *Includes: Self-attention and Embedding code samples.*

3.  **[Chapter 3: Model Scaling & Chinchilla Laws](./chapters/03_scaling_laws.md)**
    *   The science of scaling: Parameters, Data, and Compute.
    *   *Includes: Compute-optimal training calculator.*

4.  **[Chapter 4: Model Types – Open vs. Closed & SLM vs. LLM](./chapters/04_model_types.md)**
    *   Choosing between proprietary (Gemini) and open-source (Llama) models.
    *   *Includes: Small Language Model (SLM) reasoning demonstration.*

5.  **[Chapter 5: Benchmarking and Evaluation](./chapters/05_benchmarking.md)**
    *   How to measure model "intelligence" (MMLU, GSM8K, HumanEval).
    *   *Includes: Custom evaluation script for user test cases.*

6.  **[Chapter 6: Operational Considerations – Cost & Latency](./chapters/06_cost_latency.md)**
    *   The economics of AI: Token pricing, TTFT, and TPS.
    *   *Includes: Real-time latency and cost measurement script.*

7.  **[Chapter 7: The AI Tradeoff Triangle](./chapters/07_tradeoff_triangle.md)**
    *   The engineering balance between Accuracy, Cost, and Latency.
    *   *Includes: A smart model router implementation.*

8.  **[Chapter 8: Sample Implementation – Simple LLM API Call](./chapters/08_api_implementation.md)**
    *   Putting it all together: A production-ready Python SDK sample.

9.  **[Module 5: Prompt Engineering, Testing & Responsible AI](./promptengg.md)**
    *   Prompt patterns, Versioning, and Safety Guardrails.

---

## **🛠️ How to Use This Guide**

- **Read sequentially**: The chapters are built on top of each other.
- **Run the code**: Each chapter contains a `Sample Code` section. Ensure you have your Google AI API Key ready to test the Gemini integrations.
- **Check references**: Each chapter ends with curated links to the most influential research papers and technical blogs in the field.

---

*Based on the course: Generative AI Systems.*
