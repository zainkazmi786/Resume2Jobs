import re
import json
# Sample job descriptions
# with open("jobs.json", "r", encoding="utf-8") as f:
#     job_descriptions = json.load(f)
# job_descriptions = [
#     {
#         "description": "micro1\nShare\nShow more options\nFrontend Developer\nAPAC · 5 hours ago · Over 100 people clicked apply\n Remote\nMatches your job preferences, workplace type is Remote.\nContract\nApply\nSave\nSave Frontend Developer at micro1\nHow your profile and resume fit this job\nGet AI-powered advice on this job and more exclusive features with Premium. Try Premium for PKR0\nTailor my resume to this job\nAm I a good fit for this job?\nHow can I best position myself for this job?\nAbout the job\nJob Title: Frontend Developer\n\nJob Type: Full-time, Contractor\n\nAbout Us:\nOur mission at micro1 is to match the most talented people in the world with their dream jobs. If you are looking to be at the forefront of AI innovation and work with some of the fastest-growing companies in Silicon Valley, we invite you to apply for a role. By joining the micro1 community, your resume will become visible to top industry leaders, unlocking access to the best career opportunities on the market.\n\nJob Summary:\nWe are seeking a talented Frontend Developer to join our dynamic team. As a mid-level engineer, you'll leverage modern technologies such as React, Remix, Typescript, Supabase, and Vercel alongside cutting-edge AI tools to enhance development efficiency. This role offers a flexible and remote work environment we are open to applicants from around the globe.\n\nKey Responsibilities:\nDevelop and maintain scalable frontend applications using React.\nIntegrate Supabase for seamless backend connectivity.\nDeploy and manage applications on Vercel.\nUtilize AI tools to automate and optimize coding processes.\nCollaborate with cross-functional teams to define, design, and ship new features.\nEnsure the technical feasibility of UI/UX designs.\nWrite efficient, clean, and reusable code.\n\nRequired Skills and Qualifications:\nProficient in React for building user interfaces.\nExperience with Supabase for backend services.\nExperience with Remix framework.\nProficient in Typescript language.\nFamiliarity with Vercel for deployment and scaling.\nProficient with AI tools to boost development speed.\nStrong communication skills, both written and verbal.\nAbility to work autonomously in a remote setting.\nMinimum 2-4 years of relevant experience in front-end development.\n\nPreferred Qualifications:\nBased in LATAM region.\nPrior experience in a remote work environment.\nDemonstrated ability to implement AI-driven solutions in development workflows."
#     },
#     {
#         "description": "Flexing It®\nShare\nShow more options\nFreelance Full Stack Developer (Client Hire)\nAPAC · 5 days ago · Over 100 people clicked apply\n Remote\nMatches your job preferences, workplace type is Remote.\n Part-time\nMatches your job preferences, job type is Part-time.\n1 of 10 skills match: REST APIs\n1 of 10 required skills are found on your profile\nApply\nSave\nSave Freelance Full Stack Developer (Client Hire) at Flexing It®\nHow your profile and resume fit this job\nGet AI-powered advice on this job and more exclusive features with Premium. Try Premium for PKR0\nTailor my resume to this job\nAm I a good fit for this job?\nHow can I best position myself for this job?\nAbout the job\nFlexing It is a Freelance consulting marketplace that connects Freelancers and independent Consultants with organisations that are seeking independent talent.\n\nFlexing It has partnered with Our Client, an ESG Business Consulting Firm, is looking to engage with a Consultant - Web Development.\n\nKey Responsibilities\n(a) UI development using React.js, with the ability to develop visualisation/reports using Chart.js/D3.js etc.;\n(b) Backend development using Node.js to create RESTful APIs/services for the view;\n(c) Adept in MVC.\n(d) Collaborate with remote teams, adapt to changing requirements, and propose solutions.\n\nSkills Required\nStrong skills in React.js, Node.js, and MVC.\nExperience with data visualization tools like Chart.js/D3.js.\nProactive, good communication, and problem-solving abilities.\n3-5 years of Experience is required.\n\nCapacity - Full-time/Part-time Work Nature - Remote\nLoading job details"
#     }
# ]

def extract_job_fields(description):
    fields = {
        "job_title": None,
        # "location": None,
        "working_time": None,
        "posting_time": None,
        "remote" : None,
        "about_this_job": None,
        "experience_required": None
    }

    # Extract job title (specific to "Show more options\n" followed by the title)
    job_title_match = re.search(r"Show more options\n([^\n]+)", description)
    if job_title_match:
        fields["job_searched"] = job_title_match.group(1).strip()

    # Extract location (dynamic approach)
    # Look for patterns like "Location:", "Based in:", or text between job title and posting time
    # location_match = re.search(r"Show more options\n[^\n]+\n([^\n·]+)", description)
    # if location_match:
    #     fields["location"] = location_match.group(1).strip()
    # if location_match:
    #     # Use the first non-None group (either from "Location:" or the dynamic match)
    #     fields["location"] = next((group for group in location_match.groups() if group), "").strip()

    # Extract working time (e.g., Full-time, Part-time, Contract)
    working_time_match = re.search(r"Full-time|Part-time|Contract", description)
    if working_time_match:
        fields["working_time"] = working_time_match.group(0).strip()

    remote_match = re.search(r"Remote", description, re.IGNORECASE)  
    if remote_match:  
        fields["remote"] = True  
    else:  
        fields["remote"] = False  


    # Extract posting time (e.g., 5 hours ago, 5 days ago)
    posting_time_match = re.search(r"\d+\s+(hours|days|weeks|months)\s+ago", description)
    if posting_time_match:
        fields["posting_time"] = posting_time_match.group(0).strip()

    about_job_match = re.search(r"About the job[\s\S]*?(?=About the company|$)", description)
    if about_job_match:
        about_job_text = about_job_match.group(0).strip()
        about_job_text = re.sub(r"About the job\s*", "", about_job_text)  # Remove "About the job" heading
        about_job_text = re.sub(r"\n+", " ", about_job_text)  # Replace multiple newlines with a single space
        fields["about_this_job"] = about_job_text.strip()

    
    experience_sentence_match = re.search(r"([^.]*?\bexperience\b[^.]*)", about_job_text.strip(), re.IGNORECASE)

    if experience_sentence_match:
        experience_sentence = experience_sentence_match.group(0).strip()

        # ✅ Step 1: Prioritize extracting numbers with '+' (e.g., "2+ years")
        plus_experience_match = re.search(r"(\d+\+\s*(?:years?|months?))", experience_sentence, re.IGNORECASE)

        if plus_experience_match:
            fields["experience_required"] = plus_experience_match.group(0).strip()
        else:
            # ✅ Step 2: If no "+" is found, use existing extraction logic
            experience_match = re.search(r"(\d+\s*[\+\-]?\s*\d*\s*(?:years?|months?))", experience_sentence, re.IGNORECASE)

            if experience_match:
                fields["experience_required"] = experience_match.group(0).strip()
            else:
                fields["experience_required"] = None
    else:
        fields["experience_required"] = None

    return fields

# List to store all extracted job fields
# refined_data = []

# # Process each job description
# for job in job_descriptions:
#     description = job["description"]
#     fields = extract_job_fields(description)
#     refined_data.append(fields)

# Write the refined data to a JSON file
# with open("refineddata.json", "w", encoding="utf-8") as json_file:
#     json.dump(refined_data, json_file, indent=4, ensure_ascii=False)

# print("Data has been written to refineddata.json")


