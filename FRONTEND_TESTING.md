# Frontend Testing Guide

## ✅ Backend Status
Backend is running on: http://127.0.0.1:8002
API Docs: http://127.0.0.1:8002/docs

## 🎯 How to Test Frontend

### Option 1: Open Directly in Browser
```
1. Navigate to: c:\Users\rahul\OneDrive\Desktop\citybank\frontend\index.html
2. Right-click → "Open with" → Your browser (Chrome/Edge/Firefox)
```

### Option 2: Use Live Server (Recommended)
If you have VS Code Live Server extension:
```
1. Right-click on frontend/index.html in VS Code
2. Select "Open with Live Server"
```

### Option 3: Python HTTP Server
```powershell
cd c:\Users\rahul\OneDrive\Desktop\citybank\frontend
python -m http.server 8080
# Then open: http://localhost:8080
```

## 🔍 Troubleshooting

### If Upload Doesn't Work:

1. **Check Backend is Running**
   - Open http://127.0.0.1:8002/ in browser
   - Should see: `{"message":"AI-Powered Resume Screening API is running!"...}`

2. **Check Browser Console (F12)**
   - Look for these logs:
     - 🚀 `runWorkflow called`
     - 📤 `Sending request to: http://127.0.0.1:8002/upload_resume`
     - 📥 `Response status: 200`
   - If you see errors, note them down

3. **Check CORS Errors**
   - If you see: "CORS policy blocked"
   - Solution: Use test_upload.html or serve frontend via HTTP server

4. **Test with Simple Upload**
   - Open: `c:\Users\rahul\OneDrive\Desktop\citybank\test_upload.html`
   - This confirms backend is working

## 🎨 What Should Happen

When you upload a resume:
1. ✅ Progress bar animates 0% → 100%
2. ✅ Timeline shows: Upload → Extract → Score → Email → Sheets
3. ✅ Activity log updates in real-time
4. ✅ Final score displays with PASS/REVIEW badge
5. ✅ Charts show skills/experience/education scores
6. ✅ Toast notification: "Processing completed successfully!"

## 📝 Sample Resumes
Use files from: `backend/uploads/` folder

## 🐛 Common Issues

### "Failed to fetch"
- Backend not running → Check terminal window
- Wrong URL → Verify API_BASE_URL in console

### "No file selected"
- Click "Upload Resume" button first
- Select a PDF file
- Then click "Start processing"

### Backend shuts down
- Don't run commands in same terminal as backend
- Backend runs in separate PowerShell window

## ✉️ Email Testing
- Emails sent to: candidate email (if found) or HR fallback
- Check your inbox for: "🎉 Congratulations" or "Thank You for Your Application"

## 📊 Google Sheets
- If score >= 50, data is logged to Google Sheets
- Check your "Resume Screening Results" sheet
