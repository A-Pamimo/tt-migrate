import React, { useState, useCallback, useRef } from "react";
import { useSandboxStore } from "../../stores/sandboxStore";
import { useNavigate } from "react-router-dom";

export const DropZone: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { setOriginalCode } = useSandboxStore();
  const navigate = useNavigate();

  const handleFile = useCallback(
    (file: File) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        if (text) {
          setOriginalCode(text);
          navigate("/sandbox");
        }
      };
      reader.readAsText(file);
    },
    [setOriginalCode, navigate]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        handleFile(files[0]);
      }
    },
    [handleFile]
  );

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
      className={`relative cursor-pointer rounded-xl border-2 border-dashed p-12 text-center transition-all duration-300 ${
        isDragging
          ? "border-accent-primary bg-accent-primary/10 drop-zone-active"
          : "border-dark-border hover:border-dark-muted bg-dark-panel/50 hover:bg-dark-panel"
      }`}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".py,.pth,.txt"
        onChange={handleFileInput}
        className="hidden"
      />

      <div className="flex flex-col items-center gap-4">
        <div
          className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-colors ${
            isDragging ? "bg-accent-primary/20" : "bg-dark-surface"
          }`}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            stroke={isDragging ? "#7c3aed" : "#8888aa"}
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
        </div>

        <div>
          <p className="text-lg font-medium text-dark-text">
            {isDragging ? "Drop your file here" : "Drag & drop a Python file"}
          </p>
          <p className="text-sm text-dark-muted mt-1">
            or click to browse &mdash; .py files supported
          </p>
        </div>
      </div>
    </div>
  );
};
