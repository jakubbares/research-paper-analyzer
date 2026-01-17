/**
 * Paper List Component - View all analyzed papers
 */
'use client';

import { Paper } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Calendar, Users } from 'lucide-react';

interface PaperListProps {
  papers: Paper[];
  onSelectPaper: (paper: Paper) => void;
}

export function PaperList({ papers, onSelectPaper }: PaperListProps) {
  if (papers.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-4 text-lg font-medium text-gray-900">No papers yet</h3>
        <p className="mt-2 text-sm text-gray-500">Upload a paper to get started</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {papers.map((paper) => (
        <Card
          key={paper.paper_id}
          className="cursor-pointer hover:shadow-lg transition-shadow hover:border-blue-500"
          onClick={() => onSelectPaper(paper)}
        >
          <CardHeader>
            <CardTitle className="text-lg line-clamp-2">{paper.title}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-gray-600 line-clamp-3">{paper.abstract}</p>
            
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <Users className="h-3 w-3" />
              <span className="line-clamp-1">
                {paper.authors?.slice(0, 3).join(', ')}
                {paper.authors?.length > 3 && ` +${paper.authors.length - 3} more`}
              </span>
            </div>

            <div className="flex items-center gap-2 text-xs text-gray-500">
              <FileText className="h-3 w-3" />
              <span>{paper.num_pages} pages</span>
            </div>

            <div className="flex flex-wrap gap-1 mt-2">
              <Badge variant="secondary" className="text-xs">
                Ready
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

