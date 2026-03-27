import React from "react";
import { AnalysisSummary } from "../../lib/types";
import { SEVERITY_COLORS } from "../../lib/constants";

interface SeverityBreakdownProps {
  summary: AnalysisSummary;
}

export const SeverityBreakdown: React.FC<SeverityBreakdownProps> = ({
  summary,
}) => {
  const { total, supported, partial, unsupported } = summary;
  if (total === 0) return null;

  const items = [
    {
      label: "Supported",
      count: supported,
      severity: "supported" as const,
      pct: Math.round((supported / total) * 100),
    },
    {
      label: "Partial",
      count: partial,
      severity: "partial" as const,
      pct: Math.round((partial / total) * 100),
    },
    {
      label: "Unsupported",
      count: unsupported,
      severity: "unsupported" as const,
      pct: Math.round((unsupported / total) * 100),
    },
  ];

  return (
    <div className="panel p-5">
      <h3 className="text-xs font-semibold text-dark-muted uppercase tracking-wider mb-4">
        Severity Breakdown
      </h3>
      <div className="space-y-3">
        {items.map((item) => {
          const colors = SEVERITY_COLORS[item.severity];
          return (
            <div key={item.severity}>
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${colors.dot}`} />
                  <span className="text-sm text-dark-text">{item.label}</span>
                </div>
                <span className={`text-sm font-medium ${colors.text}`}>
                  {item.count}{" "}
                  <span className="text-dark-muted font-normal">
                    ({item.pct}%)
                  </span>
                </span>
              </div>
              <div className="w-full h-2 bg-dark-surface rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${colors.dot} transition-all duration-700 ease-out`}
                  style={{ width: `${item.pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Stacked bar summary */}
      <div className="mt-4 flex rounded-full overflow-hidden h-2.5">
        {items.map(
          (item) =>
            item.pct > 0 && (
              <div
                key={item.severity}
                className={`${SEVERITY_COLORS[item.severity].dot} transition-all duration-700`}
                style={{ width: `${item.pct}%` }}
                title={`${item.label}: ${item.pct}%`}
              />
            )
        )}
      </div>
    </div>
  );
};
