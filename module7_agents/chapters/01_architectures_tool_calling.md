# Chapter 7.1: Agent Architectures & Tool Calling

Agents represent the evolution from "static models" to "autonomous reasoners." An agent uses an LLM as its central brain to decide which actions to take to achieve a goal.

---

## **1. The ReAct Pattern (Reason + Act)**
The most foundational agent architecture. The agent follows a loop:
1.  **Thought**: "I need to find the current stock price of Apple."
2.  **Action**: `get_stock_price("AAPL")`
3.  **Observation**: "$185.92"
4.  **Thought**: "I have the price. Now I can answer the user."

---

## **2. Native Tool Calling (Function Calling)**
Modern models like Gemini 1.5 Pro have **Native Tool Calling** capabilities. Instead of the LLM just writing text, it outputs structured JSON that your code can execute.

### **The Flow:**
1.  **Define Tools**: Provide a list of functions with descriptions.
2.  **Prompt**: "Check the weather in Mumbai."
3.  **Model Output**: `{ "function": "get_weather", "args": {"location": "Mumbai"} }`
4.  **Execute**: Run the function and send the result back to the LLM.

---

## **3. Sample Code: Native Tool Calling with Gemini**

```python
import google.generativeai as genai

# 1. Define a tool (a simple Python function)
def get_current_weather(location: str):
    """Returns the weather for a given location."""
    # Mock data
    if "mumbai" in location.lower():
        return "Hot and humid, 32°C"
    return "22°C and sunny"

# 2. Configure the model with the tool
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[get_current_weather]
)

# 3. Start a chat and ask a question
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message("What is the weather like in Mumbai today?")

print(f"Agent Thought/Response: {response.text}")
```

---

## **Recommended Reading**
1.  **[ReAct: Synergizing Reasoning and Acting in LLMs](https://arxiv.org/abs/2210.03629)**
2.  **[Google Gemini Tool Calling Documentation](https://ai.google.dev/gemini-api/docs/function-calling)**
