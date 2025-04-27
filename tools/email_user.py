from langchain.tools import Tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import processed_jobs

def send_top_jobs_email(user_id: str) -> dict:
    """
    Fetch the top 10 jobs and send their job links to the user's email.

    :param user_id: The user's email ID (used both as DB key and recipient).
    :return: A status dictionary with success or error message.
    """
    # Fetch jobs
    query = {"userid": user_id}
    top_jobs = list(processed_jobs.find(query, {"_id": 0}).sort("similarity_score", -1).limit(10))

    if not top_jobs:
        return {"status": "failed", "reason": "No jobs found for user_id"}

    # Extract job links
    job_links = [job.get("link", "Link not found") for job in top_jobs]

    # Compose email
    email_body = "\n".join(f"{i+1}. {link}" for i, link in enumerate(job_links))

    subject = "Your Top 10 Job Matches 🚀"
    recipient = user_id  # Assuming user_id is the email

    # Email config (use environment variables for security)
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        return {"status": "failed", "reason": "Sender email credentials not found in env variables"}

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(email_body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()

        return {"status": "success", "message": f"Top job links sent to {recipient}"}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}

# LangChain-compatible tool
email_jobs_tool = Tool(
    name="Email Job Matches",
    func=send_top_jobs_email,
    description=(
        "Fetches the top 10 job matches from the database and emails their links to the user's email. "
        "Input should be the user's email address (user_id)."
    )
)

# For testing
if __name__ == "__main__":
    print(send_top_jobs_email("shahrizwan403@gmail.com"))
