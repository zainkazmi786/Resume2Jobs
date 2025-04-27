from langchain.tools import Tool
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import processed_jobs

  # Collection storing similarity scores

def fetch_top_jobs(user_id: str) -> dict:
    """
    Fetch the top 10 job matches for a user based on cosine similarity.
    
    :param user_id: The user's unique identifier.
    :return: A dictionary containing the top 10 ranked jobs.
    """
    # ✅ Query the database for the user's top jobs sorted by similarity
    query = {"userid": user_id}
    top_jobs = list(processed_jobs.find(query, {"_id": 0}).sort("similarity_score", -1).limit(10))
    
    # ✅ Return the ranked job matches
    return {
        "user_id": user_id,
        "top_jobs": top_jobs
    }

# ✅ Create the LangChain tool
fetch_top_jobs_tool = Tool(
    name="Fetch Top Job Matches",
    func=fetch_top_jobs,
    description=(
        "Fetches the top 10 most relevant job matches for the user based on the processed data "
        "and cosine similarity. Requires the user's email (user_id). "
        "This is the final step of the workflow."
    )
)

if __name__ == "__main__":
    result = fetch_top_jobs("mansoormaham26@gmail.com")
    print(result)