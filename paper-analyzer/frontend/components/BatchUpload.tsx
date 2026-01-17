/**
 * Batch Upload Component - Upload multiple papers at once
 */
'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { paperApi, Paper } from '@/lib/api';
import { Upload, CheckCircle, XCircle, Loader2 } from 'lucide-react';

interface UploadStatus {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  paper?: Paper;
  error?: string;
  progress: number;
}

interface BatchUploadProps {
  onComplete?: (papers: Paper[]) => void;
}

export function BatchUpload({ onComplete }: BatchUploadProps) {
  const [files, setFiles] = useState<UploadStatus[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const queryClient = useQueryClient();

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const validFiles = selectedFiles.filter(f => f.name.endsWith('.pdf'));
    
    setFiles(validFiles.map(file => ({
      file,
      status: 'pending',
      progress: 0
    })));
  };

  const uploadFiles = async () => {
    setIsUploading(true);
    const uploadedPapers: Paper[] = [];

    for (let i = 0; i < files.length; i++) {
      const fileStatus = files[i];
      
      // Update status to uploading
      setFiles(prev => prev.map((f, idx) => 
        idx === i ? { ...f, status: 'uploading', progress: 0 } : f
      ));

      try {
        // Upload paper
        const paper = await paperApi.uploadPaper(fileStatus.file);
        uploadedPapers.push(paper);

        // Update status to success
        setFiles(prev => prev.map((f, idx) => 
          idx === i ? { ...f, status: 'success', paper, progress: 100 } : f
        ));
      } catch (error) {
        // Update status to error
        setFiles(prev => prev.map((f, idx) => 
          idx === i ? { 
            ...f, 
            status: 'error', 
            error: error instanceof Error ? error.message : 'Upload failed',
            progress: 0 
          } : f
        ));
      }
    }

    setIsUploading(false);
    queryClient.invalidateQueries({ queryKey: ['papers'] });
    
    if (onComplete && uploadedPapers.length > 0) {
      onComplete(uploadedPapers);
    }
  };

  const totalProgress = files.length > 0
    ? (files.filter(f => f.status === 'success').length / files.length) * 100
    : 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Batch Upload Papers</CardTitle>
        <CardDescription>Upload multiple PDF papers at once for analysis</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100
              cursor-pointer"
            disabled={isUploading}
          />
        </div>

        {files.length > 0 && (
          <>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Overall Progress</span>
                <span>{Math.round(totalProgress)}%</span>
              </div>
              <Progress value={totalProgress} />
            </div>

            <div className="max-h-64 overflow-y-auto space-y-2">
              {files.map((file, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm"
                >
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    {file.status === 'pending' && <Upload className="h-4 w-4 text-gray-400" />}
                    {file.status === 'uploading' && <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />}
                    {file.status === 'success' && <CheckCircle className="h-4 w-4 text-green-500" />}
                    {file.status === 'error' && <XCircle className="h-4 w-4 text-red-500" />}
                    <span className="truncate">{file.file.name}</span>
                  </div>
                  {file.status === 'error' && (
                    <span className="text-xs text-red-600">{file.error}</span>
                  )}
                </div>
              ))}
            </div>

            <Button
              onClick={uploadFiles}
              disabled={isUploading}
              className="w-full"
            >
              {isUploading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload {files.length} Paper{files.length > 1 ? 's' : ''}
                </>
              )}
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  );
}

