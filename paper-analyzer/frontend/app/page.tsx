/**
 * Main Home Page - Focused Dynamic Visualization with Multi-Paper Support
 */
'use client';

import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { paperApi, Paper } from '@/lib/api';
import { Loader2, Sparkles, Upload, FileText, ChevronDown, ChevronUp, X, Plus } from 'lucide-react';

// Complex example queries for research paper analysis
const EXAMPLE_QUERIES = [
  // Contribution analysis
  "Create a visual taxonomy of all contributions grouped by type (theoretical, methodological, empirical) with interconnections",
  "Show me a hierarchical breakdown of the main contribution and all supporting sub-contributions",
  "Generate a novelty map showing what's new vs what builds on prior work",
  
  // Experimental analysis
  "Build a comprehensive experiment matrix: datasets × methods × metrics with all reported results",
  "Create a comparison table of all baselines vs proposed method with percentage improvements",
  "Visualize the experimental pipeline from data preprocessing to final evaluation",
  
  // Architecture & Methods
  "Draw a detailed architecture diagram showing all components and their data flow",
  "Create a module dependency graph showing how different parts of the system interact",
  "Generate a visual diff showing how this architecture differs from standard approaches",
  
  // Cross-paper analysis (multi-paper)
  "Compare methodologies across all papers and identify common patterns and unique approaches",
  "Create a literature evolution timeline showing how ideas progressed across papers",
  "Build a unified benchmark comparison table across all papers with normalized metrics",
  
  // Deep dive queries
  "Extract all hyperparameters and create an ablation study summary visualization",
  "Map all claims to their supporting evidence with strength indicators",
  "Generate a limitations and future work roadmap with research opportunity scores",
  "Create a reproducibility checklist based on what's documented vs what's missing",
];

export default function Home() {
  const [query, setQuery] = useState('');
  const [generatedHtml, setGeneratedHtml] = useState<string | null>(null);
  const [showRawData, setShowRawData] = useState(false);
  const [rawData, setRawData] = useState<any>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [papers, setPapers] = useState<Paper[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Papers are only loaded when user uploads them - no auto-loading

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: (file: File) => paperApi.uploadPaper(file),
    onSuccess: (paper) => {
      setPapers(prev => [...prev, paper]);
    }
  });

  // Generate visualization mutation
  const generateMutation = useMutation({
    mutationFn: async () => {
      if (!query.trim() || papers.length === 0) {
        throw new Error('Please enter a query and upload at least one paper');
      }
      const paperIds = papers.map(p => p.paper_id);
      const result = await paperApi.generateVisualization(paperIds, query);
      return result;
    },
    onSuccess: (data) => {
      setGeneratedHtml(data.html);
      fetchRawData();
    }
  });

  const fetchRawData = async () => {
    if (papers.length === 0) return;
    try {
      const allData: any = {};
      for (const paper of papers.slice(0, 3)) { // Limit to first 3 for raw data display
        const contributions = await paperApi.extractContributions(paper.paper_id);
        allData[paper.title] = {
          contributions: contributions.contributions?.slice(0, 5) // First 5 contributions
        };
      }
      setRawData(allData);
    } catch (e) {
      // Silently fail
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    files.forEach(file => {
      if (file.type === 'application/pdf') {
        uploadMutation.mutate(file);
      }
    });
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    files.forEach(file => {
      uploadMutation.mutate(file);
    });
  };

  const removePaper = (paperId: string) => {
    setPapers(prev => prev.filter(p => p.paper_id !== paperId));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      generateMutation.mutate();
    }
  };

  // Resize iframe
  useEffect(() => {
    if (iframeRef.current && generatedHtml) {
      const iframe = iframeRef.current;
      iframe.onload = () => {
        try {
          const height = iframe.contentWindow?.document.body.scrollHeight;
          if (height && height > 100) {
            iframe.style.height = `${Math.min(height + 50, 2000)}px`;
          }
        } catch (e) {}
      };
    }
  }, [generatedHtml]);

  // Main input screen
  if (!generatedHtml) {
    return (
      <main className="min-h-screen bg-[#0a0a0f] relative overflow-hidden">
        {/* Animated gradient background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-purple-600/30 via-transparent to-transparent rounded-full blur-3xl animate-pulse" />
          <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-blue-600/20 via-transparent to-transparent rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-transparent rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4">
          <div className="w-full max-w-3xl space-y-8">
            {/* Header */}
            <div className="text-center space-y-3">
              <div className="flex items-center justify-center gap-3 mb-4">
                <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl">
                  <Sparkles className="h-8 w-8 text-white" />
                </div>
              </div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
                Paper Visualizer
              </h1>
              <p className="text-gray-400 text-lg">
                Upload papers, ask complex questions, get custom visualizations
              </p>
            </div>

            {/* Papers area */}
            <div className="space-y-3">
              {/* Uploaded papers */}
              {papers.length > 0 && (
                <div className="space-y-2">
                  {papers.map((paper) => (
                    <div
                      key={paper.paper_id}
                      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl p-3 flex items-center justify-between group hover:bg-white/10 transition-all"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="p-2 bg-purple-500/20 rounded-lg">
                          <FileText className="h-5 w-5 text-purple-400" />
                        </div>
                        <div className="min-w-0">
                          <p className="text-white font-medium truncate">{paper.title}</p>
                          <p className="text-gray-500 text-sm">{paper.num_pages} pages</p>
                        </div>
                      </div>
                      <button
                        onClick={() => removePaper(paper.paper_id)}
                        className="text-gray-500 hover:text-red-400 p-2 opacity-0 group-hover:opacity-100 transition-all"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Add more papers button / Upload area */}
              <div
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`
                  border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all
                  ${isDragging 
                    ? 'border-purple-400 bg-purple-500/20' 
                    : 'border-gray-700 hover:border-purple-500/50 hover:bg-white/5'
                  }
                  ${papers.length > 0 ? 'py-4' : 'py-12'}
                `}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf"
                  multiple
                  onChange={handleFileSelect}
                  className="hidden"
                />
                {uploadMutation.isPending ? (
                  <div className="flex items-center justify-center gap-3">
                    <Loader2 className="h-5 w-5 text-purple-400 animate-spin" />
                    <p className="text-gray-300">Processing PDF...</p>
                  </div>
                ) : papers.length > 0 ? (
                  <div className="flex items-center justify-center gap-2 text-gray-400 hover:text-purple-400">
                    <Plus className="h-5 w-5" />
                    <span>Add more papers</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-3">
                    <Upload className="h-10 w-10 text-gray-600" />
                    <p className="text-gray-300">Drop PDFs here or click to upload</p>
                    <p className="text-gray-600 text-sm">Support for multiple papers</p>
                  </div>
                )}
              </div>
            </div>

            {/* Query Input */}
            <div className="space-y-4">
              <div className="relative">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Describe the visualization you want..."
                  disabled={papers.length === 0}
                  rows={2}
                  className={`
                    w-full px-5 py-4 rounded-2xl text-lg bg-white/5 backdrop-blur-xl border border-white/10
                    text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50
                    resize-none
                    ${papers.length === 0 ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                />
              </div>

              {/* Generate Button */}
              <button
                onClick={() => generateMutation.mutate()}
                disabled={!query.trim() || papers.length === 0 || generateMutation.isPending}
                className={`
                  w-full py-4 rounded-2xl text-lg font-semibold flex items-center justify-center gap-2 transition-all
                  ${!query.trim() || papers.length === 0 || generateMutation.isPending
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white shadow-lg shadow-purple-500/25'
                  }
                `}
              >
                {generateMutation.isPending ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating visualization...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5" />
                    Generate Visualization
                  </>
                )}
              </button>
            </div>

            {/* Error */}
            {generateMutation.isError && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-center text-sm">
                {(generateMutation.error as Error).message}
              </div>
            )}

            {/* Example Queries */}
            <div className="space-y-4 pt-4">
              <div className="flex items-center gap-2 text-gray-500 text-sm">
                <Sparkles className="h-4 w-4" />
                <span>Try these complex queries</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {EXAMPLE_QUERIES.map((example, i) => (
                  <button
                    key={i}
                    onClick={() => setQuery(example)}
                    disabled={papers.length === 0}
                    className="text-left px-4 py-3 rounded-xl text-sm bg-white/5 border border-white/5 text-gray-400 hover:bg-white/10 hover:border-purple-500/30 hover:text-gray-200 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>

            {/* Paper count indicator */}
            {papers.length > 1 && (
              <div className="text-center text-sm text-purple-400">
                Analyzing {papers.length} papers together
              </div>
            )}
          </div>
        </div>
      </main>
    );
  }

  // Generated visualization view
  return (
    <main className="min-h-screen bg-[#0a0a0f]">
      {/* Header */}
      <header className="bg-black/50 backdrop-blur-xl border-b border-white/10 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <span className="text-white font-semibold">Paper Visualizer</span>
            <span className="text-gray-500 text-sm">• {papers.length} paper{papers.length > 1 ? 's' : ''}</span>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-gray-500 text-sm max-w-md truncate hidden md:block">
              "{query.slice(0, 50)}{query.length > 50 ? '...' : ''}"
            </div>
            
            <button
              onClick={() => {
                setGeneratedHtml(null);
                setQuery('');
              }}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-sm font-medium flex items-center gap-2"
            >
              <Sparkles className="h-4 w-4" />
              New Query
            </button>
          </div>
        </div>
      </header>

      {/* Visualization */}
      <div className="max-w-7xl mx-auto p-4">
        {/* Verify Data Toggle */}
        <div className="mb-4">
          <button
            onClick={() => setShowRawData(!showRawData)}
            className="flex items-center gap-2 text-gray-500 hover:text-gray-300 text-sm transition-colors"
          >
            {showRawData ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            {showRawData ? 'Hide' : 'Show'} raw extracted data (verify accuracy)
          </button>
          
          {showRawData && rawData && (
            <div className="mt-3 bg-black/50 border border-white/10 rounded-xl p-4 max-h-64 overflow-auto">
              <pre className="text-xs text-gray-400 whitespace-pre-wrap font-mono">
                {JSON.stringify(rawData, null, 2)}
              </pre>
            </div>
          )}
        </div>

        {/* Generated HTML */}
        <div className="bg-white rounded-2xl overflow-hidden shadow-2xl shadow-purple-500/10">
          <iframe
            ref={iframeRef}
            srcDoc={generatedHtml}
            className="w-full min-h-[700px] border-0"
            sandbox="allow-scripts allow-same-origin"
            title="Generated Visualization"
          />
        </div>
      </div>
    </main>
  );
}
