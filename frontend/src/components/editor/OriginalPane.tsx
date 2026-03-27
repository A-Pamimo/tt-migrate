import React, { useRef, useCallback, useState } from "react";
import Editor, { OnMount } from "@monaco-editor/react";
import { useSandboxStore } from "../../stores/sandboxStore";
import { useSettingsStore } from "../../stores/settingsStore";
import { Diagnostic } from "../../lib/types";
import { TooltipPopover } from "./TooltipPopover";

interface OriginalPaneProps {
  onEditorMount?: (editor: any) => void;
}

export const OriginalPane: React.FC<OriginalPaneProps> = ({ onEditorMount }) => {
  const { originalCode, setOriginalCode, diagnostics } = useSandboxStore();
  const { theme } = useSettingsStore();
  const editorRef = useRef<any>(null);
  const decorationsRef = useRef<any>([]);
  const [activeTooltip, setActiveTooltip] = useState<{
    diagnostic: Diagnostic;
    position: { top: number; left: number };
  } | null>(null);

  const applyDecorations = useCallback(
    (editor: any, diagList: Diagnostic[]) => {
      if (!editor) return;

      const model = editor.getModel();
      if (!model) return;

      const decorations = diagList.map((d) => {
        let className = "";
        let glyphClass = "";

        switch (d.severity) {
          case "unsupported":
            className = "line-error";
            glyphClass = "gutter-marker-error";
            break;
          case "partial":
            className = "line-warning";
            glyphClass = "gutter-marker-warning";
            break;
          case "supported":
            className = "line-success";
            glyphClass = "gutter-marker-success";
            break;
        }

        return {
          range: {
            startLineNumber: d.line,
            startColumn: d.column || 1,
            endLineNumber: d.endLine || d.line,
            endColumn: d.endColumn || model.getLineMaxColumn(d.endLine || d.line),
          },
          options: {
            isWholeLine: true,
            className,
            glyphMarginClassName: glyphClass,
            glyphMarginHoverMessage: {
              value: `**${d.operation}** (${d.severity})\n\n${d.message}${
                d.suggestion ? `\n\n*Suggestion:* ${d.suggestion}` : ""
              }`,
            },
            hoverMessage: {
              value: `**${d.operation}**: ${d.message}`,
            },
          },
        };
      });

      decorationsRef.current = editor.deltaDecorations(
        decorationsRef.current,
        decorations
      );
    },
    []
  );

  const handleEditorMount: OnMount = useCallback(
    (editor, monaco) => {
      editorRef.current = editor;
      onEditorMount?.(editor);

      editor.updateOptions({
        glyphMargin: true,
        lineNumbers: "on",
        minimap: { enabled: false },
        fontSize: 13,
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
        scrollBeyondLastLine: false,
        automaticLayout: true,
        padding: { top: 12 },
        wordWrap: "on",
      });

      // Apply decorations if diagnostics already exist
      if (diagnostics.length > 0) {
        applyDecorations(editor, diagnostics);
      }

      // Handle click on gutter for tooltip
      editor.onMouseDown((e: any) => {
        if (
          e.target.type === 2 || // GLYPH_MARGIN
          e.target.type === 3    // LINE_NUMBERS
        ) {
          const lineNumber = e.target.position?.lineNumber;
          if (lineNumber) {
            const diag = diagnostics.find((d) => d.line === lineNumber);
            if (diag) {
              const rect = (editor.getDomNode() as HTMLElement).getBoundingClientRect();
              setActiveTooltip({
                diagnostic: diag,
                position: {
                  top: e.event.posy,
                  left: Math.min(e.event.posx + 10, rect.right - 340),
                },
              });
            }
          }
        }
      });
    },
    [onEditorMount, diagnostics, applyDecorations]
  );

  // Update decorations when diagnostics change
  React.useEffect(() => {
    if (editorRef.current && diagnostics.length > 0) {
      applyDecorations(editorRef.current, diagnostics);
    } else if (editorRef.current && diagnostics.length === 0) {
      decorationsRef.current = editorRef.current.deltaDecorations(
        decorationsRef.current,
        []
      );
    }
  }, [diagnostics, applyDecorations]);

  return (
    <div className="relative h-full flex flex-col">
      <div className="flex items-center justify-between px-4 py-2 border-b border-dark-border bg-dark-surface/50">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/60" />
            <div className="w-3 h-3 rounded-full bg-amber-500/60" />
            <div className="w-3 h-3 rounded-full bg-green-500/60" />
          </div>
          <span className="text-xs text-dark-muted ml-2">original.py</span>
        </div>
        {diagnostics.length > 0 && (
          <span className="text-xs text-dark-muted">
            {diagnostics.length} diagnostic{diagnostics.length !== 1 ? "s" : ""}
          </span>
        )}
      </div>

      <div className="flex-1">
        <Editor
          height="100%"
          language="python"
          theme={theme === "dark" ? "vs-dark" : "vs"}
          value={originalCode}
          onChange={(value) => setOriginalCode(value || "")}
          onMount={handleEditorMount}
          options={{
            glyphMargin: true,
            minimap: { enabled: false },
            fontSize: 13,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            padding: { top: 12 },
            wordWrap: "on",
          }}
        />
      </div>

      {activeTooltip && (
        <TooltipPopover
          diagnostic={activeTooltip.diagnostic}
          position={activeTooltip.position}
          onClose={() => setActiveTooltip(null)}
        />
      )}
    </div>
  );
};
