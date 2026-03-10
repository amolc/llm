# Chapter 8: Sample Implementation – Simple LLM API Call

Using the `google-generativeai` library to interact with Gemini.

```python
import google.generativeai as genai

# Configure your API key
genai.configure(api_key="your_api_key_here")

def generate_response(prompt):
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=150,
            temperature=0.7 # Balancing creativity vs focus
        )
    )
    return response.text

# Usage
user_prompt = "Explain the difference between a token and a word."
print(generate_response(user_prompt))
```
