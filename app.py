import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Dict
import PyPDF2
import io
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Make sure to create a .env file and add your credentials
# GOOGLE_API_KEY="your_google_api_key_here"
# GMAIL_EMAIL="your_email@gmail.com"
# GMAIL_APP_PASSWORD="your_16_char_app_password"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
    print("⚠️ Warning: Gmail credentials not configured. Email notifications will be disabled.")

# Don't configure at startup - do it when needed to avoid hanging
# genai.configure(api_key=GOOGLE_API_KEY)

# --- FastAPI App Initialization ---
app = FastAPI(title="AI-Powered Resume Screening")


# --- Helper Functions ---
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file's bytes."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {e}")

def clean_json_response(response_text: str) -> dict:
    """Cleans and parses a JSON string from an LLM response."""
    try:
        # Remove markdown backticks and "json" identifier
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON from AI response.")


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using Gmail SMTP.
    Returns True if successful, False otherwise.
    Tries multiple ports and methods for better compatibility.
    """
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("⚠️ Email not sent: Gmail credentials not configured")
        return False
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    
    # Try different SMTP configurations
    smtp_configs = [
        # (host, port, use_ssl, description)
        ('smtp.gmail.com', 587, False, 'TLS on port 587'),
        ('smtp.gmail.com', 465, True, 'SSL on port 465'),
        ('smtp.gmail.com', 25, False, 'TLS on port 25'),
    ]
    
    for host, port, use_ssl, description in smtp_configs:
        try:
            print(f"🔄 Trying {description}...")
            
            if use_ssl:
                # Use SSL connection
                server = smtplib.SMTP_SSL(host, port, timeout=10)
            else:
                # Use TLS connection
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


# --- AI Interaction Functions ---
async def extract_structured_data(resume_text: str) -> dict:
    """
    Uses Gemini to extract structured information from the resume text.
    (Corresponds to the first AI step in the n8n workflow)
    """
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
    """
    Compares extracted resume data with job requirements to score the candidate.
    (Corresponds to the second AI step in the n8n workflow)
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    # The candidate data is passed in the prompt context
    candidate_context = json.dumps(candidate_data, indent=2)

    prompt = f"""
    You are an AI Resume Evaluation Agent.
    Your task is to compare a candidate’s extracted resume data with the hardcoded job requirements below and return a structured JSON evaluation with a detailed and accurate score.
    **Return JSON only, no backticks, no markdown. The output must be a valid, parsable JSON object.**

    This is the candidate's extracted data:
    {candidate_context}

    These are the job requirements:
    {{
      "requiredSkills": [
        "Python", "Machine Learning", "Data Analysis", "SQL", "JavaScript",
        "React.js", "HTML", "CSS", "Node.js", "Git", "Cloud Computing", "REST APIs"
      ],
      "requiredExperience": "2 years",
      "requiredEducation": "Bachelor’s Degree in Computer Science or equivalent"
    }}

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


# --- API Endpoints ---
@app.get("/")
async def root():
    return {
        "message": "AI-Powered Resume Screening API is running!",
        "endpoints": {
            "upload": "POST /upload_resume",
            "docs": "/docs"
        }
    }

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    This endpoint receives a resume, processes it through a multi-step AI workflow,
    returns a final evaluation score and feedback, and sends an email notification.
    """
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")

    file_bytes = await file.read()

    # --- Workflow Step 1: Extract text from PDF ---
    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the PDF. The file might be empty or image-based.")

    # --- Workflow Step 2: Extract structured data from text ---
    candidate_data = await extract_structured_data(resume_text)

    # --- Workflow Step 3: Evaluate candidate against job requirements ---
    final_evaluation = await evaluate_candidate(candidate_data)
    
    # --- Workflow Step 4: Send email notification based on score ---
    candidate_name = final_evaluation.get('name', 'Candidate')
    candidate_email = final_evaluation.get('email', 'Not found')
    final_score = final_evaluation.get('finalScore', 0)
    skill_score = final_evaluation.get('skillScore', 0)
    experience_score = final_evaluation.get('experienceScore', 0)
    education_score = final_evaluation.get('educationScore', 0)
    feedback = final_evaluation.get('feedback', 'No feedback available')
    
    # Email recipient - send to candidate if email found, otherwise to HR
    if candidate_email and candidate_email != 'Not found' and '@' in candidate_email:
        recipient_email = candidate_email  # Send to candidate
    else:
        recipient_email = "rahultripathi2k4151@gmail.com"  # Send to HR if no candidate email
    
    if final_score >= 50:
        # Send offer/shortlist email
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
        # Send rejection email
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
    
    # Send the email
    email_sent = send_email(recipient_email, subject, body)
    
    # Add email status to response
    final_evaluation['email_sent'] = email_sent
    final_evaluation['email_recipient'] = recipient_email if email_sent else None
    
    return final_evaluation

# To run the app:
# 1. Create a file named .env in the same directory.
# 2. Add your Google API key to it: GOOGLE_API_KEY="your_key_here"
# 3. Install requirements: pip install -r requirements.txt
# 4. Run uvicorn: uvicorn app:app --reload