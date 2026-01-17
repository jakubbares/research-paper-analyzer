/**
 * Multi-Paper Dashboard - Analyze multiple papers
 */
'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Database, Target, Lightbulb } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface DashboardProps {
  paperIds: string[];
}

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6366f1', '#f43f5e'];

export function MultiPaperDashboard({ paperIds }: DashboardProps) {
  const { data: contributions, isLoading: loadingContributions } = useQuery({
    queryKey: ['analysis', 'contributions', paperIds],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/analysis/contributions?paper_ids=${paperIds.join(',')}`);
      return response.json();
    },
    enabled: paperIds.length > 0,
  });

  const { data: experiments, isLoading: loadingExperiments } = useQuery({
    queryKey: ['analysis', 'experiments', paperIds],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/analysis/experiments?paper_ids=${paperIds.join(',')}`);
      return response.json();
    },
    enabled: paperIds.length > 0,
  });

  const { data: patterns, isLoading: loadingPatterns } = useQuery({
    queryKey: ['analysis', 'patterns', paperIds],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/analysis/patterns?paper_ids=${paperIds.join(',')}`);
      return response.json();
    },
    enabled: paperIds.length > 0,
  });

  const { data: gaps, isLoading: loadingGaps } = useQuery({
    queryKey: ['analysis', 'gaps', paperIds],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/analysis/gaps?paper_ids=${paperIds.join(',')}`);
      return response.json();
    },
    enabled: paperIds.length > 0,
  });

  if (paperIds.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Select multiple papers to see cross-paper analysis</p>
      </div>
    );
  }

  const isLoading = loadingContributions || loadingExperiments || loadingPatterns || loadingGaps;

  if (isLoading) {
    return <div className="text-center py-12">Loading analysis...</div>;
  }

  // Prepare chart data
  const contributionChartData = contributions?.most_common?.map((item: any) => ({
    type: item.type.length > 20 ? item.type.substring(0, 20) + '...' : item.type,
    count: item.count
  })) || [];

  const datasetChartData = experiments?.common_datasets?.slice(0, 10).map((item: any) => ({
    name: item.name,
    value: item.count
  })) || [];

  return (
    <div className="space-y-6">
      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Papers Analyzed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{paperIds.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Contributions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{contributions?.total_contributions || 0}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Experiments</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{experiments?.total_experiments || 0}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Patterns Found</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{patterns?.total_patterns || 0}</div>
          </CardContent>
        </Card>
      </div>

      {/* Contribution Types Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Most Common Contribution Types
          </CardTitle>
          <CardDescription>Frequency of contribution types across papers</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={contributionChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Datasets Pie Chart */}
      {datasetChartData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Most Used Datasets
            </CardTitle>
            <CardDescription>Distribution of dataset usage</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={datasetChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {datasetChartData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Patterns */}
      {patterns?.patterns && patterns.patterns.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Detected Patterns
            </CardTitle>
            <CardDescription>Trends and insights across papers</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {patterns.patterns.map((pattern: any, index: number) => (
              <div key={index} className="p-3 bg-blue-50 rounded-lg">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-semibold text-sm">{pattern.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">{pattern.description}</p>
                  </div>
                  <Badge>{pattern.confidence}</Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Research Gaps */}
      {gaps?.gaps && gaps.gaps.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="h-5 w-5" />
              Research Opportunities
            </CardTitle>
            <CardDescription>Identified gaps and opportunities</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {gaps.gaps.map((gap: any, index: number) => (
              <div key={index} className="p-3 bg-yellow-50 rounded-lg">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-semibold text-sm">{gap.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">{gap.description}</p>
                  </div>
                  <Badge variant="outline">{gap.opportunity}</Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

