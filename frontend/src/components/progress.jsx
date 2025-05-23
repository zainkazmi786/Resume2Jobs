// src/components/Progress.jsx
import React, { useEffect, useState, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import WorkflowDiagram from "./WorkflowDiagram";

export default function Progress() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processComplete, setProcessComplete] = useState(false);
  // Always use animation mode while processing
  const [isAnimating, setIsAnimating] = useState(true);
  const messagesEndRef = useRef(null);
  const location = useLocation();
  const navigate = useNavigate();
  const { filename, prompt } = location.state || {};

  // Auto-scroll to bottom when messages update
  // const scrollToBottom = () => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // };

  // useEffect(() => {
  //   scrollToBottom();
  // }, [messages]);

  useEffect(() => {
    if (!filename || !prompt) {
      setError("Missing filename or prompt");
      setLoading(false);
      return;
    }

    // Add initial message
    setMessages([{ 
      type: "system", 
      content: `Starting job matching process for resume: ${filename}` 
    }]);

    // Step 1: POST to prepare-stream first
    fetch("http://localhost:5000/prepare-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, prompt }),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to prepare stream: ${res.status}`);
        
        setMessages(prev => [
          ...prev, 
          { type: "system", content: "Resume processing started..." }
        ]);
        
        // Step 2: Open the EventSource for streaming data
        const eventSource = new EventSource("http://localhost:5000/stream-process");
  
        eventSource.onmessage = (e) => {
          try {
            if (e.data === "✅ END") {
              eventSource.close();
              setLoading(false);
              setProcessComplete(true);
              setIsAnimating(false); // Stop animation when processing is complete
              setMessages(prev => [
                ...prev, 
                { type: "system", content: "✅ Processing completed! Your job matches are ready." }
              ]);
              return;
            }
            
            // Just add whatever message comes from the backend to the messages list
            setMessages(prev => [...prev, { type: "system", content: e.data }]);
          } catch (err) {
            // Handle non-JSON data
            setMessages(prev => [...prev, { type: "system", content: e.data }]);
          }
        };
  
        eventSource.onerror = (err) => {
          console.error("EventSource failed:", err);
          setMessages(prev => [...prev, { type: "error", content: "❌ Connection to server lost" }]);
          setError("Connection to server lost");
          setIsAnimating(false); // Stop animation on error
          eventSource.close();
          setLoading(false);
        };
  
        return () => eventSource.close();
      })
      .catch((err) => {
        console.error("Failed to initiate stream:", err);
        setMessages(prev => [...prev, { type: "error", content: `❌ ${err.message}` }]);
        setError(err.message);
        setIsAnimating(false); // Stop animation on error
        setLoading(false);
      });
  }, [filename, prompt]);

  const handleNewSearch = () => {
    navigate("/");
  };

  if (!filename || !prompt) {
    return (
      <div className="p-4 text-center">
        <p className="text-red-600 mb-4">No resume/prompt provided</p>
        <button 
          onClick={handleNewSearch}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Return to Upload
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-800">Resume Processing Progress</h1>
            {processComplete && (
              <button 
                onClick={handleNewSearch}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                New Search
              </button>
            )}
            {!processComplete && loading && (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mr-2"></div>
                <span className="text-blue-600">Processing...</span>
              </div>
            )}
          </div>
          
          {/* Workflow Diagram - Use animation mode while processing */}
          <WorkflowDiagram isAnimating={isAnimating} />
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              <p><strong>Error:</strong> {error}</p>
              <button 
                onClick={handleNewSearch}
                className="mt-2 px-4 py-1 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Try Again
              </button>
            </div>
          )}
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Process Details</h2>
          <div className="space-y-3 bg-gray-50 p-4 rounded-lg h-[40vh] overflow-y-auto">
            {messages.map((message, index) => {
              // Determine the styling based on message type
              let bgColor = "bg-gray-100";
              let textColor = "text-gray-800";
              let borderColor = "border-gray-200";
              
              switch(message.type) {
                case "system":
                  bgColor = "bg-blue-50";
                  textColor = "text-blue-800";
                  borderColor = "border-blue-200";
                  break;
                case "tool":
                  bgColor = "bg-purple-50";
                  textColor = "text-purple-800";
                  borderColor = "border-purple-200";
                  break;
                case "result":
                  bgColor = "bg-green-50";
                  textColor = "text-green-800";
                  borderColor = "border-green-200";
                  break;
                case "error":
                  bgColor = "bg-red-50";
                  textColor = "text-red-800";
                  borderColor = "border-red-200";
                  break;
                case "final":
                  bgColor = "bg-yellow-50";
                  textColor = "text-yellow-800";
                  borderColor = "border-yellow-200";
                  break;
                default:
                  break;
              }
              
              return (
                <div
                  key={index}
                  className={`${bgColor} ${textColor} px-4 py-3 rounded-lg border ${borderColor} shadow-sm`}
                >
                  <pre className="whitespace-pre-wrap font-sans text-sm">{message.content}</pre>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}