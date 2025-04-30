import pdfplumber
import json 
from groq import Groq
import re
from datetime import datetime
import os
from langchain.tools import Tool
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import user ,ENV_PATH


def load_env():

    load_dotenv(ENV_PATH)
    api_key = os.getenv("GROK_API_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    # print(f"Loaded API Key: {api_key}")  # Debugging

    if not api_key:
        raise ValueError("❌ ERROR: GROQ API Key is missing. Ensure it is set in the .env file at the root folder.")
    if not mongo_uri:
        raise ValueError("❌ ERROR: MongoDB URI is missing. Ensure it is set in the .env file.")
    
    return mongo_uri


def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ ERROR: Failed to extract text from PDF → {e}")
        return ""

def get_optimized_keywords(text):
    """Extracts keywords, job titles, email, experience level, and total years of experience from a resume."""
    try:
        client = Groq(api_key=os.getenv("GROK_API_KEY"))
        prompt_template = """You are an expert in resume parsing and job matching. Extract the relevant keywords from the given resume text for efficient cosine similarity matching with job descriptions.

        ### **Instructions:**
        - **Extract **name** from resume 
        - **Extract **all relevant skills, soft skills, tools, technologies, methodologies, certifications, key competencies, job roles, industries, qualifications, and work-related terminologies** across all domains.
        - **Flatten project technologies into the skills list** (e.g., "React" and all the skills from "E-commerce Project").
        - **Remove unnecessary achievements ** unless directly job-relevant.
        - **Ensure the output is compact** to maximize matching efficiency.
        - **Ensure JSON output remains valid and well-structured.**
        - **also extract the email from the text**
        - **extract the total experience in years from the text (experience includes jobs or internships) calculate based on the time metioned in resume**
        - **Extract 1-3 most relevant and specific job titles from the resume that are likely to be found on linkedin and are relevant to the text (the person is likely to as those job titles) **  
        - **Extract the experience level of the person from the text (internship, entry level, associate, mid-senior level, director, executive) it can be more than 1 **
        - **Extract the loction**  "city , country"--

        - **Ensure the output is strictly valid JSON without any comments, extra text, or trailing commas.**



        ### Resume Text:
        {text}

        ### **Output Format (JSON)**
        json
        {   "name" : "abc"
            "keywords": [
                "Python", "JavaScript", "React", "Flask", "MongoDB", "MySQL", 
                "Machine Learning", "API Development", "Full-Stack Developer", 
                "Data Analyst", "AI Engineer", "E-commerce", "Password Manager",
                "Node.js", "Express"
            ],
            "email" : "123@gmail.com",
            "total_experience_in_years" : 1.0 ",
            "job_titles" : ["Web Developer", "Data Analyst", "Machine Learning Engineer"]
            experience_level :
            [
                "Internship"
                "Entry Level",
                "Associate",
                "Mid-Senior Level",
                "Director",
                "Executive"
            ],
            city : "Abbottabad" , 
            country  : "Pakistan",
            
        }
        """
        
         
        prompt = prompt_template.replace("{text}", text[:15000])
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",  # or "mixtral-8x7b-32768"
            messages=[
                {"role": "system", "content": "You are an expert assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        # Get the response content (it's already a string)
        response = chat_completion.choices[0].message.content.strip()
        
        # Extracting JSON from the response using regex directly on the string
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        
        if json_match:
            extracted_data = json.loads(json_match.group())  # Convert the JSON string to a dictionary
            return extracted_data
        else:
            raise ValueError("JSON not found in API response.")
    except json.JSONDecodeError:
        print("❌ ERROR: Invalid JSON format in response.")
        return {"keywords": []}
    except Exception as e:
        print(f"❌ ERROR: Failed to extract keywords → {e}")
        return {"keywords": []}

def insert_into_db(data):
    """Inserts extracted resume data into MongoDB."""
    try:
        data["created_At"] = str(datetime.utcnow().isoformat())
        print("📥 Inserting into DB:", data)
        result = user.insert_one(data)
        print(f"✅ Data inserted successfully with ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ ERROR: Failed to insert data into MongoDB → {repr(e)}")

def process_resume(path : str):
    load_env()
    pdf_path = path.strip().replace('"', '').replace("'", "")

    """Extracts resume details and inserts into the database."""
    text = extract_text_from_pdf(pdf_path)
    if text:
        extracted_data = get_optimized_keywords(text)
        print(extracted_data)
        
        # Define required fields
        required_fields = [
            "name",
            "email",
            "job_titles",  # must be a list
            "city",
            "country",
            "experience_level",  # must be a list
            "total_experience_in_years",
            "keywords"  # must be a list
        ]
        
        # Find missing or empty fields
        missing_fields = [
            field for field in required_fields 
            if field not in extracted_data or not extracted_data[field]
        ]
        print("❗Missing fields:", missing_fields)  # Add this line

        # If any required field is missing, return an error message
        # if missing_fields:
        #     tool_name = "resume_extraction_tool"
        #     error_msg = (
        #         f"The tool `{tool_name}` did not return the following required field(s): "
        #         + ", ".join(missing_fields)
        #         + ". Please provide the missing information."
        #     )
        #     # You may choose to log or prompt the user at this point
        #     return {"error": error_msg}
        print("inserting")
        insert_into_db(extracted_data)
        return extracted_data

    return {"error": "Failed to extract text from resume."}


# ✅ Define LangChain Tool
resume_extraction_tool = Tool(
    name="extractprofile",
    func=process_resume,
    description=(
        "Use this tool FIRST to extract structured resume data from a PDF file. "
        "It returns the user's name, email, city, country, total experience, skills, keywords, "
        "job titles, and experience levels. All further steps depend on this output. "
        "Store results in MongoDB."
        "input is like this : \"./Resumes/cv1.pdf\""
    )
)

if __name__ == "__main__":
    pdf_path = "./Resumes/cv1.pdf"
    extracted_data = process_resume(pdf_path)
    # print(json.dumps(extracted_data, indent=4))
