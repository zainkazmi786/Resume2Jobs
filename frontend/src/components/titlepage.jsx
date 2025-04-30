// src/components/titlepage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, Briefcase, TrendingUp, ChevronRight } from "lucide-react";

const TitlePage = () => {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Trigger entrance animation after component mount
    setVisible(true);
  }, []);

  const handleGetStarted = () => {
    navigate("/upload");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center p-4 overflow-hidden">
      <div 
        className={`transition-all duration-1000 transform ${
          visible ? "translate-y-0 opacity-100" : "translate-y-20 opacity-0"
        }`}
      >
        <div className="text-center mb-8">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 tracking-tight">
            <span className="inline-block animate-bounce-slow">R</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.1s" }}>E</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.2s" }}>S</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.3s" }}>U</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.4s" }}>M</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.5s" }}>E</span>
            <span className="inline-block animate-bounce-slow" style={{ animationDelay: "0.6s" }}>2</span>
            <span className="inline-block animate-bounce-slow text-blue-200" style={{ animationDelay: "0.7s" }}>J</span>
            <span className="inline-block animate-bounce-slow text-blue-200" style={{ animationDelay: "0.8s" }}>O</span>
            <span className="inline-block animate-bounce-slow text-blue-200" style={{ animationDelay: "0.9s" }}>B</span>
            <span className="inline-block animate-bounce-slow text-blue-200" style={{ animationDelay: "1.0s" }}>S</span>
          </h1>
          <p className="text-xl md:text-2xl text-white opacity-90 max-w-xl mx-auto">
            Transform your resume into job opportunities with AI-powered matching
          </p>
        </div>
      </div>

      <div 
        className={`grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full mb-12 transition-all duration-1000 delay-500 transform ${
          visible ? "translate-y-0 opacity-100" : "translate-y-20 opacity-0"
        }`}
      >
        <FeatureCard 
          icon={FileText} 
          title="Resume Analysis" 
          description="Our AI analyzes your resume to extract key skills, experience, and qualifications"
          delay={0}
        />
        <FeatureCard 
          icon={Briefcase} 
          title="Job Matching" 
          description="Get matched with relevant job opportunities based on your unique profile"
          delay={150}
        />
        <FeatureCard 
          icon={TrendingUp} 
          title="Career Insights" 
          description="Receive personalized recommendations to improve your job prospects"
          delay={300}
        />
      </div>

      <div 
        className={`transition-all duration-1000 delay-1000 transform ${
          visible ? "translate-y-0 opacity-100" : "translate-y-20 opacity-0"
        }`}
      >
        <button
          onClick={handleGetStarted}
          className="group bg-white text-blue-600 hover:bg-blue-50 py-3 px-8 rounded-full font-bold text-lg shadow-lg hover:shadow-xl transition-all flex items-center"
        >
          Get Started
          <ChevronRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

const FeatureCard = ({ icon: Icon, title, description, delay }) => {
  const [visible, setVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(true);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div 
      className={`bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-1 transform ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
      }`}
    >
      <div className="bg-blue-100 p-3 rounded-full w-14 h-14 flex items-center justify-center mb-4">
        <Icon size={28} className="text-blue-600" />
      </div>
      <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default TitlePage;