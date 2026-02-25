import os
from crewai import Agent
from dotenv import load_dotenv
load_dotenv()
MODEL = "openrouter/mistralai/mistral-7b-instruct"

from tools import FinancialDocumentTool
pdf_tool = FinancialDocumentTool()

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents accurately using only the provided data.",
    backstory="You are a professional financial analyst with 20+ years experience. Use only document content; cite pages.",
    tools=[pdf_tool],
    llm=MODEL,
    verbose=True,
    system_prompt="""Analyze financial docs precisely. Compute ratios: Current Ratio (CA/CL>2), ROE (Net Income/Equity>15%), Debt/EBITDA<3.
    Output ONLY valid JSON: {"revenue": "trends/growth", "profitability": "margins/ROE", "cashflow": "operating/investing", "key_risks": ["list"], "summary": "1-para"}"""
)

risk_assessor = Agent(
    role="Financial Risk Assessment Expert",
    goal="Identify risks from financial data.",
    backstory="Expert in liquidity, credit, operational risks from balance sheets/P&Ls.",
    llm=MODEL,
    verbose=True,
    system_prompt="""From prior analysis, identify risks: liquidity shortfalls, high debt, declining margins.
    Output ONLY JSON: {"risks": [{"type": "liquidity", "score": "high/medium/low", "details": "..."}], "mitigations": ["list"]}"""
)

investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Provide evidence-based investment insights.",
    backstory="Balanced advisor using data only; no speculation.",
    llm=MODEL,
    verbose=True,
    system_prompt="""Using financial & risk analyses, recommend: Buy/Hold/Sell with rationale.
    Output JSON: {"recommendation": "Buy/Hold/Sell", "confidence": "high/medium/low", "reasons": ["list"], "target_price": "if applicable"}"""
)
