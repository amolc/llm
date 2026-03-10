# Chapter 6.3: Chunking, Metadata & Hybrid Search

For an LLM to retrieve relevant information, we must prepare our documents by breaking them into manageable, semantically cohesive "chunks."

---

## **1. Strategies for Chunking**

A chunk is a segment of a larger document. 

| Strategy | Impact on Retrieval | Best For |
| :--- | :--- | :--- |
| **Fixed-Size Chunking** | Simple but can break sentences | Fast initial indexing |
| **Recursive Character Chunking** | Respects paragraphs and sentences | Most common text-based RAG |
| **Semantic Chunking** | Uses an LLM to decide on breaks | High-accuracy retrieval |

---

## **2. Metadata Filtering**

A vector index is a black box. **Metadata** allows us to add a layer of structured search (like SQL) on top of a semantic search.

**Example**:
- **Query**: "What were the Q3 profits for Company X?"
- **Metadata**: `{"company": "X", "year": 2023, "quarter": "Q3"}`
- **Action**: Filter by `company` AND `quarter` FIRST, then perform semantic similarity on the remaining chunks.

---

## **3. Hybrid Search**

Combining **Keyword Search (BM25)** and **Semantic Search (Vector)**.
- **BM25**: Good for specific terms (e.g., "iPhone 15 Pro Max").
- **Vector**: Good for conceptual themes (e.g., "high-end smartphone features").
- **Combined**: Uses a weighted score (Reciprocal Rank Fusion - RRF) to get the best of both worlds.

---

## **4. Sample Code: Recursive Chunking**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """
Large Language Models (LLMs) are a type of artificial intelligence. 
They are trained on massive amounts of data to understand and generate human-like text. 
One of the most popular LLMs is GPT-4, developed by OpenAI. 
Another major model is Gemini, developed by Google.
"""

# Define the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # Characters per chunk
    chunk_overlap=20 # Overlap to maintain context
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---\n{chunk}")
```

---

## **Recommended Reading**
1.  **[LangChain: Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)**
2.  **[Hybrid Search with Weaviate](https://weaviate.io/blog/hybrid-search-explained)**
3.  **[Semantic Chunking Guide (LlamaIndex)](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/)**
