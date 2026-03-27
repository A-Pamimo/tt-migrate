import React from "react";
import { Diagnostic } from "../../lib/types";
import { SEVERITY_COLORS, SEVERITY_LABELS } from "../../lib/constants";

interface TooltipPopoverProps {
  diagnostic: Diagnostic;
  position: { top: number; left: number };
  onClose: () => void;
}

export const TooltipPopover: React.FC<TooltipPopoverProps> = ({
  diagnostic,
  position,
  onClose,
}) => {
  const colors = SEVERITY_COLORS[diagnostic.severity];

  return (
    <>
      <div className="fixed inset-0 z-40" onClick={onClose} />
      <div
        className="fixed z-50 w-80 bg-dark-panel border border-dark-border rounded-xl shadow-2xl p-4 space-y-2"
        style={{ top: position.top, left: position.left }}
      >
        <div className="flex items-center justify-between">
          <span
            className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium ${colors.bg} ${colors.text} border ${colors.border}`}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${colors.dot}`} />
            {SEVERITY_LABELS[diagnostic.severity]}
          </span>
          <button
            onClick={onClose}
            className="text-dark-muted hover:text-dark-text"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <div>
          <p className="text-sm font-medium text-dark-text">
            {diagnostic.operation}
          </p>
          <p className="text-xs text-dark-muted mt-1">{diagnostic.message}</p>
        </div>

        {diagnostic.suggestion && (
          <div className="pt-2 border-t border-dark-border">
            <p className="text-xs text-dark-muted">Suggestion:</p>
            <p className="text-xs text-accent-blue mt-0.5">
              {diagnostic.suggestion}
            </p>
          </div>
        )}

        {diagnostic.ttnnEquivalent && (
          <div className="pt-2 border-t border-dark-border">
            <p className="text-xs text-dark-muted">TTNN equivalent:</p>
            <code className="text-xs text-green-400 font-mono mt-0.5 block">
              {diagnostic.ttnnEquivalent}
            </code>
          </div>
        )}

        {diagnostic.docUrl && (
          <a
            href={diagnostic.docUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-accent-primary hover:underline mt-1"
          >
            View documentation
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
        )}
      </div>
    </>
  );
};
