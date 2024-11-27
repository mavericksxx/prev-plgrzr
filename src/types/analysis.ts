export interface AnalysisResult {
  visualSimilarity: {
    score: number;
    segments: SegmentAnalysis[];
  };
  textAnalysis: {
    score: number;
    inconsistencies: TextInconsistency[];
  };
  handwritingAnalysis: {
    score: number;
    anomalies: HandwritingAnomaly[];
  };
  overallScore: number;
}

export interface SegmentAnalysis {
  id: string;
  region: string;
  similarityScore: number;
  issues?: string[];
}

export interface TextInconsistency {
  location: string;
  type: 'semantic' | 'structural' | 'linguistic';
  description: string;
  severity: 'low' | 'medium' | 'high';
}

export interface HandwritingAnomaly {
  location: string;
  type: 'style' | 'pressure' | 'spacing';
  confidence: number;
  description: string;
}