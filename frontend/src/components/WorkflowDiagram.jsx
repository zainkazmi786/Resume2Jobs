// src/components/WorkflowDiagram.jsx
import React, { useState, useEffect } from "react";
import { FileText, Search, Database, Cog, Mail } from "lucide-react";

const WorkflowDiagram = ({ isAnimating = false, activeStep = null }) => {
  const [highlightedStep, setHighlightedStep] = useState(0);
  
  const steps = [
    { 
      icon: FileText, 
      title: "Resume Extraction", 
      description: "Extract structured information from your resume" 
    },
    { 
      icon: Search, 
      title: "Check Jobs", 
      description: "Check existing job records in database" 
    },
    { 
      icon: Database, 
      title: "Job Scraping", 
      description: "Scrape new jobs matching your profile" 
    },
    { 
      icon: Cog, 
      title: "Process Jobs", 
      description: "Match your profile with available jobs" 
    },
    { 
      icon: Mail, 
      title: "Email Results", 
      description: "Send top 10 job matches to your email" 
    }
  ];

  // Animation effect to cycle through steps when isAnimating is true
  useEffect(() => {
    // Only animate if specifically told to animate
    if (isAnimating) {
      const interval = setInterval(() => {
        setHighlightedStep((prev) => (prev + 1) % steps.length);
      }, 2000);
      return () => clearInterval(interval);
    } else if (activeStep !== null) {
      // If a specific step is requested and not animating
      setHighlightedStep(activeStep);
    }
  }, [isAnimating, activeStep, steps.length]);

  return (
    <div className="my-8">
      <div className="flex flex-wrap justify-center gap-4 md:gap-6">
        {steps.map((step, index) => {
          const StepIcon = step.icon;
          const isActive = index === highlightedStep;
          return (
            <div 
              key={index}
              className={`
                relative w-56 h-56 p-5 rounded-xl shadow-lg transition-all duration-300 flex flex-col items-center justify-center text-center
                ${isActive 
                  ? "bg-blue-500 text-white transform scale-105 shadow-xl" 
                  : "bg-white text-gray-700 shadow"
                }
              `}
            >
              <div className={`
                absolute top-3 left-3 rounded-full w-8 h-8 flex items-center justify-center
                ${isActive ? "bg-white text-blue-500" : "bg-blue-100 text-blue-500"}
              `}>
                {index + 1}
              </div>
              <StepIcon 
                size={48} 
                className={`mb-4 ${isActive ? "text-white" : "text-blue-500"}`} 
              />
              <h3 className="font-bold text-lg mb-2">{step.title}</h3>
              <p className={`text-sm ${isActive ? "text-blue-100" : "text-gray-500"}`}>
                {step.description}
              </p>
              {isActive && (
                <div className="absolute bottom-0 left-0 w-full h-1 bg-blue-300 rounded-b-xl">
                  <div className="h-full bg-white animate-pulse rounded-b-xl"></div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default WorkflowDiagram;