/**
 * Main Home Page - Paper Analyzer with ALL Extraction Types
 */
'use client';

import { useState, useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { PaperUpload } from '@/components/PaperUpload';
import { ContributionGrid } from '@/components/ContributionGrid';
import { ExperimentViewer } from '@/components/ExperimentViewer';
import { GenericViewer } from '@/components/GenericViewer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { paperApi, Paper } from '@/lib/api';
import { FileText, Loader2, AlertCircle, Brain } from 'lucide-react';

// Define all extraction types with their configurations
const EXTRACTION_TYPES = [
  { id: 'contributions', label: 'Contributions', fn: paperApi.extractContributions, useCustomViewer: true },
  { id: 'experiments', label: 'Experiments', fn: paperApi.extractExperiments, useCustomViewer: true },
  { id: 'architectures', label: 'Architectures', fn: paperApi.extractArchitectures },
  { id: 'hyperparameters', label: 'Hyperparameters', fn: paperApi.extractHyperparameters },
  { id: 'ablations', label: 'Ablations', fn: paperApi.extractAblations },
  { id: 'baselines', label: 'Baselines', fn: paperApi.extractBaselines },
  { id: 'equations', label: 'Equations', fn: paperApi.extractEquations },
  { id: 'algorithms', label: 'Algorithms', fn: paperApi.extractAlgorithms },
  { id: 'limitations', label: 'Limitations', fn: paperApi.extractLimitations },
  { id: 'future_work', label: 'Future Work', fn: paperApi.extractFutureWork },
  { id: 'code_resources', label: 'Code/Resources', fn: paperApi.extractCodeResources },
  { id: 'datasets', label: 'Datasets', fn: paperApi.extractDatasets },
  { id: 'loss_functions', label: 'Loss Functions', fn: paperApi.extractLossFunctions },
  { id: 'metrics', label: 'Metrics', fn: paperApi.extractMetrics },
  { id: 'training', label: 'Training', fn: paperApi.extractTraining },
  { id: 'related_work', label: 'Related Work', fn: paperApi.extractRelatedWork },
  { id: 'claims', label: 'Claims', fn: paperApi.extractClaims },
];

export default function Home() {
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [activeTab, setActiveTab] = useState('upload');
  const queryClient = useQueryClient();

  // Load existing papers on mount
  const { data: papersData } = useQuery({
    queryKey: ['papers'],
    queryFn: () => paperApi.listPapers(),
  });

  // Auto-select first paper if available and none selected
  useEffect(() => {
    if (papersData?.papers && papersData.papers.length > 0 && !selectedPaper) {
      setSelectedPaper(papersData.papers[0]);
      setActiveTab('paper');
    }
  }, [papersData, selectedPaper]);

  const handleUploadSuccess = (paper: Paper) => {
    setSelectedPaper(paper);
    setActiveTab('paper');
  };

  const handleExtract = (extractionType: string) => {
    if (selectedPaper) {
      queryClient.invalidateQueries({ queryKey: [extractionType, selectedPaper.paper_id] });
      setActiveTab(extractionType);
    }
  };

  // Generic extraction tab renderer
  const renderExtractionTab = (type: typeof EXTRACTION_TYPES[0]) => {
    const { data, isLoading, error } = useQuery({
      queryKey: [type.id, selectedPaper?.paper_id],
      queryFn: () => type.fn(selectedPaper!.paper_id),
      enabled: !!selectedPaper && activeTab === type.id,
    });

    return (
      <TabsContent key={type.id} value={type.id} className="space-y-6">
        {isLoading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            <span className="ml-3 text-gray-600">Extracting {type.label.toLowerCase()}...</span>
          </div>
        )}

        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-red-600">
                <AlertCircle className="h-5 w-5" />
                <p className="text-sm font-medium">
                  Failed to extract {type.label.toLowerCase()}: {(error as Error).message}
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {data && (
          <>
            {/* Use custom viewer for contributions and experiments */}
            {type.id === 'contributions' && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Contributions</CardTitle>
                    <CardDescription>
                      Found {data.contributions?.length || 0} contributions
                      {data.cached && ' (from cache)'}
                    </CardDescription>
                  </CardHeader>
                </Card>
                <ContributionGrid 
                  contributions={data.contributions || []} 
                  paperId={selectedPaper!.paper_id}
                />
              </>
            )}
            
            {type.id === 'experiments' && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Experiments</CardTitle>
                    <CardDescription>
                      Found {data.experiments?.length || 0} experiments
                      {data.cached && ' (from cache)'}
                    </CardDescription>
                  </CardHeader>
                </Card>
                <ExperimentViewer 
                  experiments={data.experiments || []} 
                  paperId={selectedPaper!.paper_id}
                />
              </>
            )}

            {/* Use generic viewer for all other types */}
            {!type.useCustomViewer && (
              <GenericViewer
                title={type.label}
                description={`Extracted ${type.label.toLowerCase()}`}
                data={data[type.id] || []}
                cached={data.cached}
              />
            )}
          </>
        )}
      </TabsContent>
    );
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <Brain className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Research Paper Analyzer
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Powered by DeepSeek v3 • 17 Extraction Types Available 🚀
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          {/* Tab List - Scrollable for many tabs */}
          <div className="bg-white rounded-lg p-2 shadow-sm overflow-x-auto">
            <TabsList className="inline-flex gap-2 flex-nowrap">
              <TabsTrigger value="upload">Upload</TabsTrigger>
              <TabsTrigger value="paper" disabled={!selectedPaper}>
                Paper Info
              </TabsTrigger>
              {EXTRACTION_TYPES.map(type => (
                <TabsTrigger key={type.id} value={type.id} disabled={!selectedPaper}>
                  {type.label}
                </TabsTrigger>
              ))}
            </TabsList>
          </div>

          {/* Upload Tab */}
          <TabsContent value="upload" className="space-y-6">
            <PaperUpload onUploadSuccess={handleUploadSuccess} />
          </TabsContent>

          {/* Paper Info Tab */}
          <TabsContent value="paper" className="space-y-6">
            {selectedPaper && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      {selectedPaper.title}
                    </CardTitle>
                    <CardDescription>
                      {selectedPaper.authors.join(', ')} • {selectedPaper.num_pages} pages
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-sm mb-2">Abstract</h3>
                      <p className="text-sm text-gray-700 leading-relaxed">
                        {selectedPaper.abstract || 'No abstract available'}
                      </p>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 pt-4">
                      {EXTRACTION_TYPES.map(type => (
                        <Button 
                          key={type.id}
                          onClick={() => handleExtract(type.id)}
                          variant="outline"
                          size="sm"
                          className="text-xs"
                        >
                          {type.label}
                        </Button>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          {/* All Extraction Tabs */}
          {EXTRACTION_TYPES.map(renderExtractionTab)}
        </Tabs>
      </div>
    </main>
  );
}


