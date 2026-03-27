import React from "react";
import { useSettingsStore } from "../../stores/settingsStore";
import { LLMProvider } from "../../lib/types";

const providers: { value: LLMProvider; label: string }[] = [
  { value: "anthropic", label: "Anthropic (Claude)" },
  { value: "openai", label: "OpenAI (GPT)" },
  { value: "google", label: "Google (Gemini)" },
];

export const LLMSelector: React.FC = () => {
  const { llmProvider, setLlmProvider } = useSettingsStore();

  return (
    <div>
      <label className="block text-xs text-dark-muted mb-1">LLM Provider</label>
      <select
        value={llmProvider}
        onChange={(e) => setLlmProvider(e.target.value as LLMProvider)}
        className="w-full px-3 py-1.5 text-sm bg-dark-surface border border-dark-border rounded-lg text-dark-text focus:outline-none focus:ring-1 focus:ring-accent-primary appearance-none cursor-pointer"
      >
        {providers.map((p) => (
          <option key={p.value} value={p.value}>
            {p.label}
          </option>
        ))}
      </select>
    </div>
  );
};
