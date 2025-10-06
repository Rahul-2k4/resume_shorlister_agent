# 📧 Email Connection Troubleshooting

## ❌ Error: Connection Timeout (WinError 10060)

This means your computer **cannot connect** to Gmail's SMTP servers. This is NOT an authentication issue - your credentials are correct, but something is blocking the connection.

## 🔍 Common Causes & Solutions

### 1. **Windows Firewall** 🛡️

**Check if Windows Firewall is blocking:**

```powershell
# Run in PowerShell as Administrator:
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Python*" -or $_.DisplayName -like "*SMTP*"}
```

**Allow Python through firewall:**

1. Open **Windows Defender Firewall**
2. Click **"Allow an app through firewall"**
3. Click **"Change settings"** → **"Allow another app"**
4. Browse to: `C:\Users\rahul\OneDrive\Desktop\citybank\.venv\Scripts\python.exe`
5. Check **both Private and Public** networks
6. Click **OK**

### 2. **Antivirus Software** 🦠

Many antivirus programs block SMTP connections:

- **Norton, McAfee, Avast, AVG, Kaspersky** often block port 587/465
- **Temporarily disable** antivirus and test
- If it works, add Python to antivirus exceptions

### 3. **Corporate/School Network** 🏢

If you're on a work/school network:

- SMTP ports (25, 465, 587) are often **blocked**
- VPN might be required
- Contact IT department

### 4. **ISP Restrictions** 🌐

Some Internet Service Providers block SMTP:

- Jio, Airtel, etc. sometimes block port 25
- Ports 465 and 587 usually work
- Try using mobile hotspot to test

### 5. **Router/Modem Firewall** 🔒

- Login to your router settings
- Check if SMTP ports are blocked
- Temporarily disable router firewall to test

## 🧪 Testing Methods

### Method 1: Test with PowerShell

```powershell
Test-NetConnection -ComputerName smtp.gmail.com -Port 587
```

**Expected Result:**
```
TcpTestSucceeded : True
```

If it shows `False`, the port is blocked.

### Method 2: Try All Ports

The updated code now tries 3 different methods:
1. Port 587 with TLS (most common)
2. Port 465 with SSL (alternative)
3. Port 25 with TLS (backup)

Watch the terminal for which one works!

### Method 3: Test from Different Network

- **Mobile Hotspot**: Connect to phone's hotspot and test
- **Different WiFi**: Try from home if at work, or vice versa
- **VPN**: Use a VPN service

## 🚀 Quick Fixes to Try

### Fix 1: Run PowerShell as Administrator

```powershell
# Check if ports are reachable
Test-NetConnection smtp.gmail.com -Port 587
Test-NetConnection smtp.gmail.com -Port 465
Test-NetConnection smtp.gmail.com -Port 25
```

### Fix 2: Temporarily Disable Windows Defender

1. Open **Windows Security**
2. Go to **Virus & threat protection**
3. Manage settings
4. Turn off **Real-time protection** (temporarily)
5. Test the app
6. **Turn it back on!**

### Fix 3: Use Mobile Hotspot

This confirms if it's a network issue:
1. Enable mobile hotspot on your phone
2. Connect your PC to it
3. Test the resume upload
4. If it works → network/ISP is blocking

### Fix 4: Check Proxy Settings

```powershell
# Check if proxy is configured
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" | Select-Object ProxyEnable, ProxyServer
```

If ProxyEnable is 1, disable it temporarily.

## 🔧 Updated Code Features

The app now tries multiple SMTP methods automatically:

```
🔄 Trying TLS on port 587...
❌ Failed with TLS on port 587: [WinError 10060]
🔄 Trying SSL on port 465...
✅ Email sent successfully using SSL on port 465
```

Watch your terminal for which method succeeds!

## 📱 Alternative: Use SendGrid or Mailgun

If Gmail SMTP doesn't work at all, consider using these services:

### SendGrid (Free tier: 100 emails/day)
- No SMTP port needed
- Uses HTTP API
- Works on restricted networks

### Mailgun (Free tier: 5,000 emails/month)
- HTTP API
- Better for corporate environments

Would you like me to set up one of these alternatives?

## ✅ Success Checklist

- [ ] Windows Firewall allows Python
- [ ] Antivirus exceptions added
- [ ] Not on restricted corporate network
- [ ] Test-NetConnection shows `TcpTestSucceeded: True`
- [ ] Tried mobile hotspot
- [ ] Checked terminal for which port works

## 🆘 Still Not Working?

If none of the above works:

1. **Use the n8n workflow instead** - It might have different network permissions
2. **Set up SendGrid/Mailgun** - HTTP-based email services
3. **Save evaluations to file** - Skip email for now, save results to CSV/JSON

Let me know which solution you'd like to implement! 🚀
