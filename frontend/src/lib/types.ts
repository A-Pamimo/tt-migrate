// === Severity & Status ===
export type Severity = "supported" | "partial" | "unsupported";
export type MigrationEffort = "low" | "medium" | "high";

// === Diagnostic (per-line analysis result) ===
export interface Diagnostic {
  line: number;
  column?: number;
  endLine?: number;
  endColumn?: number;
  severity: Severity;
  operation: string;
  message: string;
  suggestion?: string;
  ttnnEquivalent?: string;
  docUrl?: string;
}

// === Analysis Result ===
export interface AnalysisResult {
  score: number; // 0-100 compatibility percentage
  diagnostics: Diagnostic[];
  summary: AnalysisSummary;
  topBlockers: Blocker[];
  migrationEffort: MigrationEffort;
}

export interface AnalysisSummary {
  total: number;
  supported: number;
  partial: number;
  unsupported: number;
}

export interface Blocker {
  operation: string;
  count: number;
  severity: Severity;
  impact: string;
}

// === Refactor Request/Response ===
export interface RefactorRequest {
  code: string;
  diagnostics?: Diagnostic[];
  llmProvider?: string;
}

export interface RefactorStreamEvent {
  type: "chunk" | "done" | "error";
  content?: string;
  error?: string;
}

// === Export ===
export type ExportFormat = "py" | "ipynb" | "report";

export interface ExportRequest {
  originalCode: string;
  refactoredCode: string;
  analysisResult?: AnalysisResult;
  format: ExportFormat;
}

// === API ===
export interface AnalyzeRequest {
  code: string;
}

export interface ApiError {
  detail: string;
  status: number;
}

// === Settings ===
export type LLMProvider = "anthropic" | "openai" | "google";
export type Theme = "dark" | "light";

// === Sample Model ===
export interface SampleModel {
  id: string;
  name: string;
  description: string;
  code: string;
}
