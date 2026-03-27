import React, { useState } from "react";
import { useExport } from "../../hooks/useExport";

export const ExportPanel: React.FC = () => {
  const { exportCode, copyToClipboard, isExporting, exportError } = useExport();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await copyToClipboard();
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="panel p-5">
      <h3 className="text-xs font-semibold text-dark-muted uppercase tracking-wider mb-4">
        Export
      </h3>

      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={() => exportCode("py")}
          disabled={isExporting}
          className="btn-secondary flex items-center justify-center gap-2 text-sm"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          .py
        </button>

        <button
          onClick={() => exportCode("ipynb")}
          disabled={isExporting}
          className="btn-secondary flex items-center justify-center gap-2 text-sm"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          .ipynb
        </button>

        <button
          onClick={() => exportCode("report")}
          disabled={isExporting}
          className="btn-secondary flex items-center justify-center gap-2 text-sm"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
          Report
        </button>

        <button
          onClick={handleCopy}
          className="btn-secondary flex items-center justify-center gap-2 text-sm"
        >
          {copied ? (
            <>
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#22c55e"
                strokeWidth="2"
              >
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span className="text-green-400">Copied!</span>
            </>
          ) : (
            <>
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
              </svg>
              Copy
            </>
          )}
        </button>
      </div>

      {isExporting && (
        <div className="mt-3 flex items-center gap-2 text-xs text-dark-muted">
          <div className="w-3 h-3 border-2 border-accent-primary border-t-transparent rounded-full spinner" />
          Exporting...
        </div>
      )}

      {exportError && (
        <p className="mt-3 text-xs text-red-400">{exportError}</p>
      )}
    </div>
  );
};
