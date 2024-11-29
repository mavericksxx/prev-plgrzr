import React, { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { AnalysisResults } from './components/AnalysisResults';
import { analyzeDocument } from './services/analysisService';
import { AnalysisResult } from './types/analysis';
import { Loader2 } from 'lucide-react';

function App() {
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [files, setFiles] = useState<{
    original: File | null;
    comparison: File | null;
  }>({
    original: null,
    comparison: null
  });

  const handleFileSelect = async (file: File, type: 'original' | 'comparison') => {
    setFiles(prev => ({ ...prev, [type]: file }));
    
    // Only analyze when both files are selected
    if (type === 'comparison' && files.original || type === 'original' && files.comparison) {
      setAnalyzing(true);
      setError(null);
      try {
        const analysisResults = await analyzeDocument(
          type === 'original' ? file : files.original!, 
          type === 'comparison' ? file : files.comparison!
        );
        setResults(analysisResults);
      } catch (err) {
        setError('Error analyzing documents. Please try again.');
        console.error(err);
      } finally {
        setAnalyzing(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-400 to-rose-400 bg-clip-text text-transparent">
            prev-plgrzr
          </h1>
        </div>

        {!analyzing && !results && (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-orange-400">Original Document</h2>
              <FileUpload 
                onFileSelect={(file) => handleFileSelect(file, 'original')}
                active={!files.original}
              />
            </div>

            <div className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-rose-400">Comparison Document</h2>
              <FileUpload 
                onFileSelect={(file) => handleFileSelect(file, 'comparison')}
                active={!files.comparison}
              />
            </div>
          </div>
        )}

        {analyzing && (
          <div className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/10 text-center">
            <Loader2 className="w-12 h-12 mx-auto mb-4 animate-spin text-orange-400" />
            <p className="text-lg text-gray-300">Analyzing documents...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-2xl text-red-400">
            {error}
          </div>
        )}

        {results && <AnalysisResults results={results} />}
      </div>
    </div>
  );
}

export default App;