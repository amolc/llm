import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
# This will search for a .env file in the current directory
load_dotenv()

# Load the data from the samples folder
def load_earnings_data():
    samples_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(samples_path, 'tcs_q2.json'), 'r') as f:
        q2_data = json.load(f)
    with open(os.path.join(samples_path, 'tcs_q3.json'), 'r') as f:
        q3_data = json.load(f)
    return q2_data, q3_data

def analyze_earnings():
    # 1. Load the data
    q2, q3 = load_earnings_data()

    # 2. Setup the LLM (Gemini 1.5 Flash for speed and reasoning)
    # The API key is now loaded automatically from .env via load_dotenv()
    # Ensure GOOGLE_API_KEY is defined in your .env file
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0
    )

    # 3. Create a prompt template for comparing the two quarters
    template = """
    You are a Financial Analyst. Analyze the following earnings data for TCS for Q2 and Q3 of FY 2024-25.
    
    Q2 Data: {q2_data}
    Q3 Data: {q3_data}
    
    Please provide a concise comparison and answer the following:
    1. How did the Revenue and Net Profit change between Q2 and Q3?
    2. Which quarter had better margins and what was the difference?
    3. What is the trend in Total Contract Value (TCV)?
    4. Provide a summary insight on the company's performance trajectory.
    
    Format the output clearly with bullet points.
    """
    
    prompt = PromptTemplate(
        input_variables=["q2_data", "q3_data"],
        template=template
    )

    # 4. Use the LCEL (LangChain Expression Language) approach
    chain = prompt | llm
    
    print("--- Analyzing TCS Q2 vs Q3 FY25 Earnings ---")
    response = chain.invoke({
        "q2_data": json.dumps(q2, indent=2),
        "q3_data": json.dumps(q3, indent=2)
    })
    
    # Extract content from the AIMessage response
    print(response.content)

if __name__ == "__main__":
    analyze_earnings()
