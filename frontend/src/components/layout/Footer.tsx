import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-dark-border bg-dark-panel/50 py-4">
      <div className="max-w-[1800px] mx-auto px-4 sm:px-6 flex items-center justify-between text-xs text-dark-muted">
        <span>TT-Migrate Sandbox &mdash; Tenstorrent Model Migration Tool</span>
        <span>
          Powered by{" "}
          <a
            href="https://tenstorrent.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-accent-primary hover:underline"
          >
            Tenstorrent
          </a>
        </span>
      </div>
    </footer>
  );
};
