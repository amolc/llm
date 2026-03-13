import os
import csv
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv(dotenv_path="/Users/amolc/2026/llm/.env")

# Configuration
BASE_DIR = "/Users/amolc/2026/llm/linkedinresearch"
INPUT_CSV = os.path.join(BASE_DIR, "linkedin_leads.csv")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def generate_personalized_outreach(lead_name, lead_headline):
    """Uses Gemini to generate a highly personalized outreach message."""
    
    if not GOOGLE_API_KEY:
        return f"Hi {lead_name}, I saw you are a {lead_headline}. I'd love to connect!"

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    
    template = """
    You are a professional outreach specialist for a FinTech startup.
    Your goal is to send a short, personalized LinkedIn connection request.
    
    Target Name: {name}
    Target Headline: {headline}
    Product: An AI-powered risk monitoring and auto-trading platform for prop traders.
    Value Prop: Helps avoid accidental drawdown breaches and automates strategy execution.
    
    Constraint: Max 300 characters. Be concise, friendly, and not too salesy.
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    response = await chain.ainvoke({"name": lead_name, "headline": lead_headline})
    content = str(response.content) if response.content else ""
    return content.strip()

async def main():
    print("🚀 Starting Master Controller: Personalized Lead Outreach\n")
    
    # 1. Check if leads exist
    if not os.path.exists(INPUT_CSV):
        print(f"⚠️ No leads found at {INPUT_CSV}.")
        print("💡 Pro-tip: Run 'python3 linkedin_automation.py' first to collect leads.")
        print("--- DEMO MODE ---")
        sample_leads = [
            {"Name": "Pascal Henningsson", "Headline": "Certified funded forex trader at FTMO"},
            {"Name": "Rajkumar Balasubramanian", "Headline": "Prop firm Trader | Quantitative Analyst"}
        ]
    else:
        with open(INPUT_CSV, mode='r', encoding='utf-8') as f:
            sample_leads = list(csv.DictReader(f))[:2] # Process top 2 for demo

    # 2. Process each lead
    for lead in sample_leads:
        name = lead.get("Name", "Trader")
        headline = lead.get("Headline", "Professional")
        
        print(f"🔍 Processing: {name}")
        print(f"   Headline: {headline}")
        
        message = await generate_personalized_outreach(name, headline)
        
        print(f"   ✨ Generated Message: \"{message}\"")
        print("-" * 30)

    print("\n✅ Final Step Complete: Ready for automated engagement.")

if __name__ == "__main__":
    asyncio.run(main())
