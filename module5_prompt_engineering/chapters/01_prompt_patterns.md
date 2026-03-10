# Chapter 5.1: Prompt Engineering Patterns

To get consistent results from an LLM, we use established structural patterns. This chapter explores how to design prompts that improve reasoning and accuracy, with a focus on real-world domains like Finance and Security.

---

## **1. Chain-of-Thought (CoT)**
*   **Pattern**: Asking the model to "Think step-by-step" or "Explain your reasoning."
*   **Why**: Forces the model to allocate more compute (tokens) to intermediate reasoning steps, which significantly reduces errors in complex tasks.
*   **Best for**: Financial analysis, logic puzzles, and multi-step planning.

### **💰 Finance Example (Investment Analysis)**:
**Prompt**:
```text
Analyze if Company X is a good short-term investment based on these metrics:
- Cash Flow: $500M (up 20% YoY)
- Debt: $1.2B (up 50% YoY)
- Market Sentiment: Bullish due to new product launch.

Think step-by-step:
1. Evaluate the liquidity position.
2. Compare debt growth to cash flow growth.
3. Consider the impact of market sentiment vs. financial health.
4. Provide a final risk rating (Low, Medium, High).
```

---

## **2. Few-Shot Prompting**
*   **Pattern**: Providing 3-5 examples of input/output pairs within the prompt.
*   **Why**: Models are "In-Context Learners." They learn the desired *format*, *tone*, and *edge-case handling* from examples better than from abstract instructions.

### **💰 Finance Example (Transaction Categorization)**:
**Prompt**:
```text
Categorize the following bank transactions:

Input: "Amazon Web Services - $450.00" | Category: Cloud Infrastructure
Input: "Starbucks Coffee #1234 - $5.50" | Category: Meals & Entertainment
Input: "Regus Office Rental - $2,000.00" | Category: Rent & Utilities
Input: "Delta Airlines Flight 442 - $650.00" | Category: Travel
Input: "Monthly Payroll - $15,000.00" | Category: 
```

---

## **3. System vs. User Role Separation**
*   **Pattern**: Defining a clear "Persona" in the System instructions.
*   **Why**: Sets the "temperature" of the response and constrains the model's domain expertise. A "Financial Auditor" persona will be more critical than a "Creative Writer."

### **💰 Finance Example (Compliance Auditor)**:
**System Prompt**:
```text
"You are a Senior Financial Compliance Auditor at a Global Bank. Your goal is to review transaction logs for signs of 'Structuring' or potential 'Anti-Money Laundering (AML)' red flags. Be highly critical and cite specific financial regulations where possible."
```

**User Prompt**:
```text
"User 882 has made 5 separate cash deposits of $9,900 over the last 3 days. Is this a red flag?"
```

---

## **4. Prompt Chaining**
*   **Pattern**: Breaking a large task into smaller, sequential prompts where the output of one is the input for the next.
*   **Why**: Prevents "lost in the middle" context issues and allows for more granular control over complex workflows.

### **💰 Finance Example (Earnings Call Analysis)**:
1.  **Prompt 1**: "Extract all financial figures from this 50-page earnings transcript."
2.  **Prompt 2**: "Using the figures from Prompt 1, calculate the Gross Margin and Debt-to-Equity ratio."
3.  **Prompt 3**: "Draft a 1-page summary for the CEO highlighting the top 3 financial risks identified."

---

## **Recommended Reading**
1.  **[Prompt Engineering Guide](https://www.promptingguide.ai/)**
2.  **[Chain of Thought Prompting (Original Paper)](https://arxiv.org/abs/2201.11903)**
3.  **[LLM Patterns in Finance (Hugging Face)](https://huggingface.co/blog/finance-llm-guide)**
