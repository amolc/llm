# Chapter 6.2: Vector DBs (FAISS, Pinecone, Weaviate)

A **Vector Database** is a specialized storage system designed to index and query millions of high-dimensional vectors in milliseconds.

---

## **1. The Vector DB Architecture**

Unlike traditional SQL databases that use B-trees for indexing, Vector DBs use **Approximate Nearest Neighbor (ANN)** algorithms.

```text
[ Document ] --> [ Embedding Model ] --> [ Vector Index ]
      ^                                          |
      |                                          v
[ Metadata ] <--- [ Similarity Search ] <--- [ Query Vector ]
```

---

## **2. Popular Vector DBs Compared**

| Database | Architecture | Best For |
| :--- | :--- | :--- |
| **FAISS (Facebook)** | Local, in-memory | Research, fast local prototyping |
| **Pinecone** | Managed Cloud, Serverless | Production SaaS, low-maintenance |
| **Weaviate** | Self-hosted or Cloud, Hybrid | Rich metadata filtering and multi-modal |
| **ChromaDB** | Local, Open-source | Simple developer-first experience |

---

## **3. Sample Code: Fast Local Search with FAISS**

```python
import numpy as np
import faiss

# 1. Generate dummy data (5 documents, each 128D)
d = 128
n_docs = 5
xb = np.random.random((n_docs, d)).astype('float32')

# 2. Build the Index (FlatL2 = exact search)
index = faiss.IndexFlatL2(d)
index.add(xb) # Add document vectors to the database

# 3. Query the index
xq = np.random.random((1, d)).astype('float32')
k = 2 # Find the 2 most similar documents
distances, indices = index.search(xq, k)

print(f"Nearest indices: {indices}")
print(f"Distances: {distances}")
```

---

## **Recommended Reading**
1.  **[FAISS: A Library for Efficient Similarity Search](https://engineering.fb.com/2017/03/29/ml-applications/faiss-a-library-for-efficient-similarity-search/)**
2.  **[Pinecone: The Vector Database for Generative AI](https://www.pinecone.io/)**
3.  **[Weaviate: Open-source Vector Database](https://weaviate.io/)**
