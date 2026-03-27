import { useCallback, useState } from "react";
import { useSandboxStore } from "../stores/sandboxStore";
import apiClient from "../lib/api";
import { ExportFormat, ApiError } from "../lib/types";

export function useExport() {
  const { originalCode, refactoredCode, analysisResult } = useSandboxStore();
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

  const downloadFile = useCallback((blob: Blob, filename: string) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, []);

  const exportCode = useCallback(
    async (format: ExportFormat) => {
      if (!refactoredCode && !originalCode) {
        setExportError("No code to export");
        return;
      }

      setIsExporting(true);
      setExportError(null);

      try {
        const blob = await apiClient.exportCode({
          originalCode,
          refactoredCode,
          analysisResult: analysisResult || undefined,
          format,
        });

        const extensions: Record<ExportFormat, string> = {
          py: "migrated_model.py",
          ipynb: "migrated_model.ipynb",
          report: "migration_report.md",
        };

        downloadFile(blob, extensions[format]);
      } catch (err: unknown) {
        const apiErr = err as ApiError;
        setExportError(apiErr.detail || "Export failed");
      } finally {
        setIsExporting(false);
      }
    },
    [originalCode, refactoredCode, analysisResult, downloadFile]
  );

  const copyToClipboard = useCallback(async () => {
    const code = refactoredCode || originalCode;
    if (!code) return;

    try {
      await navigator.clipboard.writeText(code);
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement("textarea");
      textarea.value = code;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
    }
  }, [originalCode, refactoredCode]);

  return {
    exportCode,
    copyToClipboard,
    isExporting,
    exportError,
  };
}
