import React from "react";
import { useNavigate } from "react-router-dom";
import { useSandboxStore } from "../../stores/sandboxStore";
import { SAMPLE_MODELS } from "../../lib/constants";

export const SampleModels: React.FC = () => {
  const { setOriginalCode, reset } = useSandboxStore();
  const navigate = useNavigate();

  const handleSelect = (code: string) => {
    reset();
    setOriginalCode(code);
    navigate("/sandbox");
  };

  return (
    <div>
      <h3 className="text-sm font-semibold text-dark-muted uppercase tracking-wider mb-3">
        Or try a sample model
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {SAMPLE_MODELS.map((model) => (
          <button
            key={model.id}
            onClick={() => handleSelect(model.code)}
            className="text-left p-4 rounded-xl bg-dark-panel border border-dark-border hover:border-accent-primary/50 hover:bg-dark-surface transition-all duration-200 group"
          >
            <div className="flex items-center gap-2 mb-1.5">
              <div className="w-2 h-2 rounded-full bg-accent-primary group-hover:shadow-lg group-hover:shadow-accent-primary/30 transition-shadow" />
              <span className="font-medium text-dark-text text-sm">
                {model.name}
              </span>
            </div>
            <p className="text-xs text-dark-muted leading-relaxed">
              {model.description}
            </p>
          </button>
        ))}
      </div>
    </div>
  );
};
