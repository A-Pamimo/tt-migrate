/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#1e1e2e",
          panel: "#282840",
          surface: "#313150",
          border: "#3b3b5c",
          text: "#cdd6f4",
          muted: "#8888aa",
        },
        accent: {
          primary: "#7c3aed",
          secondary: "#6d28d9",
          blue: "#3b82f6",
          green: "#22c55e",
          amber: "#f59e0b",
          red: "#ef4444",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
    },
  },
  plugins: [],
};
