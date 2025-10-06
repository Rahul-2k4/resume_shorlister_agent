# 📧 Gmail Email Setup Guide

## ✅ What's Been Added

Your FastAPI app now automatically sends emails after evaluating resumes:
- **Score ≥ 50**: Sends congratulations/offer letter email
- **Score < 50**: Sends rejection email with constructive feedback

## 🔐 Gmail App Password Setup (REQUIRED)

You **CANNOT** use your regular Gmail password. You need a special App Password.

### Step-by-Step Instructions:

1. **Enable 2-Factor Authentication** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Find "2-Step Verification" and turn it ON

2. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in with your Gmail account
   - Select app: **"Mail"**
   - Select device: **"Other (Custom name)"**
   - Name it: **"Resume Screening"**
   - Click **"Generate"**
   - Copy the **16-character password** (format: xxxx xxxx xxxx xxxx)

3. **Update .env file**:
   - Open `.env` in this folder
   - Replace `your_app_password_here` with the 16-character password
   - Remove all spaces from the password
   - Example: `GMAIL_APP_PASSWORD=abcdabcdabcdabcd`

## 📝 Your .env File Should Look Like:

```
GOOGLE_API_KEY=AIzaSyDJDBuLKgvGHum49Ng8BB5PO313lw50r3M

GMAIL_EMAIL=rahultripathi2k4151@gmail.com
GMAIL_APP_PASSWORD=abcdabcdabcdabcd
```

## 🚀 Testing the Email Feature

1. **Make sure your .env is updated** with the App Password

2. **The server will auto-reload** (it's watching for changes)

3. **Upload a resume** at http://127.0.0.1:8002/docs

4. **Check your email** at rahultripathi2k4151@gmail.com

5. **Check the terminal** for confirmation:
   - ✅ Email sent successfully to rahultripathi2k4151@gmail.com

## 🔍 Troubleshooting

### ❌ "Username and Password not accepted"
- You're using your regular Gmail password instead of App Password
- Create an App Password using the steps above

### ❌ "2-Step Verification required"
- Enable 2FA on your Google account first
- Then create the App Password

### ❌ "Email not sent: Gmail credentials not configured"
- Check that GMAIL_EMAIL and GMAIL_APP_PASSWORD are in .env
- Make sure there are no typos

### ✅ Email sent but not received
- Check your spam/junk folder
- Make sure the email address is correct
- Wait a few minutes (sometimes there's a delay)

## 📬 Email Content

### For Score ≥ 50 (Shortlisted):
```
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

### For Score < 50 (Not Selected):
```
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

## 🎯 Next Steps

1. Create your Gmail App Password
2. Update the .env file
3. Test by uploading a resume
4. Check your email!

---

**Current Email Recipient**: rahultripathi2k4151@gmail.com

To change the recipient, edit line 216 in `app.py`:
```python
recipient_email = "new_email@example.com"
```
