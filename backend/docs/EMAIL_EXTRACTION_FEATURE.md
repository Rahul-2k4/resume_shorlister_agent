# 📧 Email Extraction Feature Added

## ✅ What's New

The AI agent now **automatically extracts the candidate's email address** from their resume!

## 🎯 Changes Made

### Updated Extract Data Prompt

Added email extraction to the first AI prompt:

```json
{
  "name": "Exact name from resume",
  "email": "candidate's email address",  // ← NEW!
  "candidateSkills": ["list", "of", "skills"],
  "experience": "Number of years or range",
  "education": "Highest degree or education"
}
```

**New instruction added:**

> Extract the email address from the resume (for example, `john.doe@gmail.com`, `candidate@example.com`).

### Updated Evaluation Prompt

Added email to the evaluation output format:

```json
{
  "name": "Full Name of Candidate",
  "email": "candidate's email address",  // ← NEW!
  "candidateSkills": ["skills from candidate"],
  ...
}
```

### Smart Email Routing

Updated the email sending logic to intelligently choose the recipient:

```python
# Email recipient - send to candidate if email found, otherwise to HR
if candidate_email and candidate_email != 'Not found' and '@' in candidate_email:
    recipient_email = candidate_email  # Send to candidate
else:
    recipient_email = "rahultripathi2k4151@gmail.com"  # Send to HR if no candidate email
```

## 📋 How It Works Now

### Workflow

1. **Upload Resume** → PDF is processed.
2. **AI Extracts Data** → Including email address from resume.
3. **AI Evaluates Candidate** → Scores against job requirements.
4. **Smart Email Delivery**:
   - ✅ If email found in resume → Send to [candidate's email](mailto:john.doe@gmail.com).
   - ❌ If no email found → Send to [HR inbox](mailto:rahultripathi2k4151@gmail.com).

### Example Resume Text

```text
John Doe
john.doe@gmail.com
Phone: +1 234-567-8900

Skills: Python, Machine Learning, SQL
...
```

### Extracted Data

```json
{
  "name": "John Doe",
  "email": "john.doe@gmail.com",  // ← Automatically extracted!
  "candidateSkills": ["Python", "Machine Learning", "SQL"],
  "experience": "3 years",
  "education": "Bachelor's Degree in Computer Science"
}
```

### Email Sent To

- [john.doe@gmail.com](mailto:john.doe@gmail.com) ✅ (Candidate receives their evaluation directly.)

## 🎯 Benefits

1. **Automated Communication** – Candidates get instant feedback.
2. **No Manual Entry** – Email is extracted automatically from resume.
3. **Fallback to HR** – If no email found, HR gets notified instead.
4. **Professional Experience** – Candidates receive personalized emails with their scores.

## 🚀 Testing

Upload a resume that contains an email address like:

- `candidate@example.com`
- `john.doe@gmail.com`
- `firstname.lastname@company.com`

The AI will find and extract it automatically!

## 📝 API Response

The API response now includes the email:

```json
{
  "name": "John Doe",
  "email": "john.doe@gmail.com",
  "candidateSkills": [...],
  "finalScore": 85,
  "feedback": "...",
  "email_sent": true,
  "email_recipient": "john.doe@gmail.com"
}
```

---

**Ready to test!** Upload a resume with an email address and watch it work! 🎉
