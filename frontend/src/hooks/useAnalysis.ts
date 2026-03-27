import { useCallback } from "react";
import { useSandboxStore } from "../stores/sandboxStore";
import apiClient from "../lib/api";
import { ApiError } from "../lib/types";

export function useAnalysis() {
  const {
    originalCode,
    isAnalyzing,
    analysisResult,
    analysisError,
    setIsAnalyzing,
    setAnalysisResult,
    setAnalysisError,
  } = useSandboxStore();

  const analyze = useCallback(async () => {
    if (!originalCode.trim()) {
      setAnalysisError("No code to analyze");
      return;
    }

    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      const result = await apiClient.analyze(originalCode);
      setAnalysisResult(result);
    } catch (err: unknown) {
      const apiErr = err as ApiError;
      setAnalysisError(apiErr.detail || "Analysis failed. Is the backend running?");
    } finally {
      setIsAnalyzing(false);
    }
  }, [originalCode, setIsAnalyzing, setAnalysisResult, setAnalysisError]);

  return {
    analyze,
    isAnalyzing,
    analysisResult,
    analysisError,
  };
}
