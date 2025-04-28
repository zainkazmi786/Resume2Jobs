# agent initializer.py
import sys
import os
from streaming_executor import StreamingAgentExecutor


# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import ENV_PATH , PROMPT_PATH
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# from langchain.tools import Tool
from langchain_groq import ChatGroq
from tools.extractprofile import resume_extraction_tool
from tools.check_jobs import check_jobs_tool
from tools.fetch_jobs import job_scraping_tool
from tools.similaritycheck import process_jobs_tool
from tools.email_user import email_jobs_tool
from dotenv import load_dotenv
import os

load_dotenv(ENV_PATH)

# Load system prompt from file
with open(PROMPT_PATH, "r") as f:
    system_prompt = f.read()

# ✅ Initialize the Qwen model (via Groq)
llm = ChatGroq(
    model_name="mistral-saba-24b",
    api_key=os.getenv("GROK_API_KEY")  # replace with env var or use dotenv if needed
)

# ✅ Define your tools
tools = [
    resume_extraction_tool,
    check_jobs_tool,
    job_scraping_tool,
    process_jobs_tool,
    email_jobs_tool
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Initialize the agent with tools and system prompt
base_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    agent_kwargs={"system_message": system_prompt},
    handle_parsing_errors=True
)
agent = StreamingAgentExecutor.from_agent_and_tools(
    agent=base_agent.agent,
    tools=tools,  # <-- Use the tools you explicitly created
    memory=memory
)
__all__ = ['base_agent', 'agent', 'tools', 'memory']


# ✅ Run the agent with input

if __name__ == "__main__":
    user_input = "Please extract the profile from this resume at (./Resumes/cv2.pdf) and find top 10 job matches based on the instructions. Follow every step mentioned to you to get to the goal"


    response = base_agent.invoke({
         "input": user_input
 

    })
    print("\n🧠 Agent Response:\n", response)
