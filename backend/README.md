# Document Authenticity Analyzer Backend

This is the backend implementation for the Document Authenticity Analyzer system. It provides API endpoints for analyzing PDF documents using various techniques including visual analysis, text extraction, and handwriting analysis.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

3. Start the server:
```bash
uvicorn src.main:app --reload
```

## API Endpoints

- POST `/api/analyze`: Analyze a PDF document
  - Request: multipart/form-data with PDF file
  - Response: Analysis results including visual similarity, text analysis, and handwriting analysis

## Project Structure

```
backend/
├── src/
│   ├── main.py           # FastAPI application and routes
│   ├── config.py         # Configuration settings
│   ├── models/           # Pydantic models
│   │   └── analysis.py   # Data models for analysis results
│   └── services/         # Business logic
│       ├── document_processor.py    # Main processing coordinator
│       ├── visual_analyzer.py       # Visual similarity analysis
│       ├── text_analyzer.py         # Text extraction and analysis
│       └── handwriting_analyzer.py  # Handwriting analysis
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```