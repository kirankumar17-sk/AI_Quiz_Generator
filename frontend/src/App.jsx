import React, { useState } from 'react';
import './App.css';
import GenerateQuizTab from './tabs/GenerateQuizTab';
import HistoryTab from './tabs/HistoryTab';

function TabButton({ active, children, className, ...props }) {
  return (
    <button
      className={className}
      {...props}
    >
      {children}
    </button>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("generate");

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Wikipedia Quiz Generator</h1>
      </header>
      <div className="tab-row">
        <TabButton 
          className={activeTab === "generate" ? "tab-button tab-button--active" : "tab-button tab-button--inactive"}
          active={activeTab === "generate"} 
          onClick={() => setActiveTab("generate")}
        >
          Generate Quiz
        </TabButton>
        <TabButton 
          className={activeTab === "history" ? "tab-button tab-button--active" : "tab-button tab-button--inactive"}
          active={activeTab === "history"} 
          onClick={() => setActiveTab("history")}
        >
          History
        </TabButton>
      </div>
      <main className="main">
        {activeTab === "generate" ? <GenerateQuizTab /> : <HistoryTab />}
      </main>
    </div>
  );
}