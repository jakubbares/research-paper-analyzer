/**
 * Contribution Grid Component
 */
'use client';

import { Contribution } from '@/lib/api';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from './ui/badge';
import { ExportButton } from './ExportButton';

interface ContributionGridProps {
  contributions: Contribution[];
  paperId?: string;
}

export function ContributionGrid({ contributions, paperId }: ContributionGridProps) {
  const getCategoryColor = (type: string) => {
    const colors: Record<string, string> = {
      'Novel Architecture': 'bg-blue-100 text-blue-800',
      'Novel Loss Function': 'bg-purple-100 text-purple-800',
      'Training/Optimization Procedure': 'bg-green-100 text-green-800',
      'Data Augmentation Strategy': 'bg-yellow-100 text-yellow-800',
      'Evaluation Metric': 'bg-red-100 text-red-800',
      'New Dataset': 'bg-pink-100 text-pink-800',
      'Novel Algorithm': 'bg-indigo-100 text-indigo-800',
      'Attention Mechanism': 'bg-cyan-100 text-cyan-800',
      'Pre-training Strategy': 'bg-orange-100 text-orange-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  if (contributions.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No contributions extracted yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {paperId && (
        <div className="flex justify-end">
          <ExportButton paperId={paperId} type="contributions" />
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {contributions.map((contrib, index) => (
        <Card key={index} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <Badge className={getCategoryColor(contrib.contribution_type)}>
                  {contrib.contribution_type}
                </Badge>
              </div>
            </div>
            <CardTitle className="text-lg mt-2">
              {contrib.specific_innovation}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div>
              <p className="text-sm font-medium text-gray-700">Problem Addressed:</p>
              <p className="text-sm text-gray-600">{contrib.problem_addressed}</p>
            </div>
            {contrib.comment && (
              <div>
                <p className="text-sm font-medium text-gray-700">Note:</p>
                <p className="text-sm text-gray-600 italic">{contrib.comment}</p>
              </div>
            )}
          </CardContent>
          <CardFooter>
            <p className="text-xs text-gray-500">
              📍 {contrib.evidence_location}
            </p>
          </CardFooter>
        </Card>
      ))}
      </div>
    </div>
  );
}

