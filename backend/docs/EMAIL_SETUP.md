# 📧 Gmail Email Setup Guide

## ✅ Overview

After each resume evaluation the FastAPI service can send a follow-up email. Messages differ depending on whether the candidate crosses the score threshold.

- Scores **50 or higher** trigger a congratulations email.
- Scores **below 50** trigger a polite rejection with feedback.

## 🔐 Generate a Gmail App Password

Google blocks regular passwords for SMTP connections. Create a one-time App Password and store it in the `.env` file.

### Step 1 · Enable Two-Factor Authentication

1. Open <https://myaccount.google.com/security>.
2. Turn on **2-Step Verification** (required before App Passwords are available).

### Step 2 · Create the App Password

1. Visit <https://myaccount.google.com/apppasswords>.
2. Sign in with your Gmail account.
3. Choose **Mail** as the app.
4. Choose **Other (Custom name)** as the device and name it "Resume Screening".
5. Click **Generate** and copy the 16-character code (format `xxxx xxxx xxxx xxxx`).

### Step 3 · Update the `.env` File

1. Open the `.env` file at the project root.
2. Remove spaces from the generated password and add it as shown below.

```ini
GOOGLE_API_KEY=AIzaSyDJDBuLKgvGHum49Ng8BB5PO313lw50r3M
GMAIL_EMAIL=rahultripathi2k4151@gmail.com
GMAIL_APP_PASSWORD=abcdabcdabcdabcd
```

## 🚀 Test Email Delivery

1. Confirm the `.env` file contains both `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD`.
2. Start the API with `uvicorn backend.app:app --reload`.
3. Upload a PDF resume via <http://127.0.0.1:8002/docs>.
4. Watch the terminal log for `✅ Email sent successfully ...`.
5. Check the inbox for `rahultripathi2k4151@gmail.com` (including the spam folder).

## 🔍 Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `Username and Password not accepted` | Using regular Gmail password | Create the App Password above |
| `2-Step Verification required` | 2FA not enabled | Enable 2FA, then generate the App Password |
| `Email not sent: Gmail credentials not configured` | Missing `.env` keys | Add `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` |
| Email sent but not received | Spam filtering or typos | Check spam, verify address, wait a few minutes |

## 📬 Email Templates

### Passing Candidates (Score ≥ 50)

```text
Subject: 🎉 Congratulations - You're Moving Forward!

Dear [Candidate Name],

Congratulations! We're pleased to inform you that your application has been shortlisted.

📊 Your Evaluation Results:
• Final Score: XX/100
• Skills Match: XX/100
• Experience Score: XX/100
• Education Score: XX/100

💼 Feedback:
[AI-generated feedback]

We'll be in touch soon with next steps!

Best regards,
Hiring Team
```

### Not Selected (Score < 50)

```text
Subject: Thank You for Your Application

Dear [Candidate Name],

Thank you for taking the time to apply for this position.

📊 Your Evaluation Results:
• Final Score: XX/100
• Skills Match: XX/100
• Experience Score: XX/100
• Education Score: XX/100

💼 Feedback:
[AI-generated feedback]

While your profile doesn't match our current requirements, we encourage you to apply for future opportunities that better align with your skills.

We wish you the best in your job search!

Best regards,
Hiring Team
```

## ✏️ Change the Default Recipient

The fallback sender is `rahultripathi2k4151@gmail.com`. Update the constant near the email routing logic in `backend/app.py` if needed:

```python
recipient_email = "new_email@example.com"
```

## ✅ Checklist

- [ ] Generate the Gmail App Password.
- [ ] Store it in `.env` without spaces.
- [ ] Restart `uvicorn` and upload a test resume.
- [ ] Confirm the email arrives.
