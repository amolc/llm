# Chapter 5.1: Prompt Engineering Patterns

To get consistent results from an LLM, we use established structural patterns. This chapter explores how to design prompts that improve reasoning and accuracy.

---

## **1. Chain-of-Thought (CoT)**
*   **Pattern**: Asking the model to "Think step-by-step."
*   **Why**: Forces the model to allocate more compute (tokens) to reasoning before reaching a conclusion.
*   **Best for**: Math, logic, and multi-step planning.

### **Example Prompt**:
```text
Solve the following math problem. Think step-by-step:
A farmer has 15 apples. He sells 5, then buys 2 more. How many does he have?
```

---

## **2. Few-Shot Prompting**
*   **Pattern**: Providing 3-5 examples of input/output pairs within the prompt.
*   **Why**: Models learn the desired *format* and *tone* from examples better than from instructions alone.

### **Example Prompt**:
```text
Classify the sentiment of the following reviews:
Review: "The product is amazing!" | Sentiment: Positive
Review: "It broke after one day." | Sentiment: Negative
Review: "It's okay, could be better." | Sentiment: Neutral
Review: "Best purchase ever!" | Sentiment:
```

---

## **3. System vs. User Role Separation**
*   **Pattern**: Defining a clear "Persona" in the System instructions.
*   **Why**: Sets the constraints and domain expertise of the model.

### **Example System Prompt**:
```text
"You are a senior Python security auditor. Your goal is to find vulnerabilities in the provided code and suggest fixes."
```

---

## **Recommended Reading**
1.  **[Prompt Engineering Guide](https://www.promptingguide.ai/)**
2.  **[Chain of Thought Prompting (Original Paper)](https://arxiv.org/abs/2201.11903)**
