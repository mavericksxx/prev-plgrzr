import React, { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { AnalysisResults } from './components/AnalysisResults';
import { analyzeDocument } from './services/analysisService';
import { AnalysisResult } from './types/analysis';
import { FileText, Loader2 } from 'lucide-react';

function App() {
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    setAnalyzing(true);
    setError(null);
    try {
      const analysisResults = await analyzeDocument(file);
      setResults(analysisResults);
    } catch (err) {
      setError('Error analyzing document. Please try again.');
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-8">
          <FileText className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Ink & Insight</h1>
        </div>

        {!analyzing && !results && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Upload Document for Analysis</h2>
            <FileUpload onFileSelect={handleFileSelect} />
          </div>
        )}

        {analyzing && (
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <Loader2 className="w-12 h-12 mx-auto mb-4 animate-spin text-blue-600" />
            <p className="text-lg text-gray-600">Analyzing document...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 p-4 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {results && <AnalysisResults results={results} />}
      </div>
    </div>
  );
}

export default App;