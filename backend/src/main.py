from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services.document_processor import DocumentProcessor
from .models.analysis import AnalysisResult

app = FastAPI(title="Document Authenticity Analyzer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_processor = DocumentProcessor()

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_document(file: UploadFile):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    try:
        content = await file.read()
        result = await document_processor.analyze(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))