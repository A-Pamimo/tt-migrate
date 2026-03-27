import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { SplitEditor } from "../components/editor/SplitEditor";
import { CompatibilityScore } from "../components/dashboard/CompatibilityScore";
import { SeverityBreakdown } from "../components/dashboard/SeverityBreakdown";
import { TopBlockers } from "../components/dashboard/TopBlockers";
import { MigrationEffort } from "../components/dashboard/MigrationEffort";
import { ExportPanel } from "../components/export/ExportPanel";
import { useSandboxStore } from "../stores/sandboxStore";
import { useAnalysis } from "../hooks/useAnalysis";
import { useRefactor } from "../hooks/useRefactor";

export const SandboxPage: React.FC = () => {
  const navigate = useNavigate();
  const {
    originalCode,
    analysisResult,
    analysisError,
    refactorError,
    isAnalyzing,
    isRefactoring,
  } = useSandboxStore();
  const { analyze } = useAnalysis();
  const { refactor } = useRefactor();

  // Redirect to landing if no code loaded
  useEffect(() => {
    if (!originalCode.trim()) {
      navigate("/");
    }
  }, [originalCode, navigate]);

  if (!originalCode.trim()) return null;

  return (
    <div className="flex flex-col lg:flex-row gap-4 p-4 max-w-[1800px] mx-auto h-[calc(100vh-7.5rem)]">
      {/* Main Editor Area */}
      <div className="flex-1 flex flex-col min-w-0 min-h-0">
        {/* Toolbar */}
        <div className="flex items-center justify-between mb-3 flex-shrink-0">
          <div className="flex items-center gap-2">
            <button onClick={() => navigate("/")} className="btn-secondary text-sm">
              <span className="flex items-center gap-1.5">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <line x1="19" y1="12" x2="5" y2="12" />
                  <polyline points="12 19 5 12 12 5" />
                </svg>
                Back
              </span>
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={analyze}
              disabled={isAnalyzing || !originalCode.trim()}
              className="btn-primary text-sm flex items-center gap-2"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full spinner" />
                  Analyzing...
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
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  Analyze
                </>
              )}
            </button>

            <button
              onClick={refactor}
              disabled={isRefactoring || !originalCode.trim()}
              className="btn-primary text-sm flex items-center gap-2 bg-accent-blue hover:bg-blue-600"
            >
              {isRefactoring ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full spinner" />
                  Refactoring...
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
                    <polyline points="16 18 22 12 16 6" />
                    <polyline points="8 6 2 12 8 18" />
                  </svg>
                  Refactor
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Messages */}
        {analysisError && (
          <div className="mb-3 px-4 py-2.5 bg-red-900/20 border border-red-800/50 rounded-lg text-sm text-red-400 flex items-center gap-2 flex-shrink-0">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            {analysisError}
          </div>
        )}

        {refactorError && (
          <div className="mb-3 px-4 py-2.5 bg-red-900/20 border border-red-800/50 rounded-lg text-sm text-red-400 flex items-center gap-2 flex-shrink-0">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            {refactorError}
          </div>
        )}

        {/* Editor */}
        <div className="flex-1 min-h-0">
          <SplitEditor />
        </div>
      </div>

      {/* Right Sidebar - Dashboard */}
      <div className="w-full lg:w-80 flex-shrink-0 space-y-4 overflow-y-auto scrollbar-thin">
        {analysisResult ? (
          <>
            <CompatibilityScore score={analysisResult.score} />
            <SeverityBreakdown summary={analysisResult.summary} />
            <TopBlockers blockers={analysisResult.topBlockers} />
            <MigrationEffort effort={analysisResult.migrationEffort} />
            <ExportPanel />
          </>
        ) : (
          <div className="panel p-8 text-center">
            <svg
              width="40"
              height="40"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              className="mx-auto mb-3 text-dark-muted opacity-40"
            >
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            <p className="text-sm text-dark-muted">
              Click <strong>Analyze</strong> to check your model's
              compatibility with ttnn.
            </p>
            <p className="text-xs text-dark-muted mt-2 opacity-60">
              Diagnostics, scores, and migration suggestions will appear here.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
