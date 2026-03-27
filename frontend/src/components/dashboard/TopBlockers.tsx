import React from "react";
import { Blocker } from "../../lib/types";
import { SEVERITY_COLORS } from "../../lib/constants";

interface TopBlockersProps {
  blockers: Blocker[];
}

export const TopBlockers: React.FC<TopBlockersProps> = ({ blockers }) => {
  if (!blockers || blockers.length === 0) return null;

  return (
    <div className="panel p-5">
      <h3 className="text-xs font-semibold text-dark-muted uppercase tracking-wider mb-4">
        Top Blockers
      </h3>
      <div className="space-y-2">
        {blockers.slice(0, 5).map((blocker, i) => {
          const colors = SEVERITY_COLORS[blocker.severity];
          return (
            <div
              key={i}
              className="flex items-center justify-between p-3 rounded-lg bg-dark-surface/50 border border-dark-border/50"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div
                  className={`shrink-0 w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold ${colors.bg} ${colors.text}`}
                >
                  {blocker.count}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-dark-text truncate">
                    {blocker.operation}
                  </p>
                  <p className="text-xs text-dark-muted truncate">
                    {blocker.impact}
                  </p>
                </div>
              </div>
              <span
                className={`shrink-0 ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${colors.bg} ${colors.text} border ${colors.border}`}
              >
                {blocker.severity}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
