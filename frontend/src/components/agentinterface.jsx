import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AgentInterface = () => {
  const [filename, setFilename] = useState('');
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);
  const [eventSource, setEventSource] = useState(null);

  // Handle file upload
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  // Start processing
  const startProcessing = async () => {
    if (!file || !prompt) {
      alert('Please select a file and enter a prompt');
      return;
    }

    setIsProcessing(true);
    setMessages([{ type: 'status', content: 'Starting processing...' }]);

    try {
      // First upload the file
      const formData = new FormData();
      formData.append('resume', file);
      
      await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Then start the agent stream
      const newEventSource = new EventSource(`http://127.0.0.1:5000/stream-tools?filename=${encodeURIComponent(filename)}&prompt=${encodeURIComponent(prompt)}`);
      
      newEventSource.onmessage = (e) => {
        if (e.data === '✅ END') {
          newEventSource.close();
          setIsProcessing(false);
          return;
        }

        try {
          const data = JSON.parse(e.data);
          handleStreamEvent(data);
        } catch (error) {
          console.error('Error parsing event:', error);
        }
      };

      newEventSource.onerror = () => {
        setMessages(prev => [...prev, { 
          type: 'error', 
          content: 'Connection error occurred' 
        }]);
        newEventSource.close();
        setIsProcessing(false);
      };

      setEventSource(newEventSource);

    } catch (error) {
      console.error('Error:', error);
      setIsProcessing(false);
    }
  };

  // Handle different event types from SSE
  const handleStreamEvent = (data) => {
    switch(data.type) {
      case 'tool_start':
        setMessages(prev => [...prev, {
          type: 'tool-start',
          tool: data.tool,
          input: data.input,
          timestamp: new Date().toISOString()
        }]);
        break;

      case 'tool_end':
        setMessages(prev => [...prev, {
          type: 'tool-result',
          tool: data.tool,
          output: data.output,
          timestamp: new Date().toISOString()
        }]);
        break;

      case 'error':
        setMessages(prev => [...prev, {
          type: 'error',
          content: data.message,
          traceback: data.traceback,
          timestamp: new Date().toISOString()
        }]);
        break;

      case 'status':
        setMessages(prev => [...prev, {
          type: 'status',
          content: data.message,
          timestamp: new Date().toISOString()
        }]);
        break;

      default:
        console.warn('Unknown event type:', data.type);
    }
  };

  // Clean up event source
  useEffect(() => {
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [eventSource]);

  // Render message bubbles
  const renderMessage = (message, index) => {
    switch(message.type) {
      case 'tool-start':
        return (
          <div key={index} className="tool-start-message">
            <div className="tool-header">
              <span className="tool-badge">{message.tool}</span>
              <span className="timestamp">{new Date(message.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="tool-input">
              <strong>Input:</strong> {JSON.stringify(message.input, null, 2)}
            </div>
          </div>
        );

      case 'tool-result':
        return (
          <div key={index} className="tool-result-message">
            <div className="tool-header">
              <span className="tool-badge">{message.tool}</span>
              <span className="timestamp">{new Date(message.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="tool-output">
              <strong>Result:</strong> 
              <pre>{JSON.stringify(message.output, null, 2)}</pre>
            </div>
          </div>
        );

      case 'error':
        return (
          <div key={index} className="error-message">
            <div className="error-header">❌ Error</div>
            <div className="error-content">{message.content}</div>
            {message.traceback && (
              <details className="error-details">
                <summary>Details</summary>
                <pre>{message.traceback}</pre>
              </details>
            )}
          </div>
        );

      default:
        return (
          <div key={index} className="status-message">
            {message.content}
          </div>
        );
    }
  };

  return (
    <div className="agent-interface-container">
      <div className="upload-section">
        <h2>Resume Processing Agent</h2>
        
        <div className="file-upload">
          <label>
            Upload Resume:
            <input 
              type="file" 
              accept=".pdf,.docx" 
              onChange={handleFileChange}
              disabled={isProcessing}
            />
          </label>
          {filename && <div className="filename">{filename}</div>}
        </div>

        <div className="prompt-input">
          <label>
            Processing Prompt:
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="What should I do with this resume?"
              disabled={isProcessing}
            />
          </label>
        </div>

        <button 
          onClick={startProcessing}
          disabled={isProcessing || !file || !prompt}
        >
          {isProcessing ? 'Processing...' : 'Start Processing'}
        </button>
      </div>

      <div className="message-stream">
        <h3>Processing Log</h3>
        <div className="messages-container">
          {messages.length > 0 ? (
            messages.map((message, index) => renderMessage(message, index))
          ) : (
            <div className="empty-state">
              No activity yet. Upload a resume and enter a prompt to begin.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
export default AgentInterface;
