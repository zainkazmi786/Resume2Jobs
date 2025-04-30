// src/components/resumeupload.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, Upload, ArrowLeft, Sparkles } from "lucide-react";

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [resumeName, setResumeName] = useState("");
  const [prompt, setPrompt] = useState("Please extract the profile from this resume and find top 10 job matches based on the instructions. Follow every step mentioned to you to get to the goal");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [isVisible, setIsVisible] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    // Trigger entrance animation
    setIsVisible(true);
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResume(file);
      setResumeName(file.name);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
      setResume(file);
      setResumeName(file.name);
    } else {
      setMessage("Please upload a PDF file");
    }
  };

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

  const goBack = () => {
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div 
        className={`bg-white shadow-2xl rounded-xl p-8 max-w-lg w-full transition-all duration-700 transform ${
          isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
        }`}
      >
        <div className="flex justify-between items-center mb-6">
          <button 
            onClick={goBack} 
            className="text-gray-500 hover:text-gray-700 flex items-center"
          >
            <ArrowLeft size={20} className="mr-1" />
            <span>Back</span>
          </button>
          <h2 className="text-2xl font-bold text-center text-indigo-700">Upload Your Resume</h2>
          <div className="w-20"></div> {/* Spacer for centering */}
        </div>
        
        <form onSubmit={handleUpload}>
          <div 
            className={`mb-6 border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all ${
              isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-300"
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById("file-upload").click()}
          >
            <input
              id="file-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className="flex flex-col items-center justify-center">
              {resumeName ? (
                <>
                  <FileText size={48} className="text-blue-500 mb-3" />
                  <p className="text-blue-600 font-medium">{resumeName}</p>
                  <p className="text-sm text-gray-500 mt-1">Click or drag to change file</p>
                </>
              ) : (
                <>
                  <Upload size={48} className="text-gray-400 mb-3" />
                  <p className="text-lg font-medium text-gray-700">Drop your resume here</p>
                  <p className="text-sm text-gray-500 mt-1">Or click to browse (PDF only)</p>
                </>
              )}
            </div>
          </div>

          <div className="mb-6">
            <label className="block mb-2 font-semibold text-gray-700">Customize Your Job Search</label>
            <div className="relative">
              <Sparkles size={20} className="absolute left-3 top-3 text-purple-500" />
              <textarea
                rows="3"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full border border-gray-300 p-3 pl-10 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                placeholder="Enter your custom requirements or preferences..."
              ></textarea>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Customize how AI should analyze your resume and what kind of jobs to look for
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full ${
              loading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
            } text-white py-3 px-4 rounded-lg font-medium text-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center`}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Processing...
              </>
            ) : (
              <>Find Perfect Job Matches</>
            )}
          </button>
        </form>

        {message && (
          <div className={`mt-4 p-3 rounded-lg ${
            message.includes("failed") 
              ? "bg-red-50 text-red-600 border border-red-200" 
              : "bg-green-50 text-green-600 border border-green-200"
          }`}>
            <p className="text-center text-sm">{message}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;