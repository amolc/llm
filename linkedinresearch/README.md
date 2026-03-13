# LinkedIn Lead Generation Module

This module provides a complete workflow for automated, high-intent lead generation on LinkedIn, specifically tailored for acquiring customers for trading and automation platforms.

---

## **📂 Key Components**

1.  **[lead_generation_strategy.md](file:///Users/amolc/2026/llm/linkedinresearch/lead_generation_strategy.md)**: Defines the strategy, target audience (Prop Traders), and intent signals to look for.
2.  **[discovery_execution_guide.md](file:///Users/amolc/2026/llm/linkedinresearch/discovery_execution_guide.md)**: Provides specific LinkedIn search strings and methods to find leads who are actively looking for solutions.
3.  **[linkedin_automation.py](file:///Users/amolc/2026/llm/linkedinresearch/linkedin_automation.py)**: The automation engine that performs the search, scrolls through results, and collects lead data (names and headlines) into a CSV.
4.  **[main.py](file:///Users/amolc/2026/llm/linkedinresearch/main.py)**: The "Final Sample" that uses LLM intelligence to personalize outreach messages for each lead found by the automation.

---

## **🚀 Step-by-Step Instructions**

Follow these steps to use the system effectively:

### **Step 1: Define Your Strategy**
Open [lead_generation_strategy.md](file:///Users/amolc/2026/llm/linkedinresearch/lead_generation_strategy.md) and review the **Discovery Signals**.
- Identify the "Warm" signals (Complainer, Competitor's Audience).
- Pick a target persona (e.g., the "Challenge Chaser" prop trader).

### **Step 2: Find Your Targets**
Use the [discovery_execution_guide.md](file:///Users/amolc/2026/llm/linkedinresearch/discovery_execution_guide.md) to perform initial searches.
- Copy the provided Boolean search strings into your LinkedIn search bar.
- Verify that the results match your ideal customer profile.

### **Step 3: Automated Collection & Outreach**
Run the [linkedin_automation.py](file:///Users/amolc/2026/llm/linkedinresearch/linkedin_automation.py) script.
- It will automatically log in, search for the keywords, and save the leads to `linkedin_leads.csv`.
- **Note**: Ensure your `.env` file has `LINKEDIN_USERNAME` and `LINKEDIN_PASSWORD`.

### **Step 4: AI Personalization (The Final Step)**
Run the [main.py](file:///Users/amolc/2026/llm/linkedinresearch/main.py) script.
- This script reads the `linkedin_leads.csv` and uses Gemini to craft a 1:1 personalized message based on the lead's specific headline.
- This ensures your outreach doesn't look like generic spam.

---

## **🛠️ Setup & Requirements**

- **Python Environment**: `python3 -m venv venv && source venv/bin/activate`
- **Install Dependencies**: 
  ```bash
  pip install playwright-stealth langchain-google-genai python-dotenv
  playwright install chromium
  ```
- **Credentials**: Create a `.env` file in the root with:
  ```env
  LINKEDIN_USERNAME=your_email@example.com
  LINKEDIN_PASSWORD=your_password
  GOOGLE_API_KEY=your_gemini_api_key
  ```

---

*Based on the course: Generative AI Systems.*
