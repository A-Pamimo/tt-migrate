import { create } from "zustand";
import { LLMProvider, Theme } from "../lib/types";
import { DEFAULT_API_BASE_URL } from "../lib/constants";
import apiClient from "../lib/api";

interface SettingsState {
  theme: Theme;
  llmProvider: LLMProvider;
  apiBaseUrl: string;

  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  setLlmProvider: (provider: LLMProvider) => void;
  setApiBaseUrl: (url: string) => void;
}

const getInitialTheme = (): Theme => {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("tt-migrate-theme");
    if (saved === "light" || saved === "dark") return saved;
  }
  return "dark";
};

export const useSettingsStore = create<SettingsState>((set) => ({
  theme: getInitialTheme(),
  llmProvider: "anthropic",
  apiBaseUrl: DEFAULT_API_BASE_URL,

  setTheme: (theme) => {
    if (typeof window !== "undefined") {
      localStorage.setItem("tt-migrate-theme", theme);
      document.documentElement.classList.toggle("dark", theme === "dark");
      document.documentElement.classList.toggle("light", theme === "light");
    }
    set({ theme });
  },

  toggleTheme: () => {
    set((state) => {
      const newTheme = state.theme === "dark" ? "light" : "dark";
      if (typeof window !== "undefined") {
        localStorage.setItem("tt-migrate-theme", newTheme);
        document.documentElement.classList.toggle("dark", newTheme === "dark");
        document.documentElement.classList.toggle("light", newTheme === "light");
      }
      return { theme: newTheme };
    });
  },

  setLlmProvider: (provider) => set({ llmProvider: provider }),

  setApiBaseUrl: (url) => {
    apiClient.setBaseUrl(url);
    set({ apiBaseUrl: url });
  },
}));
