/**
 * Experiment Viewer Component
 */
'use client';

import { Experiment } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from './ui/badge';
import { ExportButton } from './ExportButton';

interface ExperimentViewerProps {
  experiments: Experiment[];
  paperId?: string;
}

export function ExperimentViewer({ experiments, paperId }: ExperimentViewerProps) {
  if (experiments.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No experiments extracted yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {paperId && (
        <div className="flex justify-end">
          <ExportButton paperId={paperId} type="experiments" />
        </div>
      )}
      {experiments.map((exp, index) => (
        <Card key={index}>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle>{exp.name}</CardTitle>
                <CardDescription className="mt-2">{exp.description}</CardDescription>
              </div>
              <Badge className="bg-green-100 text-green-800">{exp.task}</Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Datasets */}
            {exp.datasets.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Datasets</h4>
                <div className="space-y-2">
                  {exp.datasets.map((dataset: any, i: number) => (
                    <div key={i} className="text-sm bg-gray-50 p-3 rounded-lg">
                      <p className="font-medium">{dataset.name}</p>
                      {dataset.splits && (
                        <p className="text-xs text-gray-600 mt-1">
                          Train: {dataset.splits.train} | Val: {dataset.splits.val} | Test: {dataset.splits.test}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Baselines */}
            {exp.baselines.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Baselines</h4>
                <div className="flex flex-wrap gap-2">
                  {exp.baselines.map((baseline: any, i: number) => (
                    <Badge key={i} className="bg-blue-100 text-blue-800">
                      {baseline.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Proposed Methods */}
            {exp.proposed_methods.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Proposed Methods</h4>
                <div className="flex flex-wrap gap-2">
                  {exp.proposed_methods.map((method: any, i: number) => (
                    <Badge key={i} className="bg-purple-100 text-purple-800">
                      {method.name} {method.variant && `(${method.variant})`}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Evaluation Metrics */}
            {exp.evaluation_metrics.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Evaluation Metrics</h4>
                <div className="flex flex-wrap gap-2">
                  {exp.evaluation_metrics.map((metric: any, i: number) => (
                    <Badge
                      key={i}
                      className={metric.primary ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'}
                    >
                      {metric.name} {metric.primary && '⭐'}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Results Table */}
            {exp.results.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Results</h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 text-sm">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left font-medium text-gray-700">Method</th>
                        {exp.results[0]?.metrics && Object.keys(exp.results[0].metrics).map((key) => (
                          <th key={key} className="px-4 py-2 text-left font-medium text-gray-700">{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {exp.results.map((result: any, i: number) => (
                        <tr key={i}>
                          <td className="px-4 py-2 font-medium">{result.method}</td>
                          {result.metrics && Object.values(result.metrics).map((value: any, j: number) => (
                            <td key={j} className="px-4 py-2">{value}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Hyperparameters */}
            {Object.keys(exp.hyperparameters).length > 0 && (
              <div>
                <h4 className="font-semibold text-sm mb-2">Hyperparameters</h4>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <pre className="text-xs overflow-x-auto">
                    {JSON.stringify(exp.hyperparameters, null, 2)}
                  </pre>
                </div>
              </div>
            )}

            {/* Evidence Location */}
            {exp.evidence_location && (
              <p className="text-xs text-gray-500">
                📍 {exp.evidence_location}
              </p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

