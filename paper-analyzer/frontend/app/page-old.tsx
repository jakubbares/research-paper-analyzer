/**
 * Main Home Page - Paper Analyzer
 */
'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { PaperUpload } from '@/components/PaperUpload';
import { ContributionGrid } from '@/components/ContributionGrid';
import { ExperimentViewer } from '@/components/ExperimentViewer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { paperApi, Paper, Contribution, Experiment } from '@/lib/api';
import { FileText, Loader2, AlertCircle, Brain, FlaskConical } from 'lucide-react';

export default function Home() {
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [activeTab, setActiveTab] = useState('upload');
  const queryClient = useQueryClient();

  // Fetch contributions
  const {
    data: contributionsData,
    isLoading: contributionsLoading,
    error: contributionsError,
  } = useQuery({
    queryKey: ['contributions', selectedPaper?.paper_id],
    queryFn: () => paperApi.extractContributions(selectedPaper!.paper_id),
    enabled: !!selectedPaper && activeTab === 'contributions',
  });

  // Fetch experiments
  const {
    data: experimentsData,
    isLoading: experimentsLoading,
    error: experimentsError,
  } = useQuery({
    queryKey: ['experiments', selectedPaper?.paper_id],
    queryFn: () => paperApi.extractExperiments(selectedPaper!.paper_id),
    enabled: !!selectedPaper && activeTab === 'experiments',
  });

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
    // 🔥 AUTOMATICALLY START EXTRACTING CONTRIBUTIONS!
    setActiveTab('contributions');
  };

  const handleExtractContributions = () => {
    if (selectedPaper) {
      queryClient.invalidateQueries({ queryKey: ['contributions', selectedPaper.paper_id] });
      setActiveTab('contributions');
    }
  };

  const handleExtractExperiments = () => {
    if (selectedPaper) {
      queryClient.invalidateQueries({ queryKey: ['experiments', selectedPaper.paper_id] });
      setActiveTab('experiments');
    }
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
                Powered by Meta Llama 3.3 70B via AWS Bedrock • Auto-extracts on upload 🚀
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-grid">
            <TabsTrigger value="upload">Upload</TabsTrigger>
            <TabsTrigger value="paper" disabled={!selectedPaper}>
              Paper Info
            </TabsTrigger>
            <TabsTrigger value="contributions" disabled={!selectedPaper}>
              Contributions
            </TabsTrigger>
            <TabsTrigger value="experiments" disabled={!selectedPaper}>
              Experiments
            </TabsTrigger>
          </TabsList>

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

                    <div className="flex flex-wrap gap-3 pt-4">
                      <Button onClick={handleExtractContributions} className="flex items-center gap-2">
                        <Brain className="h-4 w-4" />
                        Extract Contributions
                      </Button>
                      <Button onClick={handleExtractExperiments} variant="outline" className="flex items-center gap-2">
                        <FlaskConical className="h-4 w-4" />
                        Extract Experiments
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          {/* Contributions Tab */}
          <TabsContent value="contributions" className="space-y-6">
            {contributionsLoading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                <span className="ml-3 text-gray-600">Extracting contributions...</span>
              </div>
            )}

            {contributionsError && (
              <Card className="border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center gap-2 text-red-600">
                    <AlertCircle className="h-5 w-5" />
                    <p className="text-sm font-medium">
                      Failed to extract contributions: {(contributionsError as Error).message}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {contributionsData && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Contributions</CardTitle>
                    <CardDescription>
                      Found {contributionsData.contributions.length} technical contributions
                      {contributionsData.cached && ' (from cache)'}
                    </CardDescription>
                  </CardHeader>
                </Card>
                <ContributionGrid 
                  contributions={contributionsData.contributions} 
                  paperId={selectedPaper.paper_id}
                />
              </>
            )}
          </TabsContent>

          {/* Experiments Tab */}
          <TabsContent value="experiments" className="space-y-6">
            {experimentsLoading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                <span className="ml-3 text-gray-600">Extracting experiments...</span>
              </div>
            )}

            {experimentsError && (
              <Card className="border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center gap-2 text-red-600">
                    <AlertCircle className="h-5 w-5" />
                    <p className="text-sm font-medium">
                      Failed to extract experiments: {(experimentsError as Error).message}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {experimentsData && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Experiments</CardTitle>
                    <CardDescription>
                      Found {experimentsData.experiments.length} experiments
                      {experimentsData.cached && ' (from cache)'}
                    </CardDescription>
                  </CardHeader>
                </Card>
                <ExperimentViewer 
                  experiments={experimentsData.experiments} 
                  paperId={selectedPaper.paper_id}
                />
              </>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
