# 📧 Email Connection Troubleshooting

## ❌ Symptom: Connection Timeout (WinError 10060)

This error means the machine could not reach Gmail's SMTP servers. Credentials are correct, but a firewall, antivirus, or network policy is blocking outbound traffic.

## 🔍 Common Causes and Fixes

### Windows Firewall

```powershell
# Run in an elevated PowerShell window
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*Python*" -or $_.DisplayName -like "*SMTP*" }
```

If Python is blocked:

1. Open **Windows Defender Firewall**.
2. Select **Allow an app through firewall**.
3. Click **Change settings** → **Allow another app**.
4. Browse to `C:\Users\rahul\OneDrive\Desktop\citybank\.venv\Scripts\python.exe`.
5. Enable both **Private** and **Public** networks.

### Antivirus Software

Vendors such as Norton, McAfee, Avast, AVG, and Kaspersky often block SMTP ports 465 and 587. Temporarily disable the shield and test. If the email works, add Python to the antivirus allow-list.

### Corporate or School Networks

Managed networks frequently block outbound SMTP traffic. A VPN or a personal connection may be required. Contact IT if you must use the corporate network.

### ISP Restrictions

Some ISPs block port 25 entirely. Ports 465 and 587 usually work, but verify using a mobile hotspot to rule out ISP filtering.

### Router or Modem Firewall

Check the router admin console for blocked SMTP ports. Temporarily disable the firewall to test, then re-enable it once finished.

## 🧪 Diagnostics

### Test Connectivity from PowerShell

```powershell
Test-NetConnection -ComputerName smtp.gmail.com -Port 587
```

Expect `TcpTestSucceeded : True`. Any `False` result indicates a blocked port.

### Try Multiple Ports

The backend now iterates through ports 587 (TLS), 465 (SSL), and 25 (TLS). Inspect the terminal log to see which port, if any, succeeds.

### Switch Networks

- Connect to a phone hotspot.
- Try a different Wi-Fi network.
- Test while connected to a VPN.

## 🚀 Quick Remediation Checklist

### Run Connectivity Tests

```powershell
Test-NetConnection smtp.gmail.com -Port 587
Test-NetConnection smtp.gmail.com -Port 465
Test-NetConnection smtp.gmail.com -Port 25
```

### Temporarily Disable Windows Defender

1. Open **Windows Security** → **Virus & threat protection**.
2. Select **Manage settings**.
3. Turn off **Real-time protection** briefly.
4. Re-run the email test.
5. Re-enable protection immediately after testing.

### Use a Mobile Hotspot

1. Enable hotspot on the phone.
2. Connect the PC to the hotspot.
3. Upload a resume.
4. If it succeeds, the original network is blocking SMTP.

### Inspect Proxy Settings

```powershell
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" | \
  Select-Object ProxyEnable, ProxyServer
```

If `ProxyEnable` equals 1, disable the proxy temporarily and test again.

## 🔧 What the Code Now Does

```text
🔄 Trying TLS on port 587...
❌ Failed with TLS on port 587: [WinError 10060]
🔄 Trying SSL on port 465...
✅ Email sent successfully using SSL on port 465
```

The console output identifies the configuration that works or fails, making debugging faster.

## 🌐 Consider HTTP Email APIs

If Gmail SMTP remains blocked, services such as **SendGrid** (100 emails/day) or **Mailgun** (5,000 emails/month) expose HTTP APIs that bypass SMTP ports entirely.

## ✅ Final Checklist

- [ ] Firewall allows `.venv\Scripts\python.exe`.
- [ ] Antivirus has a rule permitting SMTP traffic.
- [ ] Network/VPN allows outbound ports 25, 465, or 587.
- [ ] `Test-NetConnection` succeeds on at least one port.
- [ ] Mobile hotspot test confirms whether the ISP is the issue.
- [ ] Terminal log indicates which SMTP attempt succeeds.

## 🆘 Still Blocked?

1. Run the workflow from n8n, which may have different network permissions.
2. Switch to SendGrid or Mailgun for HTTP-based email delivery.
3. Temporarily disable email and store results in a JSON or CSV file until SMTP access is restored.
