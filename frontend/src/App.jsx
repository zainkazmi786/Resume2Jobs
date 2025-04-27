// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResumeUpload from "./components/resumeupload";
import Progress from "./components/progress";
import AgentInterface from "./components/agentinterface";

function App() {
  return (
    // <AgentInterface/>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ResumeUpload />} />
        <Route path="/progress" element={<Progress />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
