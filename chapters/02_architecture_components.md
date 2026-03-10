# Chapter 2: Core Architecture Components

The Transformer is the backbone of all modern LLMs. It uses several key components to process text.

## **A. Embeddings**
Embeddings represent words in a "semantic space." Words with similar meanings are closer together in this space.

### **Visualizing Semantic Space**
```text
[ High-Dimensional Space ]
      ^
      |   (Queen) .
      |            .
      |             . (King)
      |
      |   (Woman) .
      |            .
      |             . (Man)
      +---------------------------->
```
*   **Vector Math Example**: `Vector("King") - Vector("Man") + Vector("Woman") ≈ Vector("Queen")`

### **Sample Code: Similarity with Embeddings**
You can use `sentence-transformers` (a popular library for embeddings) to see how semantically similar two sentences are.

```python
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "The cat sits outside", 
    "A man is playing guitar", 
    "The feline is resting in the garden"
]

# Compute embeddings
embeddings = model.encode(sentences)

# Compute cosine similarity between "cat" and "feline" sentences
cosine_score = util.cos_sim(embeddings[0], embeddings[2])

print(f"Similarity between Sentence 1 and Sentence 3: {cosine_score.item():.4f}")
# Expected: High similarity (~0.7+) because 'cat' and 'feline' are semantically related.
```

---

## **B. Self-Attention**
Self-attention allows the model to focus on different parts of the input sequence when processing a specific token.

### **Attention Visualization**
In the sentence: *"The animal didn't cross the street because **it** was too tired."*

| Word | Attention focus of "**it**" |
| :--- | :--- |
| The | Low |
| **animal** | **High (Primary Reference)** |
| cross | Low |
| street | Medium (Context) |
| because | Low |
| it | Self |
| tired | High (Reason) |

### **Sample Code: Simple Self-Attention Mechanism**
This is a simplified conceptual implementation of how attention weights are calculated (Query, Key, Value).

```python
import numpy as np

def scaled_dot_product_attention(query, key, value):
    # Calculate dot product
    matmul_qk = np.matmul(query, key.T)
    
    # Scale by square root of dimension
    d_k = query.shape[-1]
    scaled_attention_logits = matmul_qk / np.sqrt(d_k)
    
    # Apply softmax to get weights (summing to 1)
    attention_weights = np.exp(scaled_attention_logits) / np.sum(np.exp(scaled_attention_logits), axis=-1)
    
    # Multiply by values
    output = np.matmul(attention_weights, value)
    
    return output, attention_weights

# Example usage with dummy vectors
q = np.array([[1, 0, 1]]) # Query for "it"
k = np.array([[1, 0, 1],  # Key for "animal"
              [0, 1, 0]]) # Key for "street"
v = np.array([[10, 0, 0], # Value for "animal"
              [0, 5, 0]]) # Value for "street"

output, weights = scaled_dot_product_attention(q, k, v)
print(f"Attention Weights: {weights}") # "it" focuses more on "animal"
```

---

## **C. Transformer Architecture**
Modern LLMs stack dozens of "Transformer Blocks."

### **The Transformer Block Diagram**
```text
[ Input Tokens ]
      |
[ Multi-Head Attention ] <--- Focus on context
      |
[ Add & Norm ] <------------- Residual Connection
      |
[ Feed Forward Network ] <--- Feature Processing
      |
[ Add & Norm ] <------------- Residual Connection
      |
[ Output to next layer ]
```

---

## **Recommended Reading & Resources**

To deepen your understanding of these foundations, I highly recommend the following articles:

1.  **[The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) by Jay Alammar**
    *   *Why read:* The gold standard for visual explanations of how Transformers, Attention, and Embeddings work.
2.  **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)**
    *   *Why read:* The original research paper that started the GenAI revolution. Essential for technical depth.
3.  **[What are Embeddings?](https://www.cloudflare.com/learning/ai/what-are-embeddings/) by Cloudflare**
    *   *Why read:* A very clear, high-level explanation of how text is turned into math.
4.  **[Transformer Explainer](https://poloclub.github.io/transformer-explainer/) (Interactive Tool)**
    *   *Why use:* A brilliant interactive visualization where you can see the math happening in real-time.

