import React from 'react';
import { AnalysisResult } from '../types/analysis';
import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface AnalysisResultsProps {
  results: AnalysisResult;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  const getScoreColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600';
    if (score >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 0.9) return <CheckCircle className="w-6 h-6 text-green-600" />;
    if (score >= 0.7) return <AlertTriangle className="w-6 h-6 text-yellow-600" />;
    return <XCircle className="w-6 h-6 text-red-600" />;
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Overall Analysis Score</h2>
          <div className="flex items-center gap-2">
            {getScoreIcon(results.overallScore)}
            <span className={`text-2xl font-bold ${getScoreColor(results.overallScore)}`}>
              {(results.overallScore * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Visual Similarity</h3>
            <p className={`text-lg ${getScoreColor(results.visualSimilarity.score)}`}>
              {(results.visualSimilarity.score * 100).toFixed(1)}%
            </p>
            <ul className="mt-2 space-y-1">
              {results.visualSimilarity.segments.map(segment => (
                <li key={segment.id} className="text-sm text-gray-600">
                  {segment.region}: {(segment.similarityScore * 100).toFixed(1)}%
                </li>
              ))}
            </ul>
          </div>

          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Text Analysis</h3>
            <p className={`text-lg ${getScoreColor(results.textAnalysis.score)}`}>
              {(results.textAnalysis.score * 100).toFixed(1)}%
            </p>
            <ul className="mt-2 space-y-1">
              {results.textAnalysis.inconsistencies.map((inc, idx) => (
                <li key={idx} className="text-sm text-gray-600">
                  {inc.description} ({inc.severity})
                </li>
              ))}
            </ul>
          </div>

          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Handwriting Analysis</h3>
            <p className={`text-lg ${getScoreColor(results.handwritingAnalysis.score)}`}>
              {(results.handwritingAnalysis.score * 100).toFixed(1)}%
            </p>
            <ul className="mt-2 space-y-1">
              {results.handwritingAnalysis.anomalies.map((anomaly, idx) => (
                <li key={idx} className="text-sm text-gray-600">
                  {anomaly.description} ({(anomaly.confidence * 100).toFixed(1)}%)
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};