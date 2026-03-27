import React, { useRef, useCallback } from "react";
import Editor, { OnMount } from "@monaco-editor/react";
import { useSandboxStore } from "../../stores/sandboxStore";
import { useSettingsStore } from "../../stores/settingsStore";

interface RefactoredPaneProps {
  onEditorMount?: (editor: any) => void;
}

export const RefactoredPane: React.FC<RefactoredPaneProps> = ({
  onEditorMount,
}) => {
  const { refactoredCode, isRefactoring } = useSandboxStore();
  const { theme } = useSettingsStore();
  const editorRef = useRef<any>(null);

  const handleEditorMount: OnMount = useCallback(
    (editor) => {
      editorRef.current = editor;
      onEditorMount?.(editor);

      editor.updateOptions({
        readOnly: true,
        minimap: { enabled: false },
        fontSize: 13,
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
        scrollBeyondLastLine: false,
        automaticLayout: true,
        padding: { top: 12 },
        wordWrap: "on",
        domReadOnly: true,
      });
    },
    [onEditorMount]
  );

  return (
    <div className="relative h-full flex flex-col">
      <div className="flex items-center justify-between px-4 py-2 border-b border-dark-border bg-dark-surface/50">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/60" />
            <div className="w-3 h-3 rounded-full bg-amber-500/60" />
            <div className="w-3 h-3 rounded-full bg-green-500/60" />
          </div>
          <span className="text-xs text-dark-muted ml-2">refactored.py</span>
        </div>
        {isRefactoring && (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 border-2 border-accent-primary border-t-transparent rounded-full spinner" />
            <span className="text-xs text-accent-primary">Refactoring...</span>
          </div>
        )}
      </div>

      <div className="flex-1 relative">
        {!refactoredCode && !isRefactoring ? (
          <div className="absolute inset-0 flex items-center justify-center text-dark-muted">
            <div className="text-center">
              <svg
                width="40"
                height="40"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                className="mx-auto mb-3 opacity-40"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
              </svg>
              <p className="text-sm">Refactored code will appear here</p>
              <p className="text-xs mt-1 opacity-60">
                Click "Refactor" to generate ttnn-compatible code
              </p>
            </div>
          </div>
        ) : (
          <Editor
            height="100%"
            language="python"
            theme={theme === "dark" ? "vs-dark" : "vs"}
            value={refactoredCode}
            onMount={handleEditorMount}
            options={{
              readOnly: true,
              minimap: { enabled: false },
              fontSize: 13,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              scrollBeyondLastLine: false,
              automaticLayout: true,
              padding: { top: 12 },
              wordWrap: "on",
            }}
          />
        )}
      </div>
    </div>
  );
};
