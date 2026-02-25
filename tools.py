import os
from crewai.tools import BaseTool
from pydantic import BaseModel, validator
from typing import Type
from langchain_community.document_loaders import PyPDFLoader

class PDFInput(BaseModel):
    path: str
    
    @validator('path')
    def validate_path(cls, v):
        if not os.path.exists(v) or not v.endswith('.pdf'):
            raise ValueError(f"Invalid PDF path: {v}")
        return v

class FinancialDocumentTool(BaseTool):
    name: str = "financial_document_reader"
    description: str = "Use ONLY for actual PDF file paths. Returns full cleaned text."
    args_schema: Type[BaseModel] = PDFInput

    def _run(self, path: str) -> str:
        if not os.path.exists(path):
            return f"ERROR: File not found - {path}"
        loader = PyPDFLoader(path)
        documents = loader.load()
        full_text = ""
        for i, doc in enumerate(documents):
            full_text += f"Page {i}: {doc.page_content.strip()}\n\n"
        return full_text[:15000]
