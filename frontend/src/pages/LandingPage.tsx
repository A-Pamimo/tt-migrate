import React, { useState } from "react";
import { DropZone } from "../components/upload/DropZone";
import { CodePaste } from "../components/upload/CodePaste";
import { SampleModels } from "../components/upload/SampleModels";

type Tab = "upload" | "paste";

export const LandingPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>("upload");

  return (
    <div className="min-h-[calc(100vh-7.5rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl space-y-8">
        {/* Hero */}
        <div className="text-center space-y-3">
          <h1 className="text-4xl font-bold tracking-tight">
            <span className="text-accent-primary">TT-Migrate</span> Sandbox
          </h1>
          <p className="text-dark-muted text-lg max-w-md mx-auto">
            Analyze your PyTorch models for Tenstorrent ttnn compatibility and
            get AI-powered migration suggestions.
          </p>
        </div>

        {/* Tabs */}
        <div>
          <div className="flex border-b border-dark-border mb-4">
            <button
              onClick={() => setActiveTab("upload")}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === "upload"
                  ? "border-accent-primary text-accent-primary"
                  : "border-transparent text-dark-muted hover:text-dark-text"
              }`}
            >
              Upload File
            </button>
            <button
              onClick={() => setActiveTab("paste")}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === "paste"
                  ? "border-accent-primary text-accent-primary"
                  : "border-transparent text-dark-muted hover:text-dark-text"
              }`}
            >
              Paste Code
            </button>
          </div>

          {activeTab === "upload" ? <DropZone /> : <CodePaste />}
        </div>

        {/* Samples */}
        <SampleModels />
      </div>
    </div>
  );
};
