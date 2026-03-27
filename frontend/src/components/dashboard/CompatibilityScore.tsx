import React from "react";

interface CompatibilityScoreProps {
  score: number;
}

export const CompatibilityScore: React.FC<CompatibilityScoreProps> = ({
  score,
}) => {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 75) return { stroke: "#22c55e", text: "text-green-400" };
    if (s >= 40) return { stroke: "#f59e0b", text: "text-amber-400" };
    return { stroke: "#ef4444", text: "text-red-400" };
  };

  const color = getColor(score);

  return (
    <div className="panel p-5">
      <h3 className="text-xs font-semibold text-dark-muted uppercase tracking-wider mb-4">
        Compatibility Score
      </h3>
      <div className="flex items-center justify-center">
        <div className="relative w-36 h-36">
          <svg
            className="transform -rotate-90 w-36 h-36"
            viewBox="0 0 120 120"
          >
            {/* Background ring */}
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="#3b3b5c"
              strokeWidth="10"
            />
            {/* Score ring */}
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke={color.stroke}
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-3xl font-bold ${color.text}`}>
              {score}%
            </span>
            <span className="text-xs text-dark-muted mt-0.5">compatible</span>
          </div>
        </div>
      </div>
    </div>
  );
};
