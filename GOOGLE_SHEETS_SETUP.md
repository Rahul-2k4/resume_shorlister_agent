# 📊 Google Sheets Integration Setup Guide

## ✅ What's New

Candidates who **score 50 or above** are now automatically saved to Google Sheets!

## 🎯 Features

- ✅ **Automatic Data Storage** - Qualified candidates saved to Google Sheets
- ✅ **Complete Information** - Name, email, scores, skills, feedback
- ✅ **Timestamp** - When the candidate was evaluated
- ✅ **Easy to Review** - All data in one spreadsheet

## 📋 What Gets Saved

For candidates with **Final Score ≥ 50**:

| Column | Data |
|--------|------|
| Timestamp | When evaluated |
| Name | Candidate's full name |
| Email | Candidate's email |
| Final Score | Overall score (0-100) |
| Skill Score | Skills match score |
| Experience Score | Experience match score |
| Education Score | Education match score |
| Experience | Years of experience |
| Education | Degree/qualification |
| Candidate Skills | List of all skills |
| Feedback | AI-generated feedback |

## 🔐 Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"**
3. Name it: **"Resume Screening"**
4. Click **"Create"**

### Step 2: Enable Google Sheets API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google Sheets API"**
3. Click on it and click **"Enable"**
4. Also enable **"Google Drive API"** (same process)

### Step 3: Create Service Account

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Service account name: **"resume-screening-bot"**
4. Click **"Create and Continue"**
5. Role: Select **"Editor"**
6. Click **"Continue"** → **"Done"**

### Step 4: Download Credentials JSON

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"**
4. Choose **JSON** format
5. Click **"Create"**
6. A JSON file will be downloaded (e.g., `resume-screening-xxxxx.json`)
7. **Save this file** to your project folder as **`credentials.json`**

### Step 5: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Click **"Blank"** to create a new spreadsheet
3. Name it: **"Resume Screening Results"**
4. **IMPORTANT:** Copy the **sheet URL** (you'll need it)
5. Click **"Share"** button
6. **Paste the service account email** (from the JSON file, looks like: `resume-screening-bot@xxxx.iam.gserviceaccount.com`)
7. Give it **"Editor"** permission
8. Click **"Send"**

### Step 6: Update .env File

Add these lines to your `.env` file:

```env
# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Resume Screening Results
```

**Your complete .env should look like:**

```env
GOOGLE_API_KEY=AIzaSyDJDBuLKgvGHum49Ng8BB5PO313lw50r3M

GMAIL_EMAIL=rahultripathi2k4151@gmail.com
GMAIL_APP_PASSWORD=wnxuepwgsauvcjst

GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Resume Screening Results
```

## 📁 File Structure

Your project should have:

```
citybank/
├── app.py
├── .env
├── credentials.json          ← Google Service Account credentials (NEW!)
├── requirements.txt
└── ...
```

## 🚀 Testing

1. **Make sure credentials.json is in the project folder**
2. **Restart the server** (it will auto-reload)
3. **Upload a resume** that will score ≥ 50
4. **Check the terminal** for:
   ```
   ✅ Candidate data saved to Google Sheets: John Doe
   ```
5. **Open your Google Sheet** - the data should be there!

## 🔍 Troubleshooting

### ❌ "Credentials file not found"

**Problem:** `credentials.json` is missing

**Solution:**
- Download the JSON file from Google Cloud Console
- Save it in the same folder as `app.py`
- Make sure it's named exactly `credentials.json`

### ❌ "Spreadsheet not found"

**Problem:** Sheet name doesn't match or not shared

**Solution:**
1. Check the sheet name in Google Sheets (top-left)
2. Make sure it matches the name in `.env`
3. **Share the sheet** with the service account email

### ❌ "Permission denied"

**Problem:** Service account doesn't have access

**Solution:**
1. Open the Google Sheet
2. Click **"Share"**
3. Add the service account email (from `credentials.json`)
4. Give it **"Editor"** permission

### ❌ "API not enabled"

**Problem:** Google Sheets API is not enabled

**Solution:**
1. Go to Google Cloud Console
2. Navigate to **"APIs & Services"** → **"Library"**
3. Enable both:
   - Google Sheets API
   - Google Drive API

## 📊 Example Google Sheet

After running, your sheet will look like:

| Timestamp | Name | Email | Final Score | Skill Score | Experience Score | Education Score | Experience | Education | Candidate Skills | Feedback |
|-----------|------|-------|-------------|-------------|------------------|-----------------|------------|-----------|------------------|----------|
| 2025-10-06 15:30:00 | John Doe | john@example.com | 85 | 90 | 75 | 80 | 3 years | Bachelor's | Python, ML, SQL | Strong candidate... |
| 2025-10-06 16:00:00 | Jane Smith | jane@example.com | 92 | 95 | 85 | 90 | 5 years | Master's | Python, React, AWS | Excellent match... |

## 🎯 Workflow Summary

```
Resume Upload
    ↓
AI Extraction (name, email, skills, etc.)
    ↓
AI Evaluation & Scoring
    ↓
Check Score
    ├─ Score ≥ 50
    │   ├─ Send Offer Email ✅
    │   └─ Save to Google Sheets 📊  ← NEW!
    │
    └─ Score < 50
        └─ Send Rejection Email ❌
```

## ⚙️ Configuration Options

In `.env`, you can customize:

```env
# Sheet name (must match exact name in Google Sheets)
GOOGLE_SHEET_NAME=Resume Screening Results

# Credentials file path (relative to app.py)
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json

# Or use absolute path:
# GOOGLE_SHEETS_CREDENTIALS_FILE=C:/Users/rahul/Desktop/credentials.json
```

## 📈 Benefits

1. **Centralized Database** - All qualified candidates in one place
2. **Easy Sharing** - Share sheet with HR team
3. **Filter & Sort** - Use Google Sheets features
4. **Export** - Download as CSV/Excel anytime
5. **Charts** - Create visualizations of candidate scores
6. **No Code** - HR can view without technical knowledge

## 🔒 Security Notes

- ⚠️ **NEVER commit `credentials.json` to GitHub**
- ⚠️ `.gitignore` should include `credentials.json`
- ⚠️ Keep your service account key secure
- ✅ Only share sheet with necessary people
- ✅ Service account has limited permissions

---

**Ready to test!** Follow the setup steps and upload a resume with score ≥ 50! 🎉
