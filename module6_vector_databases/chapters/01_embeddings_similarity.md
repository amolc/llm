# Chapter 6.1: Embeddings & Similarity Search

Embeddings are the backbone of modern LLM retrieval systems. They transform unstructured text into dense numerical vectors that capture semantic meaning.

---

## **1. What are Embeddings?**
An embedding is a vector (a list of numbers) that represents a piece of text in a high-dimensional space. 
- **Semantic Proximity**: Similar concepts (e.g., "dog" and "puppy") are mathematically closer in this space than unrelated concepts (e.g., "dog" and "skyscraper").
- **Dimensions**: Common models use 768, 1536, or 3072 dimensions.

---

## **2. Similarity Metrics**
To find relevant information, we calculate the distance between a **Query Vector** and **Document Vectors**.

| Metric | Calculation | Best For |
| :--- | :--- | :--- |
| **Cosine Similarity** | Measures the angle between vectors | Most text-based tasks (ignores magnitude) |
| **Euclidean Distance (L2)** | Measures straight-line distance | When the magnitude of the vector matters |
| **Dot Product** | Sum of products of components | High-performance hardware acceleration |

---

## **3. Sample Code: Cosine Similarity with Numpy**

```python
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Mock embeddings (3D for simplicity)
apple_vector = np.array([0.9, 0.1, 0.05])
iphone_vector = np.array([0.85, 0.15, 0.02])
banana_vector = np.array([0.1, 0.8, 0.01])

sim_apple_iphone = cosine_similarity(apple_vector, iphone_vector)
sim_apple_banana = cosine_similarity(apple_vector, banana_vector)

print(f"Similarity (Apple, iPhone): {sim_apple_iphone:.4f}")
print(f"Similarity (Apple, Banana): {sim_apple_banana:.4f}")
```

---

## **Recommended Reading**
1.  **[What are Vector Embeddings? (Pinecone Guide)](https://www.pinecone.io/learn/vector-embeddings/)**
2.  **[Visualizing Embeddings (TensorFlow Projector)](https://projector.tensorflow.org/)**
