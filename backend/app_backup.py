# Backup copy of the FastAPI application kept for reference.
# This version mirrors the current implementation but is retained separately
# so changes can be compared easily when experimenting.

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException
import PyPDF2
import io
from dotenv import load_dotenv
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
CONFIG_DIR = BASE_DIR / "config"

load_dotenv(PROJECT_ROOT / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GOOGLE_SHEETS_CREDS_FILE = os.getenv(
    "GOOGLE_SHEETS_CREDENTIALS_FILE",
    str(CONFIG_DIR / "credentials.json"),
)
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Resume Screening Results")
JOB_REQUIREMENTS_FILE = os.getenv(
    "JOB_REQUIREMENTS_FILE",
    str(CONFIG_DIR / "job_requirements.json"),
)

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
    print("⚠️ Warning: Gmail credentials not configured. Email notifications will be disabled.")

app = FastAPI(title="AI-Powered Resume Screening (Backup)")


def load_job_requirements() -> dict:
    try:
        with open(JOB_REQUIREMENTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Job requirements file not found: {JOB_REQUIREMENTS_FILE}. Please create the file.",
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in job requirements file: {e}",
        )


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {e}")


def clean_json_response(response_text: str) -> dict:
    try:
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON from AI response.")


def send_email(to_email: str, subject: str, body: str) -> bool:
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("⚠️ Email not sent: Gmail credentials not configured")
        return False

    msg = MIMEMultipart()
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    smtp_configs = [
        ('smtp.gmail.com', 587, False, 'TLS on port 587'),
        ('smtp.gmail.com', 465, True, 'SSL on port 465'),
        ('smtp.gmail.com', 25, False, 'TLS on port 25'),
    ]

    for host, port, use_ssl, description in smtp_configs:
        try:
            print(f"🔄 Trying {description}...")

            if use_ssl:
                server = smtplib.SMTP_SSL(host, port, timeout=10)
            else:
                server = smtplib.SMTP(host, port, timeout=10)
                server.starttls()

            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_EMAIL, to_email, text)
            server.quit()

            print(f"✅ Email sent successfully to {to_email} using {description}")
            return True

        except Exception as e:
            print(f"❌ Failed with {description}: {e}")
            continue

    print("❌ All SMTP methods failed. Possible causes:")
    print("   - Firewall blocking outgoing SMTP connections")
    print("   - Antivirus blocking email")
    print("   - Corporate network restrictions")
    print("   - ISP blocking SMTP ports")
    return False


def save_to_google_sheets(candidate_data: dict) -> bool:
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS_FILE, scope)
        client = gspread.authorize(creds)

        try:
            sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        except gspread.SpreadsheetNotFound:
            print(f"⚠️ Spreadsheet '{GOOGLE_SHEET_NAME}' not found. Please create it first or share it with the service account.")
            return False

        if sheet.row_count == 0 or sheet.row_values(1) == []:
            headers = [
                'Timestamp', 'Name', 'Email', 'Final Score',
                'Skill Score', 'Experience Score', 'Education Score',
                'Experience', 'Education', 'Candidate Skills', 'Feedback'
            ]
            sheet.insert_row(headers, 1)

        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            candidate_data.get('name', 'N/A'),
            candidate_data.get('email', 'N/A'),
            candidate_data.get('finalScore', 0),
            candidate_data.get('skillScore', 0),
            candidate_data.get('experienceScore', 0),
            candidate_data.get('educationScore', 0),
            candidate_data.get('experience', 'N/A'),
            candidate_data.get('education', 'N/A'),
            ', '.join(candidate_data.get('candidateSkills', [])) if isinstance(candidate_data.get('candidateSkills'), list) else candidate_data.get('candidateSkills', 'N/A'),
            candidate_data.get('feedback', 'N/A')
        ]

        sheet.append_row(row)

        print(f"✅ Candidate data saved to Google Sheets: {candidate_data.get('name')}")
        return True

    except FileNotFoundError:
        print(f"❌ Credentials file not found: {GOOGLE_SHEETS_CREDS_FILE}")
        print("   Please download your Google Service Account credentials JSON file")
        return False
    except Exception as e:
        print(f"❌ Failed to save to Google Sheets: {e}")
        return False


async def extract_structured_data(resume_text: str) -> dict:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
    prompt = f"""
    Resume Text:
    {resume_text}

    You are a Resume Screening Assistant. Your task is to analyze the candidate's resume text and extract structured information only from the content of the resume. Do not invent or add any information.

    Return a clean JSON object in this format:
    {{
      "name": "Exact name from resume",
      "email": "candidate's email address",
      "candidateSkills": ["list", "of", "skills"],
      "experience": "Number of years or range",
      "education": "Highest degree or education"
    }}

    Instructions:
    1. Always use the exact name as written in the resume.
    2. Extract the email address from the resume (e.g., "john.doe@gmail.com", "candidate@example.com").
    3. Extract all skills mentioned in the resume and list them under "candidateSkills".
    4. Estimate experience from the text (e.g., "3 years", "6+ years").
    5. Identify the highest education level or degree mentioned.
    6. **Do not wrap the JSON in markdown or code blocks. Return only the JSON object itself.**
    7. If a field is missing, use "Not found" or an empty array.
    """
    try:
        response = await model.generate_content_async(prompt)
        return clean_json_response(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error during data extraction: {e}")


async def evaluate_candidate(candidate_data: dict) -> dict:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')

    job_reqs = load_job_requirements()

    candidate_context = json.dumps(candidate_data, indent=2)
    job_context = json.dumps({
        "job_title": job_reqs.get("job_title", "Software Developer"),
        "requiredSkills": job_reqs.get("required_skills", []) + job_reqs.get("preferred_skills", []),
        "requiredExperience": f"{job_reqs.get('minimum_experience_years', 2)} years",
        "requiredEducation": job_reqs.get("required_education", "Bachelor's Degree")
    }, indent=2)

    prompt = f"""
    You are an AI Resume Evaluation Agent.
    Your task is to compare a candidate’s extracted resume data with the hardcoded job requirements below and return a structured JSON evaluation with a detailed and accurate score.
    **Return JSON only, no backticks, no markdown. The output must be a valid, parsable JSON object.**

    This is the candidate's extracted data:
    {candidate_context}

    These are the job requirements:
    {job_context}

    Now, produce the final evaluation in this exact format:
    {{
      "name": "Full Name of Candidate",
      "email": "candidate's email address",
      "candidateSkills": ["skills from candidate"],
      "requiredSkills": ["skills required for job"],
      "matchedSkills": ["skills that overlap"],
      "missingSkills": ["required skills not found in candidateSkills"],
      "skillScore": 0,
      "experience": "Candidate experience",
      "experienceScore": 0,
      "education": "Candidate education",
      "educationScore": 0,
      "finalScore": 0,
      "feedback": "Brief summary of candidate’s suitability",
      "weights": {{
        "skills": 0.7,
        "experience": 0.2,
        "education": 0.1
      }}
    }}
    """
    try:
        response = await model.generate_content_async(prompt)
        return clean_json_response(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error during evaluation: {e}")


@app.get("/")
async def root():
    return {
        "message": "AI-Powered Resume Screening API (Backup) is running!",
        "endpoints": {
            "upload": "POST /upload_resume",
            "docs": "/docs"
        }
    }


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")

    file_bytes = await file.read()

    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the PDF. The file might be empty or image-based.")

    candidate_data = await extract_structured_data(resume_text)

    final_evaluation = await evaluate_candidate(candidate_data)

    candidate_name = final_evaluation.get('name', 'Candidate')
    candidate_email = final_evaluation.get('email', 'Not found')
    final_score = final_evaluation.get('finalScore', 0)
    skill_score = final_evaluation.get('skillScore', 0)
    experience_score = final_evaluation.get('experienceScore', 0)
    education_score = final_evaluation.get('educationScore', 0)
    feedback = final_evaluation.get('feedback', 'No feedback available')

    if candidate_email and candidate_email != 'Not found' and '@' in candidate_email:
        recipient_email = candidate_email
    else:
        recipient_email = "rahultripathi2k4151@gmail.com"

    if final_score >= 50:
        subject = "🎉 Congratulations - You're Moving Forward!"
        body = f"""Dear {candidate_name},

Congratulations! We're pleased to inform you that your application has been shortlisted.

📊 Your Evaluation Results:
• Final Score: {final_score}/100
• Skills Match: {skill_score}/100
• Experience Score: {experience_score}/100
• Education Score: {education_score}/100

💼 Feedback:
{feedback}

We'll be in touch soon with next steps!

Best regards,
Hiring Team"""
    else:
        subject = "Thank You for Your Application"
        body = f"""Dear {candidate_name},

Thank you for taking the time to apply for this position.

📊 Your Evaluation Results:
• Final Score: {final_score}/100
• Skills Match: {skill_score}/100
• Experience Score: {experience_score}/100
• Education Score: {education_score}/100

💼 Feedback:
{feedback}

While your profile doesn't match our current requirements, we encourage you to apply for future opportunities that better align with your skills.

We wish you the best in your job search!

Best regards,
Hiring Team"""

    email_sent = send_email(recipient_email, subject, body)

    final_evaluation['email_sent'] = email_sent
    final_evaluation['email_recipient'] = recipient_email if email_sent else None

    sheets_saved = False
    if final_score >= 50:
        sheets_saved = save_to_google_sheets(final_evaluation)
        final_evaluation['saved_to_sheets'] = sheets_saved

    return final_evaluation


# To run the app located in backend/:
#   uvicorn backend.app_backup:app --reload
