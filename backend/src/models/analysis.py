from pydantic import BaseModel
from typing import List, Literal

class SegmentAnalysis(BaseModel):
    id: str
    region: str
    similarity_score: float
    issues: List[str] = []

class TextInconsistency(BaseModel):
    location: str
    type: Literal["semantic", "structural", "linguistic"]
    description: str
    severity: Literal["low", "medium", "high"]

class HandwritingAnomaly(BaseModel):
    location: str
    type: Literal["style", "pressure", "spacing"]
    confidence: float
    description: str

class VisualSimilarity(BaseModel):
    score: float
    segments: List[SegmentAnalysis]

class TextAnalysis(BaseModel):
    score: float
    inconsistencies: List[TextInconsistency]

class HandwritingAnalysis(BaseModel):
    score: float
    anomalies: List[HandwritingAnomaly]

class AnalysisResult(BaseModel):
    visual_similarity: VisualSimilarity
    text_analysis: TextAnalysis
    handwriting_analysis: HandwritingAnalysis
    overall_score: float