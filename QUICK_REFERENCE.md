# Attendance Recording App - Quick Reference Guide

## 🚀 Quick Start (60 Seconds)

### 1️⃣ Set Environment Variables
```bash
# Windows (Command Prompt)
setx GMAIL_USER "your-email@gmail.com"
setx GMAIL_APP_PASSWORD "xxxx xxxx xxxx xxxx"

# macOS/Linux (Terminal)
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

### 2️⃣ Prepare Files
- ✅ `students.csv` - 64 students with emails
- ✅ `attendance.txt` - attendance records (one line per class)
- ✅ `attendance_app.py` - the main script

### 3️⃣ Run the Application
```bash
python attendance_app.py
```

### 4️⃣ Check Results
- 📊 `attendance_report.csv` - Summary table
- 📧 Emails sent to all students
- 📝 `attendance.log` - Execution details

---

## 📋 Pre-Flight Checklist

Before running the app, verify:

- [ ] Python 3.6+ installed (`python --version`)
- [ ] Gmail account created
- [ ] 2-Step Verification enabled on Gmail
- [ ] App Password generated from Gmail (16 characters)
- [ ] GMAIL_USER environment variable set
- [ ] GMAIL_APP_PASSWORD environment variable set
- [ ] `students.csv` in correct location with 64 students
- [ ] `attendance.txt` with attendance records (at least 1 line)
- [ ] Both input files have correct format

---

## 🔧 Verify Setup

### Check Python
```bash
python --version
# Expected: Python 3.6 or higher
```

### Check Environment Variables
```bash
# Windows
echo %GMAIL_USER%
echo %GMAIL_APP_PASSWORD%

# macOS/Linux
echo $GMAIL_USER
echo $GMAIL_APP_PASSWORD
```

Both should display values (not blank).

### Check Files
```bash
# Windows
dir students.csv attendance.txt

# macOS/Linux
ls students.csv attendance.txt
```

Both files must exist in the working directory.

---

## 📊 Input File Formats (Quick Reference)

### `students.csv`
```
Roll,Name,Email
1,Student Name,email@example.com
2,Another Student,email2@example.com
...
64,Last Student,email64@example.com
```

**Key Points**:
- Exactly 64 rows (plus header)
- Roll numbers 1-64
- Valid email addresses
- No empty cells

### `attendance.txt`
```
1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29
1,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30
2,4,5,7,9,11,13,15,17,19,21,23,25,27,28,29
```

**Key Points**:
- One line = one class
- Comma-separated roll numbers
- Numbers must be 1-64
- No headers needed

---

## 🔍 Common Commands

### Windows Command Prompt

```bash
# Navigate to folder
cd C:\Users\YourName\attendance_app

# Run the app
python attendance_app.py

# View the report
type attendance_report.csv

# View the log
type attendance.log

# Set environment variable (permanent)
setx GMAIL_USER "your-email@gmail.com"

# Set environment variable (this session only)
set GMAIL_USER=your-email@gmail.com
```

### macOS / Linux Terminal

```bash
# Navigate to folder
cd ~/attendance_app

# Run the app
python3 attendance_app.py

# View the report
cat attendance_report.csv

# View the log
cat attendance.log

# Set environment variable (this session)
export GMAIL_USER="your-email@gmail.com"

# Set permanent (add to ~/.bash_profile or ~/.zshrc)
echo 'export GMAIL_USER="your-email@gmail.com"' >> ~/.bash_profile
```

---

## ⚡ Common Issues & Solutions

### Issue 1: "File not found: students.csv"
```
❌ Error: FileNotFoundError: File not found: students.csv

✅ Solution:
   1. Make sure students.csv is in the same folder as attendance_app.py
   2. Check filename spelling exactly (case-sensitive on Mac/Linux)
   3. Make sure it's a .csv file, not .xlsx or .txt
```

### Issue 2: "Gmail credentials not found"
```
❌ Error: Gmail credentials not found in environment variables

✅ Solutions:
   Windows:
   - Open new Command Prompt (important!)
   - Run: setx GMAIL_USER "your-email@gmail.com"
   - Run: setx GMAIL_APP_PASSWORD "xxxx xxxx xxxx xxxx"
   - Close and reopen Command Prompt
   - Verify: echo %GMAIL_USER%

   Mac/Linux:
   - Run: source ~/.bash_profile
   - Verify: echo $GMAIL_USER
```

### Issue 3: "Gmail authentication failed"
```
❌ Error: Gmail authentication failed

✅ Solutions:
   1. Wrong App Password?
      - Go to: https://myaccount.google.com/apppasswords
      - Create a new one
      - Update GMAIL_APP_PASSWORD variable

   2. 2-Step Verification not enabled?
      - Go to: https://myaccount.google.com/security
      - Enable "2-Step Verification"
      - Then create App Password

   3. Using regular Gmail password instead of App Password?
      - App Password ≠ Gmail password
      - Must use the 16-character App Password
```

### Issue 4: "SMTP error while sending"
```
❌ Error: SMTP error while sending email

✅ Solutions:
   1. Internet connection working?
      - Check internet connection
      - Try accessing gmail.com in browser

   2. Gmail account locked?
      - Log in to Gmail manually
      - Accept any security prompts
      - Try running script again

   3. Too many emails sent?
      - Gmail rate limits: ~5-10 emails/second
      - Wait 5-10 minutes before trying again
```

### Issue 5: Emails not arriving in inbox
```
❌ Emails sent but not visible

✅ Solutions:
   1. Check spam/junk folder
      - Gmail often filters automated emails
      - Add sender to contacts to whitelist

   2. Verify email addresses in students.csv
      - Check for typos
      - Ensure valid format (user@domain.com)

   3. Check attendance.log for actual sent status
      - Open attendance.log
      - Search for student name
      - Verify "Email sent successfully" message
```

---

## 📈 Performance Tips

### Speed Up Email Sending
- Gmail rate limit: ~5-10 emails/second
- For 64 students: ~8-13 seconds minimum
- If slower, check internet connection

### Optimize for Large Classes
- Current: Works for 64 students
- For >1000 students: Consider async sending
- For external SMTP: Modify send_email() function

### Reduce Log File Size
- After each run, `attendance.log` grows
- Archive old logs periodically:
  ```bash
  # Move old log
  mv attendance.log attendance_backup_$(date +%Y%m%d).log
  ```

---

## 🔐 Security Checklist

- [ ] Using App Password (not main Gmail password)
- [ ] Environment variables set (not hardcoded)
- [ ] No credentials in source code
- [ ] No credentials in version control (git)
- [ ] No sharing of GMAIL_APP_PASSWORD
- [ ] Attended 2-Step Verification setup
- [ ] Limited App Password to "Mail" only
- [ ] Using SSL/TLS encryption (default)

---

## 📞 Help & Support

### View Detailed Help
```bash
# Open the full documentation
cat DOCUMENTATION.md

# Open setup guide
cat SETUP_GUIDE.md
```

### Enable Debug Mode
Add to top of `attendance_app.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

This shows more detailed information during execution.

### Check Logs
```bash
# View last 20 lines
tail -20 attendance.log

# Search for errors
grep "ERROR" attendance.log

# Search for specific student
grep "Student Name" attendance.log
```

---

## 📱 Example Workflow

### Step 1: Create Students List
```csv
Roll,Name,Email
1,Alice Johnson,alice@gmail.com
2,Bob Smith,bob@gmail.com
3,Carol Davis,carol@gmail.com
...
64,Zara Wilson,zara@gmail.com
```

### Step 2: Record Attendance
```
1,2,3,4,5,6,7,8,9,10
2,3,4,5,6,7,8,9,10,11
3,4,5,6,7,8,9,10,11,12
...
```

### Step 3: Set Credentials
```bash
setx GMAIL_USER "instructor@gmail.com"
setx GMAIL_APP_PASSWORD "abcd efgh ijkl mnop"
```

### Step 4: Run Application
```bash
python attendance_app.py
```

### Step 5: Review Results
- Check `attendance_report.csv`
- Verify emails sent in log
- Each student receives personalized report

---

## 🎯 Usage Examples

### Example 1: First Time Setup
```bash
# 1. Download files
# 2. Place students.csv and attendance.txt in folder
# 3. Set environment variables
setx GMAIL_USER "my-email@gmail.com"
setx GMAIL_APP_PASSWORD "xxxx xxxx xxxx xxxx"
# 4. Restart Command Prompt
# 5. Run
python attendance_app.py
```

### Example 2: Update Attendance
```bash
# 1. Edit attendance.txt to add new class
# 2. Add line: 1,2,3,5,7,9,11,13 (new class)
# 3. Run
python attendance_app.py
# 4. New attendance_report.csv generated
# 5. Emails updated with new percentages
```

### Example 3: Test Before Full Run
```bash
# 1. Edit students.csv - keep only 3 students
# 2. Edit attendance.txt - keep only 2 lines
# 3. Update email addresses to test emails
# 4. Run: python attendance_app.py
# 5. Verify test emails received
# 6. Restore full students.csv
# 7. Run full script
```

---

## 📊 Output File Reference

### `attendance_report.csv`
- **What**: Summary table of all students
- **When**: Generated every run
- **Use**: Import to Excel, track trends, audit records
- **Columns**: Roll, Name, Email, Classes Attended, Total Classes, Attendance %

### `attendance.log`
- **What**: Execution log with timestamps
- **When**: Appended every run
- **Use**: Troubleshooting, verification, audit trail
- **Level**: INFO, WARNING, ERROR messages

### Email Messages
- **What**: Personalized HTML reports
- **When**: Sent to each student
- **Use**: Student notification, record keeping
- **Colors**: Green (≥75%), Red (<75%)

---

## ✨ Tips & Tricks

### Create a Shortcut (Windows)
```batch
# Create run.bat file
@echo off
python attendance_app.py
pause
```

Double-click to run without opening cmd.

### Automate Weekly Runs (Windows Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly on Friday at 5 PM
4. Action: Run `python attendance_app.py`

### Automate Weekly Runs (Mac/Linux Cron)
```bash
# Edit crontab
crontab -e

# Add line for Friday 5 PM
0 17 * * 5 /usr/bin/python3 /path/to/attendance_app.py
```

### Email Preview
Check the HTML in `create_html_email()` function for how emails look.

---

## 🎓 Learning Resources

### Python Documentation
- Official Python: https://www.python.org/doc/
- SMTP Library: https://docs.python.org/3/library/smtplib.html
- CSV Module: https://docs.python.org/3/library/csv.html

### Gmail Setup
- App Passwords: https://support.google.com/accounts/answer/185833
- 2-Step Verification: https://support.google.com/accounts/answer/185839

### Related Topics
- Security: https://owasp.org/
- Email Best Practices: https://www.campaignmonitor.com/

---

## 📋 Glossary

| Term | Definition |
|------|-----------|
| Roll Number | Unique student identifier (1-64) |
| Attendance % | Percentage of classes attended |
| App Password | 16-char Gmail token (limited permissions) |
| CSV | Comma-Separated Values (spreadsheet format) |
| SMTP | Simple Mail Transfer Protocol (email sending) |
| SSL/TLS | Encryption protocols for secure connections |
| Environment Variable | OS-level configuration (not in code) |
| Threshold | Minimum value for good status (75%) |

---

**Last Updated**: January 2025
**Version**: 1.0
**Quick Reference Guide**
