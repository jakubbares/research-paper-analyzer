/**
 * DynamicViewer - Renders LLM-generated HTML visualizations
 * 
 * Takes a user query and paper IDs, sends to backend which generates
 * custom HTML visualization on-the-fly using the LLM.
 */
'use client';

import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, Sparkles, AlertCircle, Maximize2, Minimize2, RefreshCw } from 'lucide-react';
import { paperApi } from '@/lib/api';

interface DynamicViewerProps {
  paperIds: string[];
  paperTitles?: Record<string, string>;
}

export function DynamicViewer({ paperIds, paperTitles = {} }: DynamicViewerProps) {
  const [query, setQuery] = useState('');
  const [generatedHtml, setGeneratedHtml] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Example queries for inspiration
  const exampleQueries = [
    "Show all contributions grouped by type",
    "Compare experiments across papers in a table",
    "List all baselines and their performance",
    "Show architecture diagrams and descriptions",
    "Summarize limitations and future work",
    "Create a matrix of datasets vs methods",
  ];

  const generateMutation = useMutation({
    mutationFn: async () => {
      if (!query.trim()) {
        throw new Error('Please enter a query');
      }
      return paperApi.generateVisualization(paperIds, query);
    },
    onSuccess: (data) => {
      setGeneratedHtml(data.html);
    }
  });

  // Handle iframe resize based on content - NO HEIGHT LIMIT!
  useEffect(() => {
    if (iframeRef.current && generatedHtml) {
      const iframe = iframeRef.current;
      iframe.onload = () => {
        try {
          const height = iframe.contentWindow?.document.body.scrollHeight;
          if (height && height > 100) {
            // NO LIMIT! Let it be as massive as it needs!
            iframe.style.height = `${height + 100}px`;
          }
        } catch (e) {
          // Fallback to large default
          iframe.style.height = '3000px';
        }
      };
    }
  }, [generatedHtml]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      generateMutation.mutate();
    }
  };

  if (paperIds.length === 0) {
    return (
      <Card className="border-yellow-200 bg-yellow-50">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 text-yellow-700">
            <AlertCircle className="h-5 w-5" />
            <p className="text-sm font-medium">
              No papers selected. Upload and select papers to generate visualizations.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Query Input Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            Dynamic Visualization Generator
          </CardTitle>
          <CardDescription>
            Describe what you want to see — the AI will generate a custom visualization.
            Analyzing {paperIds.length} paper{paperIds.length > 1 ? 's' : ''}.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Query Input */}
          <div className="flex gap-3">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g., Show all contributions grouped by type with paper titles..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={generateMutation.isPending}
            />
            <Button
              onClick={() => generateMutation.mutate()}
              disabled={generateMutation.isPending || !query.trim()}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6"
            >
              {generateMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4 mr-2" />
                  Generate
                </>
              )}
            </Button>
          </div>

          {/* Example Queries */}
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-gray-500 py-1">Try:</span>
            {exampleQueries.map((eq, i) => (
              <button
                key={i}
                onClick={() => setQuery(eq)}
                className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-purple-100 hover:text-purple-700 transition-colors"
              >
                {eq}
              </button>
            ))}
          </div>

          {/* Selected Papers */}
          {Object.keys(paperTitles).length > 0 && (
            <div className="text-xs text-gray-500 border-t pt-3 mt-2">
              <span className="font-medium">Papers: </span>
              {Object.values(paperTitles).slice(0, 5).join(', ')}
              {Object.keys(paperTitles).length > 5 && ` +${Object.keys(paperTitles).length - 5} more`}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Error Display */}
      {generateMutation.isError && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 text-red-600">
              <AlertCircle className="h-5 w-5" />
              <p className="text-sm font-medium">
                Generation failed: {(generateMutation.error as Error).message}
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Generated Visualization */}
      {generatedHtml && (
        <Card className={isFullscreen ? 'fixed inset-4 z-50 overflow-auto' : ''}>
          <CardHeader className="flex flex-row items-center justify-between py-3 px-4 border-b">
            <div>
              <CardTitle className="text-sm font-medium">Generated Visualization</CardTitle>
              <CardDescription className="text-xs">
                Query: "{query}"
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => generateMutation.mutate()}
                disabled={generateMutation.isPending}
              >
                <RefreshCw className={`h-4 w-4 ${generateMutation.isPending ? 'animate-spin' : ''}`} />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsFullscreen(!isFullscreen)}
              >
                {isFullscreen ? (
                  <Minimize2 className="h-4 w-4" />
                ) : (
                  <Maximize2 className="h-4 w-4" />
                )}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {/* Sandboxed iframe for safe HTML rendering - MASSIVE SIZE SUPPORT! */}
            <iframe
              ref={iframeRef}
              srcDoc={generatedHtml}
              className="w-full min-h-[1000px] border-0"
              sandbox="allow-scripts allow-same-origin"
              title="Generated Visualization"
              style={{ minHeight: '1000px' }}
            />
          </CardContent>
        </Card>
      )}

      {/* Loading Overlay */}
      {generateMutation.isPending && (
        <Card>
          <CardContent className="py-12">
            <div className="flex flex-col items-center justify-center gap-4">
              <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
              <div className="text-center">
                <p className="text-sm font-medium text-gray-700">Generating visualization...</p>
                <p className="text-xs text-gray-500 mt-1">
                  The AI is analyzing {paperIds.length} paper{paperIds.length > 1 ? 's' : ''} and creating a custom view
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

