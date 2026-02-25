import os
import uuid
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from crewai import Crew, Process, Task
import uvicorn

# Lazy imports - only when needed
def get_agents():
    from agents import financial_analyst, risk_assessor, investment_advisor, pdf_tool
    return financial_analyst, risk_assessor, investment_advisor, pdf_tool

def get_tasks():
    from task import create_financial_analysis_task, create_risk_assessment_task, create_investment_task
    return create_financial_analysis_task, create_risk_assessment_task, create_investment_task

app = FastAPI(title="Financial Document Analyzer")
def run_crew(query: str, file_path: str):
    # Get agents FIRST - THIS WAS MISSING!
    financial_analyst, risk_assessor, investment_advisor, pdf_tool = get_agents()
    
    # Extract document FIRST, before creating tasks
    document_text = pdf_tool._run(file_path)
    
    # Create clean tasks (no document text)
    create_financial_task, create_risk_task, create_investment_task = get_tasks()
    financial_task = create_financial_task(query)
    risk_task = create_risk_task(financial_task)
    investment_task = create_investment_task(financial_task, risk_task)
    
    # Pass document via crew inputs
    crew = Crew(
        agents=[financial_analyst, risk_assessor, investment_advisor],
        tasks=[financial_task, risk_task, investment_task],
        process=Process.sequential,
        verbose=True,
        inputs={"document": document_text}  # Available to all tasks
    )
    
    result = crew.kickoff(inputs={"query": query, "document": document_text})
    return {
        "financial": str(financial_task.output.raw) if hasattr(financial_task, 'output') else "N/A",
        "risks": str(risk_task.output.raw) if hasattr(risk_task, 'output') else "N/A", 
        "investment": str(investment_task.output.raw) if hasattr(investment_task, 'output') else "N/A",
        "final": str(result)
    }

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_api(file: UploadFile = File(...), query: str = Form("Comprehensive financial analysis")):
    os.makedirs("uploads", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}.pdf"

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        response = run_crew(query=query, file_path=file_path)
        return {"status": "success", "analysis": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
