from langchain.tools import Tool
from config import jobss
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def check_job_records(input_data) -> list:
    try:
        if isinstance(input_data, str):
            input_dict = json.loads(input_data)
        else:
            input_dict = input_data
    except json.JSONDecodeError:
        return {"error": "Invalid input format. Must be a JSON string with proper keys."}


    job_titles = input_dict.get("job_titles", [])
    city = input_dict.get("city", "")
    country = input_dict.get("country", "")
    experience_list = input_dict.get("experience_list", [])
    workplace_type = input_dict.get("workplace_type", [])

    results = []

    for title in job_titles:
        job_title_exists = jobss.count_documents({"job_searched": title}) > 0
        if not job_title_exists:
            results.append({
                "job_title": title,
                "exists": False,
                "message": f"No records found for job title: {title}"
            })
            continue

        query = {
            "job_searched": title,
            "country": country,
            "$or": [
                {"city": city},
                {"remote": True}
            ],
            "experience_levels": {"$in": experience_list},
            "workplace_type": {"$in": workplace_type}
        }

        matching_jobs = list(jobss.find(query, {"experience_levels": 1, "_id": 0}))
        found_experience_levels = set()
        for job in matching_jobs:
            found_experience_levels.update(job.get("experience_levels", []))

        missing_experience_levels = set(experience_list) - found_experience_levels

        results.append({
            "job_title": title,
            "exists": True,
            "matching_experience_levels": list(found_experience_levels),
            "missing_experience_levels": list(missing_experience_levels),
            "total_matching_jobs": len(matching_jobs)
        })

    return results



check_jobs_tool = Tool(
    name="Check Job Records",
    func=check_job_records,
    description=(
        "Checks if job records exist in the database for a list of job_titles, city, country, "
        "experience_list, and workplace_type (Remote, On-site, Hybrid). "
        "Returns a list of results with details about matching and missing experience levels for each job title.\n\n"
        "**Input Format:** A STRING (json) with the following keys:\n"
        "- 'job_titles': list of job titles (e.g., ['AI Engineer', 'Web Developer'])\n"
        "- 'city': string (e.g., 'Haripur')\n"
        "- 'country': string (e.g., 'Pakistan')\n"
        "- 'experience_list': list of experience levels (e.g., ['Internship', 'Entry Level'])\n"
        "- 'workplace_type': list of workplace types (e.g., ['Remote', 'On-site', 'Hybrid'])"
        "This tool will loop through each job title and check if matching jobs exist in the database "
        "based on the given location, experience levels, and workplace types."
    )
)

