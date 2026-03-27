import { useCallback } from "react";
import { useSandboxStore } from "../stores/sandboxStore";
import { useSettingsStore } from "../stores/settingsStore";
import apiClient from "../lib/api";

export function useRefactor() {
  const {
    originalCode,
    diagnostics,
    isRefactoring,
    refactoredCode,
    refactorError,
    setIsRefactoring,
    setRefactoredCode,
    appendRefactoredCode,
    setRefactorError,
    resetRefactored,
  } = useSandboxStore();

  const { llmProvider } = useSettingsStore();

  const refactor = useCallback(async () => {
    if (!originalCode.trim()) {
      setRefactorError("No code to refactor");
      return;
    }

    setIsRefactoring(true);
    setRefactorError(null);
    resetRefactored();

    try {
      await apiClient.refactorStream(
        {
          code: originalCode,
          diagnostics,
          llmProvider,
        },
        (chunk) => {
          appendRefactoredCode(chunk);
        },
        () => {
          setIsRefactoring(false);
        },
        (error) => {
          setRefactorError(error);
          setIsRefactoring(false);
        }
      );
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Refactoring failed";
      setRefactorError(message);
      setIsRefactoring(false);
    }
  }, [
    originalCode,
    diagnostics,
    llmProvider,
    setIsRefactoring,
    setRefactorError,
    resetRefactored,
    appendRefactoredCode,
  ]);

  return {
    refactor,
    isRefactoring,
    refactoredCode,
    refactorError,
  };
}
