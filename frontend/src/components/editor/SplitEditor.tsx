import React, { useRef, useCallback } from "react";
import { OriginalPane } from "./OriginalPane";
import { RefactoredPane } from "./RefactoredPane";

export const SplitEditor: React.FC = () => {
  const leftEditorRef = useRef<any>(null);
  const rightEditorRef = useRef<any>(null);
  const isSyncing = useRef(false);

  const syncScroll = useCallback(
    (source: "left" | "right") => {
      if (isSyncing.current) return;
      isSyncing.current = true;

      const sourceEditor =
        source === "left" ? leftEditorRef.current : rightEditorRef.current;
      const targetEditor =
        source === "left" ? rightEditorRef.current : leftEditorRef.current;

      if (sourceEditor && targetEditor) {
        const scrollTop = sourceEditor.getScrollTop();
        targetEditor.setScrollTop(scrollTop);
      }

      requestAnimationFrame(() => {
        isSyncing.current = false;
      });
    },
    []
  );

  const handleLeftMount = useCallback(
    (editor: any) => {
      leftEditorRef.current = editor;
      editor.onDidScrollChange(() => syncScroll("left"));
    },
    [syncScroll]
  );

  const handleRightMount = useCallback(
    (editor: any) => {
      rightEditorRef.current = editor;
      editor.onDidScrollChange(() => syncScroll("right"));
    },
    [syncScroll]
  );

  return (
    <div className="flex h-full rounded-xl overflow-hidden border border-dark-border">
      <div className="flex-1 min-w-0 border-r border-dark-border">
        <OriginalPane onEditorMount={handleLeftMount} />
      </div>
      <div className="flex-1 min-w-0">
        <RefactoredPane onEditorMount={handleRightMount} />
      </div>
    </div>
  );
};
