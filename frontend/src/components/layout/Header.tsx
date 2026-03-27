import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { ThemeToggle } from "../settings/ThemeToggle";
import { LLMSelector } from "../settings/LLMSelector";

export const Header: React.FC = () => {
  const location = useLocation();
  const [showSettings, setShowSettings] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-dark-panel/95 dark:bg-dark-panel/95 light:bg-white/95 backdrop-blur border-b border-dark-border dark:border-dark-border">
      <div className="max-w-[1800px] mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 bg-accent-primary rounded-lg flex items-center justify-center group-hover:bg-accent-secondary transition-colors">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points="16 18 22 12 16 6" />
                <polyline points="8 6 2 12 8 18" />
              </svg>
            </div>
            <span className="font-semibold text-lg tracking-tight">
              TT-Migrate
            </span>
          </Link>

          <nav className="hidden sm:flex items-center gap-1">
            <Link
              to="/"
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                location.pathname === "/"
                  ? "bg-dark-surface text-white"
                  : "text-dark-muted hover:text-dark-text hover:bg-dark-surface/50"
              }`}
            >
              Home
            </Link>
            <Link
              to="/sandbox"
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                location.pathname === "/sandbox"
                  ? "bg-dark-surface text-white"
                  : "text-dark-muted hover:text-dark-text hover:bg-dark-surface/50"
              }`}
            >
              Sandbox
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <ThemeToggle />

          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 rounded-lg hover:bg-dark-surface transition-colors text-dark-muted hover:text-dark-text"
              title="Settings"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
              </svg>
            </button>

            {showSettings && (
              <>
                <div
                  className="fixed inset-0 z-40"
                  onClick={() => setShowSettings(false)}
                />
                <div className="absolute right-0 top-12 z-50 w-72 p-4 bg-dark-panel border border-dark-border rounded-xl shadow-xl space-y-4">
                  <h3 className="text-sm font-semibold text-dark-text">Settings</h3>
                  <LLMSelector />
                  <div className="pt-2 border-t border-dark-border">
                    <label className="block text-xs text-dark-muted mb-1">
                      API Base URL
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-1.5 text-sm bg-dark-surface border border-dark-border rounded-lg text-dark-text focus:outline-none focus:ring-1 focus:ring-accent-primary"
                      defaultValue="http://localhost:8000"
                      onBlur={(e) => {
                        // Import dynamically to avoid circular deps
                        import("../../stores/settingsStore").then(({ useSettingsStore }) => {
                          useSettingsStore.getState().setApiBaseUrl(e.target.value);
                        });
                      }}
                    />
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
