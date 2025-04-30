=

# 🧠 RESUME2JOBS

This project automates the end-to-end workflow of parsing resumes, identifying missing job records in a database, scraping new jobs, and sending personalized job matches to users via email. It uses a LangChain agent, integrated with multiple tools and a database, to intelligently manage the process from input to recommendation.

---

## 🚀 Features

- 🔍 **Resume Parsing**: Automatically extracts structured data like name, email, job titles, skills, experience, etc.
- 🧠 **AI-Powered Workflow**: Uses LangChain + Groq (Qwen-2.5-32B) to orchestrate logic.
- 🗄️ **Database Integration**: Stores jobs, fields, users, and match records in MongoDB.
- 🌐 **Job Scraping**: Scrapes job listings dynamically using Selenium for missing combinations.
- ✉️ **Job Recommendations**: Sends top 10 job matches to the user's email.

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                                                 |
|---------------|----------------------------------------------------------------------------|
| **AI Agent**  | LangChain + Groq (Qwen 2.5-32B)                                            |
| **Backend**   | Python, Flask (tool wrappers)                                              |
| **Scraping**  | Selenium                                                                   |
| **Database**  | MongoDB                                                                    |
| **Resume Parsing** | Custom tool (PDF to structured JSON)                                  |
| **Emailing**  | SMTP / Email API                                                           |

---



## 📌 How It Works (Workflow)

1. **Resume Upload**  
   User uploads a resume (PDF).

2. **Resume Extraction**  
   Tool parses it to extract required fields:  
   `name`, `email`, `job_titles`, `city`, `country`, `experience_level`, `keywords`, `total_experience_in_years`.

3. **Job Record Check**  
   Checks the database for existing job records with relevant titles and experience levels.

4. **Scraping**  
   If job records are missing, uses Selenium to scrape from job portals and store them.

5. **Job Processing**  
   Matches job postings with the user profile.

6. **Emailing Matches**  
   Sends top 10 ranked jobs to the user's email.

---

## ✅ Requirements

- Python 3.8+
- MongoDB
- LangChain
- Groq API Access
- Flask
- Selenium

---

## 🔧 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/zainkazmi786/Resume2Jobs
cd Resume2Jobs
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**

```env
GROK_API_KEY=
MONGO_URI=
DATABASE_NAME=job_recommendation
USER_COLLECTION=user
JOBS_COLLECTION=jobs
PROCESSED_JOBS_COLLECTION=processed_jobs
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=
SENDER_PASSWORD=

```

4.
 **Run the Backend**

```bash
python backend/app.py
```
 **Run the Frontend**
In seperate terminal
```bash
cd frontend
npm run dev
```


## 📊 Database Collections

- `users` – Contains parsed resume data
- `jobs` – Scraped job data
- `processed_jobs` – Processed Jobs &


---

## 📌 Use Cases

- Automating job matching in hiring platforms  



---

## 🙌 Author

**Syed Muhammad Zain Raza Kazmi**  
[LinkedIn](https://www.linkedin.com/in/syed-m-zain-raza-kazmi-a323a7286/) • [Email](mailto:zainkazmi258@gmail.com)

