# Ink & Insight - Document Authenticity Analyzer

## Project Overview
A comprehensive web application for analyzing document authenticity using advanced image processing, OCR, and deep learning techniques.

## Project Structure

### Frontend (React + TypeScript)

#### Core Files
- `src/App.tsx`
  - Main application component
  - Manages file upload and analysis state
  - Coordinates between components

- `src/types/analysis.ts`
  - TypeScript interfaces for analysis results
  - Defines structure for visual, text, and handwriting analysis data

#### Components
- `src/components/FileUpload.tsx`
  - Handles PDF file upload via drag-and-drop
  - Uses react-dropzone for file handling
  - Validates file types

- `src/components/AnalysisResults.tsx`
  - Displays analysis results in a structured format
  - Shows scores and findings for each analysis type
  - Includes visual indicators for result severity

#### Services
- `src/services/analysisService.ts`
  - Manages communication with backend API
  - Handles document analysis requests
  - Processes analysis responses

### Backend (Python + FastAPI)

#### Core Files
- `backend/src/main.py`
  - FastAPI application setup
  - API endpoint definitions
  - CORS configuration

- `backend/src/config.py`
  - Application configuration settings
  - Environment variables
  - Path configurations

#### Models
- `backend/src/models/analysis.py`
  - Pydantic models for data validation
  - Defines structure for analysis results
  - Type definitions for analysis components

- `backend/src/models/neural_network.py`
  - Deep learning model architecture
  - Siamese network implementation
  - Custom CNN for handwriting analysis

#### Services
- `backend/src/services/document_processor.py`
  - Coordinates analysis pipeline
  - Manages concurrent analysis tasks
  - Combines results from different analyzers

- `backend/src/services/visual_analyzer.py`
  - Handles visual similarity analysis
  - Image segmentation
  - Region-based analysis

- `backend/src/services/text_analyzer.py`
  - OCR text extraction
  - Semantic analysis
  - Text consistency checking

- `backend/src/services/handwriting_analyzer.py`
  - Handwriting style analysis
  - Pressure and spacing detection
  - Anomaly identification

- `backend/src/services/model_trainer.py`
  - Neural network training pipeline
  - Dataset management
  - Model saving and loading

### Configuration Files
- `package.json`
  - Frontend dependencies
  - Project scripts
  - Build configuration

- `tsconfig.json` and related files
  - TypeScript configuration
  - Module resolution settings
  - Compiler options

- `vite.config.ts`
  - Vite build configuration
  - Plugin setup
  - Development server settings

- `tailwind.config.js`
  - Tailwind CSS configuration
  - Theme customization
  - Content paths

- `eslint.config.js`
  - ESLint configuration
  - Code style rules
  - TypeScript integration

### Documentation
- `backend/README.md`
  - Backend setup instructions
  - API documentation
  - Project structure overview

## Technology Stack
- Frontend:
  - React 18
  - TypeScript
  - Tailwind CSS
  - Lucide React (icons)
  - React Dropzone (file upload)

- Backend:
  - FastAPI
  - PyTorch
  - OpenCV
  - Tesseract OCR
  - Transformers
  - SpaCy

## Development Setup
1. Frontend:
   ```bash
   npm install
   npm run dev
   ```

2. Backend:
   ```bash
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```