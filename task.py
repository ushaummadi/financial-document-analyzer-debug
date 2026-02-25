from crewai import Task
from agents import financial_analyst, risk_assessor, investment_advisor

def create_financial_analysis_task(query: str = "Comprehensive analysis") -> Task:
    return Task(
        description=f"""
        USER QUERY: {query}

        The full financial document has been pre-processed and is available.
        Your job: Extract and analyze key financial metrics from the document.

        REQUIRED ANALYSIS:
        1. Revenue trends (YoY/QoQ % changes) - Page 4
        2. Profitability (gross/net margins, EBITDA margin) - Page 4  
        3. Cash flow (operating cash, FCF) - Page 4
        4. Ratios (estimate Current Ratio, Debt/EBITDA from cash/income) 
        5. Balance sheet (cash position $36.8B) - Page 4
        6. Risks (declining deliveries, inventory 24 days)

        Output structured analysis with specific numbers from document.
        """,
        expected_output="Structured JSON financial analysis report.",
        agent=financial_analyst
    )

def create_risk_assessment_task(financial_task) -> Task:
    return Task(
        description="Review financial analysis. Identify risks: liquidity, leverage, margins, cash flow. Score severity.",
        expected_output="JSON risks list.",
        agent=risk_assessor,
        context=[financial_task]
    )

def create_investment_task(financial_task, risk_task) -> Task:
    return Task(
        description="Based on financials + risks, recommend BUY/HOLD/SELL.",
        expected_output="JSON investment recommendation.",
        agent=investment_advisor,
        context=[financial_task, risk_task]
    )
