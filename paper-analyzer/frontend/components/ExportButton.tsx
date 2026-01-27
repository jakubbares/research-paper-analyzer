/**
 * Export Button Component - Download analysis results
 */
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Download, Loader2 } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ExportButtonProps {
  paperId: string;
  type: 'contributions' | 'experiments' | 'all';
  label?: string;
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'default' | 'sm' | 'lg';
}

export function ExportButton({ 
  paperId, 
  type, 
  label, 
  variant = 'outline',
  size = 'sm'
}: ExportButtonProps) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format: 'json' | 'csv' | 'markdown') => {
    setIsExporting(true);
    try {
      const endpoint = `${API_URL}/api/papers/${paperId}/export/${type}?format=${format}`;
      const response = await fetch(endpoint);
      
      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Get filename from Content-Disposition header or create one
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `${paperId}_${type}.${format}`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Download the file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const getLabel = () => {
    if (label) return label;
    if (type === 'all') return 'Export All';
    return `Export ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  };

  return (
    <div className="flex gap-2">
      <Button
        variant={variant}
        size={size}
        onClick={() => handleExport('json')}
        disabled={isExporting}
        className="gap-2"
      >
        {isExporting ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Download className="h-4 w-4" />
        )}
        JSON
      </Button>
      <Button
        variant={variant}
        size={size}
        onClick={() => handleExport('csv')}
        disabled={isExporting || type === 'all'}
        className="gap-2"
      >
        CSV
      </Button>
      {type === 'all' && (
        <Button
          variant={variant}
          size={size}
          onClick={() => handleExport('markdown')}
          disabled={isExporting}
          className="gap-2"
        >
          Markdown
        </Button>
      )}
    </div>
  );
}


