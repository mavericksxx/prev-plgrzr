import { AnalysisResult } from '../types/analysis';

export const analyzeDocument = async (original: File, comparison: File): Promise<AnalysisResult> => {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Mock response - replace with actual API call in production
  return {
    visualSimilarity: {
      score: 0.85,
      segments: [
        {
          id: '1',
          region: 'header',
          similarityScore: 0.92
        },
        {
          id: '2',
          region: 'signature',
          similarityScore: 0.78,
          issues: ['Inconsistent pressure points detected']
        }
      ]
    },
    textAnalysis: {
      score: 0.90,
      inconsistencies: [
        {
          location: 'paragraph 2',
          type: 'semantic',
          description: 'Contextual mismatch with surrounding content',
          severity: 'medium'
        }
      ]
    },
    handwritingAnalysis: {
      score: 0.82,
      anomalies: [
        {
          location: 'page 1, bottom',
          type: 'style',
          confidence: 0.89,
          description: 'Writing style variation detected'
        }
      ]
    },
    overallScore: 0.86
  };
};