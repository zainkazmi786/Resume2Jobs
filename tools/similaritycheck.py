from langchain.tools import Tool
from sentence_transformers import SentenceTransformer, util
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import jobss, user, processed_jobs
from pydantic import BaseModel
from typing import List

class ProcessJobsInput(BaseModel):
    user_id: str
    job_titles: List[str]
    city: str
    country: str
    experience_list: List[str]
    workplace_type: List[str]


# Load BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to find matched skills in a job description
def find_matched_skills(job_description, resume_keywords):
    return [skill for skill in resume_keywords if skill.lower() in job_description.lower()]

def process_jobs(input_data):     

    """Ranks jobs based on similarity with user profile and saves results to MongoDB."""
    try:
        if isinstance(input_data, str):
            data = json.loads(input_data)
        else:
            data = input_data
    except json.JSONDecodeError:
        return {"error": "Invalid input format. Must be a JSON string with proper keys."}
    try:
        user_id = data.get("user_id")
        job_titles = data.get("job_titles", [])
        city = data.get("city")
        country = data.get("country")
        explist = data.get("experience_list", [])
        workplace = data.get("workplace_type", [])

        user_data = user.find_one({"email": user_id})
        if not user_data:
            return "❌ User not found"

        resume_keywords = user_data.get("keywords", [])
        if not resume_keywords:
            return "⚠️ No keywords found in user profile"

        resume_text = " ".join(resume_keywords)
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)

        total_processed = []

        for job_title in job_titles:
            query = {
                "job_searched": job_title,
                "country": country,
                "experience_levels": {"$in": explist},
                "$or": [
                    {"city": city},
                    {"remote": True}
                ],
                "workplace_type": {"$in": workplace}  # Optional filtering
            }

            jobs_data = jobss.find(query)

            for job in jobs_data:
                job_description = job.get("about_this_job", "")
                job_embedding = model.encode(job_description, convert_to_tensor=True)
                similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).squeeze().item()
                matched_skills = find_matched_skills(job_description, resume_keywords)

                total_processed.append({
                    "job_title": job.get("job_searched", ""),
                    "userid": user_id,
                    "link": job.get("job_link", ""),
                    "similarity_score": similarity_score,
                    "matched_skills": matched_skills,
                })

        if not total_processed:
            return "No jobs matched the criteria."

        processed_jobs.insert_many(total_processed)
        return f"✅ {len(total_processed)} jobs processed and inserted successfully Now please send email with top 10 matches.."

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"


process_jobs_tool = Tool(
    name="Process Jobs",
    func=process_jobs,
    description=(
        "Processes and ranks jobs for a user based on similarity with their profile.\n\n"
        "**Input Format:** A string (json) with the following keys:\n"
        "- 'user_id': string (user email or ID)\n"
        "- 'job_titles': list of job titles (e.g., ['Web Developer', 'Data Scientist'])\n"
        "- 'city': string (e.g., 'Lahore')\n"
        "- 'country': string (e.g., 'Pakistan')\n"
        "- 'experience_list': list of experience levels (e.g., ['Internship', 'Entry Level'])\n"
        "- 'workplace_type': list of workplace types (e.g., ['Remote', 'On-site'])"
    )
)
