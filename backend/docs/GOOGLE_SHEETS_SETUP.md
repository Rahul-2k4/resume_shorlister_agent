# 📊 Google Sheets Integration Setup Guide

## ✅ Overview

Any candidate whose final score is **50 or higher** is written automatically to a Google Sheet named **Resume Screening Results**.

## 🎯 What Gets Stored

| Column | Description |
| --- | --- |
| Timestamp | When the evaluation ran |
| Name | Candidate name |
| Email | Candidate email |
| Final Score | Overall score (0–100) |
| Skill Score | Skills sub-score |
| Experience Score | Experience sub-score |
| Education Score | Education sub-score |
| Experience | Years or range extracted from the resume |
| Education | Highest degree |
| Candidate Skills | List of skills detected |
| Feedback | AI summary |

## 🔐 Configure Google Cloud

### 1. Create a Project

1. Visit <https://console.cloud.google.com/>.
2. Select **Create Project** and name it “Resume Screening”.

### 2. Enable APIs

1. Open **APIs & Services → Library**.
2. Enable both **Google Sheets API** and **Google Drive API**.

### 3. Create a Service Account

1. Navigate to **APIs & Services → Credentials**.
2. Click **Create Credentials → Service account**.
3. Name it `resume-screening-bot` and assign the **Editor** role.

### 4. Download the Credentials File

1. Open the service account details → **Keys** tab.
2. Choose **Add key → Create new key → JSON**.
3. Save the file as `credentials.json`.
4. Place it in `backend/config/credentials.json`.

### 5. Share the Google Sheet

1. Create a blank sheet at <https://sheets.google.com/>.
2. Name it **Resume Screening Results**.
3. Share the sheet with the service account email (looks like `resume-screening-bot@…gserviceaccount.com`).
4. Grant **Editor** access.

## ⚙️ Update Environment Variables

Add these keys to the root `.env` file:

```ini
GOOGLE_SHEETS_CREDENTIALS_FILE=backend/config/credentials.json
GOOGLE_SHEET_NAME=Resume Screening Results
```

A full example `.env`:

```ini
GOOGLE_API_KEY=your_google_api_key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
GOOGLE_SHEETS_CREDENTIALS_FILE=backend/config/credentials.json
GOOGLE_SHEET_NAME=Resume Screening Results
```

## 📁 Project Structure

```text
citybank/
├─ backend/
│  ├─ app.py
│  ├─ config/
│  │  ├─ credentials.json
│  │  └─ job_requirements.json
│  └─ requirements.txt
├─ frontend/
└─ .env
```

## 🚀 Test the Integration

1. Ensure `backend/config/credentials.json` exists.
2. Run `uvicorn backend.app:app --reload`.
3. Upload a resume that should score at least 50.
4. Watch the console for `✅ Candidate data saved to Google Sheets: ...`.
5. Open the Google Sheet and confirm a new row appears.

## 🔍 Troubleshooting

| Issue | Diagnosis | Fix |
| --- | --- | --- |
| Credentials file not found | Wrong path or file missing | Verify `GOOGLE_SHEETS_CREDENTIALS_FILE` path |
| Spreadsheet not found | Sheet name mismatch | Match `.env` name to the sheet title |
| Permission denied | Sheet not shared with service account | Share with service account email |
| API not enabled | Sheets/Drive API disabled | Enable both APIs in Google Cloud |

## 📈 Sample Rows

| Timestamp | Name | Email | Final Score | Skills | Experience | Education | Feedback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-10-06 15:30:00 | John Doe | john@example.com | 85 | 90 | 75 | 80 | Strong candidate... |
| 2025-10-06 16:00:00 | Jane Smith | jane@example.com | 92 | 95 | 85 | 90 | Excellent match... |

## 🔄 Workflow Snapshot

```text
Resume Upload → AI Extraction → AI Evaluation → Score Check →
  • Score ≥ 50 → Send positive email + append to Google Sheet
  • Score < 50 → Send rejection email
```

## 🔒 Security Notes

- Keep `credentials.json` out of version control; `.gitignore` already covers it.
- Limit sharing on the spreadsheet.
- Regenerate the key if the file leaks.

## ✅ Final Checklist

- [ ] Google Sheets and Drive APIs enabled.
- [ ] Service account JSON saved to `backend/config/`.
- [ ] Sheet shared with the service account.
- [ ] `.env` references the correct paths.
- [ ] Test upload writes to the sheet.
