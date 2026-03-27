import React from "react";
import { MigrationEffort as MigrationEffortType } from "../../lib/types";
import { EFFORT_COLORS, EFFORT_LABELS } from "../../lib/constants";

interface MigrationEffortProps {
  effort: MigrationEffortType;
}

export const MigrationEffort: React.FC<MigrationEffortProps> = ({ effort }) => {
  const colorClasses = EFFORT_COLORS[effort];
  const label = EFFORT_LABELS[effort];

  const descriptions: Record<MigrationEffortType, string> = {
    low: "Most operations are directly supported. Minimal code changes expected.",
    medium:
      "Several operations need workarounds or partial rewrites. Moderate effort required.",
    high: "Significant portions of the model need rearchitecting for ttnn compatibility.",
  };

  return (
    <div className="panel p-5">
      <h3 className="text-xs font-semibold text-dark-muted uppercase tracking-wider mb-4">
        Migration Effort
      </h3>
      <div className="flex items-center gap-3">
        <span
          className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-semibold border ${colorClasses}`}
        >
          {label}
        </span>
      </div>
      <p className="text-xs text-dark-muted mt-3 leading-relaxed">
        {descriptions[effort]}
      </p>
    </div>
  );
};
