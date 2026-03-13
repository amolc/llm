import os
import json
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# 1. Load environment variables
load_dotenv()

def run_llamaindex_analysis():
    print("--- Starting LlamaIndex TCS Earnings Analysis ---")
    
    # 2. Configure Gemini LLM and Embeddings
    # Using gemini-2.0-flash as it's stable and widely available
    api_key = os.getenv("GOOGLE_API_KEY")
    
    Settings.llm = Gemini(
        model="models/gemini-flash-latest",
        api_key=api_key,
        temperature=0.1
    )
    
    Settings.embed_model = GeminiEmbedding(
        model_name="models/gemini-embedding-001",
        api_key=api_key
    )

    # 3. Load JSON data and convert to LlamaIndex Documents
    samples_path = os.path.dirname(os.path.abspath(__file__))
    
    documents = []
    for filename in ['tcs_q2.json', 'tcs_q3.json']:
        file_path = os.path.join(samples_path, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Create a document for each quarter with metadata
            doc_text = f"TCS Earnings Data for {data['quarter']} {data['financial_year']}:\n"
            doc_text += json.dumps(data, indent=2)
            
            doc = Document(
                text=doc_text,
                metadata={
                    "quarter": data['quarter'],
                    "financial_year": data['financial_year'],
                    "company": "TCS"
                }
            )
            documents.append(doc)

    # 4. Create Index and Query Engine
    print("Indexing documents...")
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(similarity_top_k=2)

    # 5. Perform Queries
    queries = [
        "How did the Revenue and Net Profit change between Q2 and Q3?",
        "Which quarter had better margins and what was the difference?",
        "What is the trend in Total Contract Value (TCV)?",
        "Provide a summary insight on the company's performance trajectory."
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        response = query_engine.query(query)
        print(f"Answer: {response}")

if __name__ == "__main__":
    run_llamaindex_analysis()
