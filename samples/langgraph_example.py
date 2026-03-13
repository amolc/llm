import json
import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Define the State of the Graph
class EarningsState(TypedDict):
    q2_data: dict
    q3_data: dict
    comparison_analysis: str
    final_report: str

# Node 1: Load Data
def load_data_node(state: EarningsState):
    samples_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(samples_path, 'tcs_q2.json'), 'r') as f:
        q2 = json.load(f)
    with open(os.path.join(samples_path, 'tcs_q3.json'), 'r') as f:
        q3 = json.load(f)
    return {"q2_data": q2, "q3_data": q3}

# Node 2: Analyze Data
def analyze_node(state: EarningsState):
    # Using Gemini 3 Flash Preview for reasoning
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    You are a Financial Data Analyst. Compare these two quarters for TCS:
    Q2: {q2}
    Q3: {q3}
    
    Please provide a concise comparison and answer the following:
    1. How did the Revenue and Net Profit change between Q2 and Q3?
    2. Which quarter had better margins and what was the difference?
    3. What is the trend in Total Contract Value (TCV)?
    4. Provide a summary insight on the company's performance trajectory.
    
    Format the output clearly with bullet points.
    """)
    
    chain = prompt | llm
    response = chain.invoke({"q2": json.dumps(state["q2_data"]), "q3": json.dumps(state["q3_data"])})
    return {"comparison_analysis": response.content}

# Node 3: Generate Executive Report
def report_node(state: EarningsState):
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    You are a Senior Investment Strategist. Convert the following analysis into a high-level executive report for stakeholders.
    
    Analysis: {analysis}
    
    Format the report with:
    - Executive Summary
    - Key Performance Metrics
    - Strategic Outlook
    """)
    
    chain = prompt | llm
    response = chain.invoke({"analysis": state["comparison_analysis"]})
    return {"final_report": response.content}

# Build the Graph
workflow = StateGraph(EarningsState)

# Add Nodes
workflow.add_node("loader", load_data_node)
workflow.add_node("analyzer", analyze_node)
workflow.add_node("reporter", report_node)

# Add Edges (Linear workflow for this example)
workflow.set_entry_point("loader")
workflow.add_edge("loader", "analyzer")
workflow.add_edge("analyzer", "reporter")
workflow.add_edge("reporter", END)

# Compile
app = workflow.compile()

def run_analysis():
    print("--- Starting LangGraph TCS Earnings Workflow ---")
    # Initial state with required keys to satisfy EarningsState
    inputs: EarningsState = {
        "q2_data": {},
        "q3_data": {},
        "comparison_analysis": "",
        "final_report": ""
    }
    
    for output in app.stream(inputs):
        # output is a dict with node_name: state_updates
        for node_name, state_update in output.items():
            print(f"\n[Node: {node_name} completed]")
            if "final_report" in state_update:
                print("\n--- FINAL EXECUTIVE REPORT ---")
                print(state_update["final_report"])

if __name__ == "__main__":
    run_analysis()
