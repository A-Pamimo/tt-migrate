import React, { useState } from "react";
import { useSandboxStore } from "../../stores/sandboxStore";
import { useNavigate } from "react-router-dom";

export const CodePaste: React.FC = () => {
  const [code, setCode] = useState("");
  const { setOriginalCode } = useSandboxStore();
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (code.trim()) {
      setOriginalCode(code);
      navigate("/sandbox");
    }
  };

  return (
    <div className="space-y-3">
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your PyTorch model code here..."
        className="w-full h-64 px-4 py-3 bg-dark-surface border border-dark-border rounded-xl text-dark-text font-mono text-sm resize-none focus:outline-none focus:ring-1 focus:ring-accent-primary placeholder-dark-muted scrollbar-thin"
        spellCheck={false}
      />
      <div className="flex justify-end">
        <button
          onClick={handleSubmit}
          disabled={!code.trim()}
          className="btn-primary"
        >
          Open in Sandbox
        </button>
      </div>
    </div>
  );
};
