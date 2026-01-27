/**
 * Generic Extraction Viewer - Display any extracted data type
 */
'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface GenericViewerProps {
  title: string;
  description: string;
  data: any[];
  cached?: boolean;
}

export function GenericViewer({ title, description, data, cached = false }: GenericViewerProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>No {title.toLowerCase()} found</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>{title}</CardTitle>
              <CardDescription>
                {description} • Found {data.length} items
                {cached && ' (from cache)'}
              </CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.map((item, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardContent className="pt-6">
              <div className="space-y-3">
                {/* Render each field dynamically */}
                {Object.entries(item).map(([key, value]) => {
                  // Skip internal fields
                  if (key.startsWith('_')) return null;
                  
                  // Handle different value types
                  let displayValue: string;
                  if (typeof value === 'object' && value !== null) {
                    displayValue = JSON.stringify(value, null, 2);
                  } else {
                    displayValue = String(value || 'N/A');
                  }

                  // Truncate long values
                  const isTruncated = displayValue.length > 200;
                  const truncatedValue = isTruncated 
                    ? displayValue.substring(0, 200) + '...' 
                    : displayValue;

                  return (
                    <div key={key}>
                      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-sm text-gray-900 whitespace-pre-wrap break-words">
                        {truncatedValue}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}


