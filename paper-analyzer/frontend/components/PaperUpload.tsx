/**
 * Paper Upload Component
 */
'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Upload, Loader2, FileText, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { paperApi, Paper } from '@/lib/api';

interface PaperUploadProps {
  onUploadSuccess?: (paper: Paper) => void;
}

export function PaperUpload({ onUploadSuccess }: PaperUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const uploadMutation = useMutation({
    mutationFn: (file: File) => paperApi.uploadPaper(file),
    onSuccess: (paper) => {
      setSelectedFile(null);
      onUploadSuccess?.(paper);
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      if (e.dataTransfer.files[0].type === 'application/pdf') {
        setSelectedFile(e.dataTransfer.files[0]);
      } else {
        alert('Please upload a PDF file');
      }
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      uploadMutation.mutate(selectedFile);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Research Paper</CardTitle>
        <CardDescription>
          Upload a PDF file to analyze contributions and experiments
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Drag and Drop Zone */}
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {selectedFile ? (
            <div className="space-y-2">
              <FileText className="mx-auto h-12 w-12 text-blue-600" />
              <p className="text-sm font-medium">{selectedFile.name}</p>
              <p className="text-xs text-gray-500">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          ) : (
            <>
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                Drag and drop your PDF here, or click to select
              </p>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <Button
                variant="outline"
                className="mt-4"
                onClick={() => document.getElementById('file-upload')?.click()}
              >
                Select PDF File
              </Button>
            </>
          )}
        </div>

        {/* Upload Button */}
        {selectedFile && (
          <Button
            onClick={handleUpload}
            disabled={uploadMutation.isPending}
            className="w-full"
          >
            {uploadMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Uploading and parsing...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload and Analyze
              </>
            )}
          </Button>
        )}

        {/* Success Message */}
        {uploadMutation.isSuccess && (
          <div className="flex items-center gap-2 text-green-600 bg-green-50 p-3 rounded-lg">
            <CheckCircle2 className="h-5 w-5" />
            <span className="text-sm font-medium">
              Paper uploaded successfully!
            </span>
          </div>
        )}

        {/* Error Message */}
        {uploadMutation.isError && (
          <div className="text-red-600 bg-red-50 p-3 rounded-lg">
            <p className="text-sm font-medium">
              Upload failed: {(uploadMutation.error as Error).message}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

