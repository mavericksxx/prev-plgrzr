import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload } from 'lucide-react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  active?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, active = true }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    disabled: !active
  });

  return (
    <div
      {...getRootProps()}
      className={`p-10 border-2 border-dashed rounded-xl text-center cursor-pointer transition-all
        ${isDragActive ? 'border-orange-400 bg-orange-400/5' : active ? 'border-white/20 hover:border-orange-400/50' : 'border-white/10 bg-white/5 opacity-50 cursor-not-allowed'}
        ${active ? 'hover:bg-white/5' : ''}`}
    >
      <input {...getInputProps()} />
      <Upload className={`w-12 h-12 mx-auto mb-4 ${active ? 'text-white/40' : 'text-white/20'}`} />
      <p className={`text-lg ${active ? 'text-white/60' : 'text-white/20'}`}>
        {isDragActive
          ? 'Drop the PDF here...'
          : active 
            ? 'Drag & drop a PDF file here, or click to select'
            : 'Document uploaded'}
      </p>
      <p className={`mt-2 text-sm ${active ? 'text-white/40' : 'text-white/20'}`}>
        Only PDF files are accepted
      </p>
    </div>
  );
};