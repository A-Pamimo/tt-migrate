import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { LandingPage } from "./pages/LandingPage";
import { SandboxPage } from "./pages/SandboxPage";
import { useSettingsStore } from "./stores/settingsStore";

const App: React.FC = () => {
  const { theme } = useSettingsStore();

  // Apply theme class on mount and changes
  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    document.documentElement.classList.toggle("light", theme === "light");
  }, [theme]);

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-dark-bg dark:bg-dark-bg">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/sandbox" element={<SandboxPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
};

export default App;
