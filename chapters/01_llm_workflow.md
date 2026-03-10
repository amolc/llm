# Chapter 1: LLM Workflow – From Prompt to Prediction

Every time you interact with an LLM, the system follows a specific pipeline to process your request and generate a response.

## **The Pipeline**
1.  **Text Input**: The user sends a natural language prompt.
2.  **Tokenization**: The text is broken into smaller units called "tokens."
3.  **Embeddings**: Tokens are converted into high-dimensional vectors (numbers) representing semantic meaning.
4.  **Transformer Layers**: The model uses "self-attention" to understand the relationship between tokens.
5.  **Next Token Prediction**: The model calculates the probability of the next token and generates it.

---

## **Sample Code: Understanding Tokenization**
Modern LLMs use methods like Byte-Pair Encoding (BPE). Here are examples of how to handle tokenization for both Gemini and OpenAI models.

### **1. Token Counting with Gemini**
Gemini uses its own internal tokenizer. You can count tokens using the `google-generativeai` library.

```python
import google.generativeai as genai

# Configure your API key
genai.configure(api_key="your_api_key_here")

# Initialize a Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

text = "Generative AI is transforming software engineering."

# Count tokens in the text
response = model.count_tokens(text)
print(f"Total tokens for Gemini: {response.total_tokens}")
```

### **2. Detailed Tokenization with OpenAI (tiktoken)**
OpenAI uses the `tiktoken` library, which is highly efficient and allows you to see the exact token IDs and decode them back into strings. This is useful for understanding how text is actually represented.

```python
import tiktoken

# Initialize the encoder for GPT-4
encoding = tiktoken.encoding_for_model("gpt-4")

text = "Generative AI is transforming software engineering."

# Convert text to token IDs
tokens = encoding.encode(text)
print(f"Token IDs: {tokens}")

# Convert token IDs back to strings (to see the split)
decoded_tokens = [encoding.decode_single_token_bytes(token).decode('utf-8') for token in tokens]
print(f"Decoded Tokens: {decoded_tokens}")

# Total count
print(f"Total tokens for GPT-4: {len(tokens)}")
```
