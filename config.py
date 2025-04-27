import os
from pymongo import MongoClient
from dotenv import load_dotenv

import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)) 
PROMPT_PATH = os.path.join(ROOT_DIR, "prompts", "systemprompt.txt")
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Load environment variables from .env file
# ROOT_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv()


# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Initialize MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
jobss = db[os.getenv("JOBS_COLLECTION")]
user = db[os.getenv("USER_COLLECTION")]
processed_jobs = db[os.getenv("PROCESSED_JOBS_COLLECTION")]