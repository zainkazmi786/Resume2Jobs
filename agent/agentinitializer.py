# agentinitializer.py - Updated version
import sys
import os
from agent.streaming_executor import StreamingAgentExecutor

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import ENV_PATH, PROMPT_PATH
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from tools.extractprofile import resume_extraction_tool
from tools.check_jobs import check_jobs_tool
from tools.fetch_jobs import job_scraping_tool
from tools.similaritycheck import process_jobs_tool
from tools.email_user import email_jobs_tool
from dotenv import load_dotenv

load_dotenv(ENV_PATH)

# Load system prompt
with open(PROMPT_PATH, "r") as f:
    system_prompt = f.read()

# Initialize model
llm = ChatGroq(
    model_name="mistral-saba-24b",
    api_key=os.getenv("GROK_API_KEY")
)

# Define and verify tools
tools = [
    resume_extraction_tool,
    check_jobs_tool,
    job_scraping_tool,
    process_jobs_tool,
    email_jobs_tool
]

# Print tool names to verify they are correctly registered
print("📋 Registered tool names:", [tool.name for tool in tools])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize normal agent
base_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    agent_kwargs={"system_message": system_prompt},
    handle_parsing_errors=True
)

# Verify the agent has access to the tools
print("🔍 Agent tools:", [tool.name for tool in base_agent.tools])

# Initialize streaming agent
agent = StreamingAgentExecutor.from_agent_and_tools(
    agent=base_agent.agent,
    tools=tools,
    memory=memory
)

__all__ = ['base_agent', 'agent', 'tools', 'memory']