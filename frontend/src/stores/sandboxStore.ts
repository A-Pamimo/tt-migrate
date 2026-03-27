import { create } from "zustand";
import { AnalysisResult, Diagnostic } from "../lib/types";

interface SandboxState {
  originalCode: string;
  refactoredCode: string;
  diagnostics: Diagnostic[];
  analysisResult: AnalysisResult | null;
  isAnalyzing: boolean;
  isRefactoring: boolean;
  analysisError: string | null;
  refactorError: string | null;

  setOriginalCode: (code: string) => void;
  setRefactoredCode: (code: string) => void;
  appendRefactoredCode: (chunk: string) => void;
  setDiagnostics: (diagnostics: Diagnostic[]) => void;
  setAnalysisResult: (result: AnalysisResult) => void;
  setIsAnalyzing: (isAnalyzing: boolean) => void;
  setIsRefactoring: (isRefactoring: boolean) => void;
  setAnalysisError: (error: string | null) => void;
  setRefactorError: (error: string | null) => void;
  reset: () => void;
  resetRefactored: () => void;
}

const initialState = {
  originalCode: "",
  refactoredCode: "",
  diagnostics: [],
  analysisResult: null,
  isAnalyzing: false,
  isRefactoring: false,
  analysisError: null,
  refactorError: null,
};

export const useSandboxStore = create<SandboxState>((set) => ({
  ...initialState,

  setOriginalCode: (code) => set({ originalCode: code }),
  setRefactoredCode: (code) => set({ refactoredCode: code }),
  appendRefactoredCode: (chunk) =>
    set((state) => ({ refactoredCode: state.refactoredCode + chunk })),
  setDiagnostics: (diagnostics) => set({ diagnostics }),
  setAnalysisResult: (result) =>
    set({ analysisResult: result, diagnostics: result.diagnostics }),
  setIsAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
  setIsRefactoring: (isRefactoring) => set({ isRefactoring }),
  setAnalysisError: (error) => set({ analysisError: error }),
  setRefactorError: (error) => set({ refactorError: error }),
  reset: () => set(initialState),
  resetRefactored: () => set({ refactoredCode: "", refactorError: null }),
}));
