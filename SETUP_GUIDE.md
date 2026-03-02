# Attendance Recording Application - Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Install Python Dependencies](#install-python-dependencies)
3. [Gmail Setup](#gmail-setup)
4. [Environment Variables Setup](#environment-variables-setup)
5. [Prepare Data Files](#prepare-data-files)
6. [Run the Application](#run-the-application)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

- **Python**: 3.6 or higher
- **Operating System**: Windows, macOS, or Linux
- **Gmail Account**: Required for sending emails
- **Internet Connection**: Required for Gmail SMTP

---

## Install Python Dependencies

The application uses only Python's built-in libraries. No external packages need to be installed!

**Built-in modules used:**
- `os` - Environment variable management
- `csv` - CSV file handling
- `logging` - Logging and error tracking
- `smtplib` - Gmail SMTP connection
- `ssl` - Secure SSL/TLS connection
- `email.message` - Email composition
- `datetime` - Timestamp generation
- `pathlib` - File path handling

✅ **All dependencies come with Python by default!**

---

## Gmail Setup

### Step 1: Enable 2-Step Verification (if not already enabled)

1. Go to **Google Account**: https://myaccount.google.com/
2. Click **"Security"** in the left sidebar
3. Scroll down to **"How you sign in to Google"**
4. Click **"2-Step Verification"**
5. Follow the on-screen prompts to verify your identity
6. Complete the setup process

### Step 2: Create an App Password

1. Go to **Google Account**: https://myaccount.google.com/
2. Click **"Security"** in the left sidebar
3. Scroll down to **"App passwords"** (only visible if 2-Step Verification is enabled)
4. Select:
   - **App**: "Mail"
   - **Device**: "Windows PC" / "Mac" / "Linux" (choose your OS)
5. Click **"Generate"**
6. Google will display a **16-character password**
7. **Copy this password** - you'll need it for the next step!

⚠️ **IMPORTANT**: Keep this App Password secure. Do NOT share it publicly.

---

## Environment Variables Setup

Environment variables securely store your Gmail credentials without hardcoding them in the script.

### 🪟 Windows Setup

#### Option 1: Using Command Prompt (Permanent)

1. Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter)

2. Run the following commands:
   ```
   setx GMAIL_USER "your-email@gmail.com"
   setx GMAIL_APP_PASSWORD "xxxx xxxx xxxx xxxx"
   ```
   Replace:
   - `your-email@gmail.com` with your actual Gmail address
   - `xxxx xxxx xxxx xxxx` with the 16-character App Password (copy from Step 2 above)

3. Close and reopen Command Prompt for changes to take effect

4. Verify the variables were set:
   ```
   echo %GMAIL_USER%
   echo %GMAIL_APP_PASSWORD%
   ```

#### Option 2: Using Environment Variables GUI (Permanent)

1. Press `Win + X` and select **"System"**
2. Click **"Advanced system settings"** on the left
3. Click **"Environment Variables"** button
4. Under **"User variables"**, click **"New"**
5. Create two new variables:
   - **Variable name**: `GMAIL_USER` | **Value**: `your-email@gmail.com`
   - **Variable name**: `GMAIL_APP_PASSWORD` | **Value**: `xxxx xxxx xxxx xxxx`
6. Click **"OK"** and restart your computer

#### Option 3: Using PowerShell (Per session)

1. Open **PowerShell** (press `Win + X`, select "Windows PowerShell")

2. Run:
   ```powershell
   $env:GMAIL_USER = "your-email@gmail.com"
   $env:GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"
   ```

   (Note: This only lasts for the current session)

---

### 🍎 macOS / 🐧 Linux Setup

#### Option 1: Using Terminal (Permanent)

1. Open **Terminal**

2. Edit your shell profile:
   ```bash
   nano ~/.bash_profile
   ```
   (Or use `~/.zshrc` if you're using zsh on macOS)

3. Add these lines at the end:
   ```bash
   export GMAIL_USER="your-email@gmail.com"
   export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
   ```

4. Save the file:
   - Press `Ctrl + O`, then `Enter`
   - Press `Ctrl + X`

5. Reload the profile:
   ```bash
   source ~/.bash_profile
   ```

6. Verify the variables:
   ```bash
   echo $GMAIL_USER
   echo $GMAIL_APP_PASSWORD
   ```

#### Option 2: Per Terminal Session

```bash
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

(Note: This only lasts for the current terminal session)

---

## Prepare Data Files

The application requires two data files in the same directory as `attendance_app.py`:

### 1. `students.csv`

**Format**: CSV with headers: `Roll`, `Name`, `Email`

**Example**:
```
Roll,Name,Email
1,Aarjav Sharma,aarjav.sharma@example.com
2,Bhavna Patel,bhavna.patel@example.com
3,Chirag Verma,chirag.verma@example.com
...
```

**Rules**:
- First column: Roll number (1-64)
- Second column: Student full name
- Third column: Student email address
- Total: 64 rows (plus header)

**Sample file provided**: `students.csv` (ready to use or customize)

### 2. `attendance.txt`

**Format**: Text file with comma-separated roll numbers. Each line = one class.

**Example**:
```
1,2,3,5,7,9,11,13,15,17,19,21,23,25
1,3,4,6,8,10,12,14,16,18,20,22,24,26
2,4,5,7,9,11,13,15,17,19,21,23,25,27
...
```

**Rules**:
- Each line represents one class
- Numbers are roll numbers (1-64) separated by commas
- No headers needed
- Empty lines are skipped

**Sample file provided**: `attendance.txt` with 10 sample classes

---

## Run the Application

### Step 1: Navigate to the Application Directory

```bash
# Windows
cd C:\path\to\attendance_app

# macOS / Linux
cd /path/to/attendance_app
```

### Step 2: Run the Script

```bash
python attendance_app.py
```

Or if you have both Python 2 and 3:

```bash
python3 attendance_app.py
```

### Step 3: Monitor the Output

The application will display:
```
📖 Loading student data...
✓ Loaded 64 students

📋 Reading attendance records...
✓ Found 10 classes

🧮 Calculating attendance percentages...
✓ Attendance calculated for 64 students

📊 Generating attendance report...
✓ Report saved to attendance_report.csv

📧 Sending attendance emails to students...
--------------------------------------------------------------------------------
[1/64] ✓ Aarjav Sharma (aarjav.sharma@example.com)
[2/64] ✓ Bhavna Patel (bhavna.patel@example.com)
...
```

### Step 4: Check Results

Three output files will be created:

1. **`attendance_report.csv`** - Summary of all students' attendance
   ```
   Roll,Name,Email,Classes Attended,Total Classes,Attendance Percentage
   1,Aarjav Sharma,aarjav.sharma@example.com,8,10,80.0
   ...
   ```

2. **`attendance.log`** - Detailed execution log
   ```
   2025-01-15 10:30:45,123 - INFO - Successfully loaded 64 students
   2025-01-15 10:30:46,456 - INFO - Successfully read 10 attendance records
   ...
   ```

3. **Emails sent** to each student with personalized HTML report

---

## Troubleshooting

### ❌ Error: "Gmail credentials not found in environment variables"

**Solution**: Make sure environment variables are set correctly:
- Windows: Run `echo %GMAIL_USER%` in Command Prompt
- macOS/Linux: Run `echo $GMAIL_USER` in Terminal

If empty, re-follow the **Environment Variables Setup** section above.

---

### ❌ Error: "Gmail authentication failed"

**Possible causes**:
1. **Wrong App Password**: App Password is not the same as your Gmail password
   - Go to: https://myaccount.google.com/apppasswords
   - Create a new one and update your environment variable

2. **2-Step Verification not enabled**:
   - Enable it first (see Gmail Setup section)
   - Then create an App Password

3. **Spaces in the password**: Some systems require removing spaces
   - Try: `xxxxxxxxxxxx` (without spaces)

---

### ❌ Error: "File not found: students.csv"

**Solution**: 
- Make sure `students.csv` is in the same directory as `attendance_app.py`
- Verify the filename spelling (case-sensitive on macOS/Linux)

---

### ❌ Error: "SMTP error" during email sending

**Possible causes**:
1. **Network issue**: Check your internet connection
2. **Gmail account issue**: Try logging into Gmail manually
3. **Too many emails**: If sending many emails rapidly, Gmail may rate-limit
   - Wait a few minutes and try again

---

### ⚠️ Emails not arriving in students' inboxes?

**Check**:
1. Spam/Junk folder
2. Email logs: Open `attendance.log` to verify emails were sent
3. Student email addresses: Verify they're correct in `students.csv`

---

### ❓ How do I test without sending real emails?

**Option 1**: Test with a test email address first
- Create a test Gmail account
- Update `students.csv` with test email address
- Run the app

**Option 2**: Comment out the email sending section
- In `attendance_app.py`, find the `for idx, student in enumerate(attendance_data, 1):` loop
- Comment out the `send_email()` call
- Run the app to test the report generation

---

## FAQ

### Q: Can I use a non-Gmail email address?
**A**: No. This application is specifically designed for Gmail SMTP (smtp.gmail.com). 
However, you can modify the SMTP settings to use another email provider.

### Q: Is it safe to store Gmail credentials?
**A**: Yes, using environment variables is secure because:
- Credentials are not in the source code
- They're stored at the system level
- The App Password has limited permissions (Mail only)

### Q: Can I run this on a schedule (cron job)?
**A**: Yes! On Linux/macOS:
```bash
# Open crontab
crontab -e

# Add this line to run every Friday at 5 PM
0 17 * * 5 /usr/bin/python3 /path/to/attendance_app.py
```

### Q: What if I have more than 64 students?
**A**: Simply add more rows to `students.csv` and update roll numbers accordingly.

### Q: Can I customize the email template?
**A**: Yes! Edit the `create_html_email()` function in `attendance_app.py` to change colors, text, and layout.

---

## Support & Documentation

- **Python Docs**: https://docs.python.org/3/
- **Gmail App Passwords**: https://support.google.com/accounts/answer/185833
- **SMTP Documentation**: https://docs.python.org/3/library/smtplib.html

---

**Last Updated**: January 2025
**Version**: 1.0
**License**: MIT
