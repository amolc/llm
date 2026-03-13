import os
import json
import csv
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# Load environment variables
load_dotenv()

def create_linkedin_research_system():
    print("--- Initializing LinkedIn Algorithmic Trading Research System ---")
    
    # 1. Setup Gemini LLM and Embeddings
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    Settings.llm = Gemini(
        model="models/gemini-flash-latest",
        api_key=api_key,
        temperature=0.1
    )
    
    Settings.embed_model = GeminiEmbedding(
        model_name="models/gemini-embedding-001",
        api_key=api_key
    )

    # 2. Seed Data (Gathered from Research)
    research_data = [
        {"text": "James Simons, Founder of Renaissance Technologies. Pioneer in quantitative trading and algorithmic strategies. Based in New York.", "source": "Web Research"},
        {"text": "Jeff Yass, Co-founder of Susquehanna International Group (SIG). Expert in options market making and quantitative trading.", "source": "Web Research"},
        {"text": "Stefania Perrucci, Founder and CIO at New Sky Capital. Posts about financial markets, quantitative analysis, and trader psychology on LinkedIn.", "source": "LinkedIn Influencer List"},
        {"text": "Ray Dalio, Founder of Bridgewater Associates. Focuses on macroeconomics and systematic investing principles.", "source": "LinkedIn Influencer List"},
        {"text": "Nassim Nicholas Taleb, Author and Options Trader. Specialist in tail risk and black swan events in algorithmic contexts.", "source": "Web Research"},
        {"text": "Cliff Asness, Founder of AQR Capital Management. Known for factor-based quantitative investing and algorithmic research.", "source": "Industry Leaders"},
        {"text": "Ken Griffin, Founder of Citadel and Citadel Securities. Leading figure in high-frequency and algorithmic market making.", "source": "Industry Leaders"},
        {"text": "David Shaw, Founder of D.E. Shaw & Co. Pioneer in computational finance and algorithmic trading.", "source": "Industry Leaders"},
        {"text": "Edward Thorp, Author of 'Beat the Dealer' and pioneer in quantitative finance. Used algorithms for blackjack and later for the stock market.", "source": "Web Research"},
        {"text": "Howard Marks, Co-founder of Oaktree Capital Management. Focuses on market cycles and distressed debt through systematic approaches.", "source": "LinkedIn Research"},
        {"text": "Aswath Damodaran, Professor at NYU Stern. Specialist in valuation and corporate finance models used in algorithmic trading systems.", "source": "Web Research"},
        {"text": "Renaissance Technologies (Medallion Fund) uses statistical arbitrage and mean reversion strategies extensively. Founded by James Simons.", "source": "Web Research"},
        {"text": "Virtu Financial: Led by Douglas Cifu. Known for electronic execution and high-frequency risk management algorithms.", "source": "Web Research"},
        {"text": "Jump Trading: Global leader in HFT and algorithmic trading, leveraging machine learning and low-latency infrastructure.", "source": "Web Research"},
        {"text": "Hudson River Trading (HRT): Combines quantitative research and high-frequency execution in global markets.", "source": "Web Research"},
        {"text": "Citadel Securities: Top market maker in equities and options using sophisticated algorithmic routing.", "source": "Web Research"},
        {"text": "Jane Street: Excels in options pricing and volatility arbitrage using quantitative and algorithmic decision-making.", "source": "Web Research"}
    ]

    # 3. Create LlamaIndex Documents
    documents = []
    for item in research_data:
        doc = Document(
            text=item["text"],
            metadata={"source": item["source"]}
        )
        documents.append(doc)

    # 4. Indexing
    print("Indexing research data...")
    index = VectorStoreIndex.from_documents(documents)
    # Use a higher similarity top_k to capture all documents for extraction
    query_engine = index.as_query_engine(similarity_top_k=20)

    # 5. Extracting Structured Data for CSV
    print("Extracting contact information...")
    extraction_query = """
    Identify and extract a comprehensive list of ALL individual people and key company leaders mentioned in the provided research data who are associated with algorithmic trading, quantitative finance, or HFT.
    
    For each unique person or leader, provide:
    - Name: Full name of the individual.
    - Role: Their job title or primary role (e.g., Founder, CIO, Professor, Leader).
    - Company: The organization they are associated with (e.g., Renaissance Technologies, Citadel, Jane Street).
    - Expertise: Their primary area of expertise in algorithmic trading (e.g., Statistical Arbitrage, HFT, Market Making, Options Pricing).

    Return the final result strictly as a JSON array of objects.
    Format: [{"Name": "...", "Role": "...", "Company": "...", "Expertise": "..."}]
    """
    
    response = query_engine.query(extraction_query)
    
    # Try to parse the JSON from the response
    try:
        # The LLM might wrap the JSON in code blocks
        content = str(response).strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        contacts = json.loads(content)
        
        # 6. Save to CSV
        csv_file = os.path.join(os.path.dirname(__file__), 'algorithmic_traders_contacts.csv')
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Name", "Role", "Company", "Expertise"])
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
        
        print(f"Successfully created CSV: {csv_file}")
        print(f"Total contacts found: {len(contacts)}")
        
    except Exception as e:
        print(f"Error parsing or saving data: {e}")
        print("Raw response from LLM:")
        print(response)

if __name__ == "__main__":
    create_linkedin_research_system()
