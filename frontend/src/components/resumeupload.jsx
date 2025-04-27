// src/components/ResumeUpload.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [prompt, setPrompt] = useState("Please extract the profile from this resume and find top 10 job matches based on the instructions. Follow every step mentioned to you to get to the goal");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!resume) return setMessage("Please select a resume");
    
    setLoading(true);
    setMessage("Uploading resume...");
    
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("prompt", prompt);
  
    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setMessage(data.message + ": " + data.filename);
        // Navigate to progress page with resume filename and prompt
        navigate("/progress", { state: { filename: data.filename, prompt } });
      } else {
        setMessage("Upload failed: " + data.error);
        setLoading(false);
      }
    } catch (error) {
      setMessage("Upload failed: " + error.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4 text-center text-indigo-700">Resume Job Matcher</h2>
        <p className="text-gray-600 mb-6 text-center">Upload your resume and let AI find the best job matches for you</p>
        
        <form onSubmit={handleUpload}>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Choose Resume (PDF)</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
              className="w-full border border-gray-300 p-2 rounded"
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Custom Prompt (Optional)</label>
            <textarea
              rows="3"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded"
              placeholder="Enter your custom prompt or use the default..."
            ></textarea>
          </div>
          <button
            type="submit"
            disabled={loading}
            className={`w-full ${loading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'} text-white py-2 rounded transition`}
          >
            {loading ? "Processing..." : "Find Job Matches"}
          </button>
        </form>
        {message && (
          <p className={`mt-4 text-center text-sm ${message.includes("failed") ? "text-red-600" : "text-green-600"}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;