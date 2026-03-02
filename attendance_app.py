"""
Attendance Recording Application
================================
A Python application that records student attendance, calculates percentages,
and sends personalized HTML email reports to each student via Gmail.

Author: Attendance System
License: MIT
"""

import os
import csv
import logging
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attendance.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# FUNCTION: load_students()
# ============================================================================
def load_students(filename='students.csv'):
    """
    Load student data from CSV file.
    
    Args:
        filename (str): Path to the students CSV file
        
    Returns:
        list: List of dictionaries with keys: Roll, Name, Email
        
    Raises:
        FileNotFoundError: If students.csv doesn't exist
        ValueError: If CSV format is invalid
    """
    try:
        # Check if file exists
        if not Path(filename).exists():
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(f"File not found: {filename}")
        
        students = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validate headers
            if reader.fieldnames != ['Roll', 'Name', 'Email']:
                logger.error("Invalid CSV headers. Expected: Roll, Name, Email")
                raise ValueError("Invalid CSV headers. Expected: Roll, Name, Email")
            
            for row in reader:
                # Validate that all fields are present
                if not all(row.values()):
                    logger.warning(f"Skipping incomplete row: {row}")
                    continue
                students.append(row)
        
        logger.info(f"Successfully loaded {len(students)} students from {filename}")
        return students
    
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading students: {e}")
        raise


# ============================================================================
# FUNCTION: read_attendance()
# ============================================================================
def read_attendance(filename='attendance.txt'):
    """
    Read attendance records from text file.
    
    Each line represents one class with comma-separated roll numbers of present students.
    
    Args:
        filename (str): Path to the attendance file
        
    Returns:
        list: List of lists, where each inner list contains roll numbers present in that class
        
    Raises:
        FileNotFoundError: If attendance.txt doesn't exist
    """
    try:
        if not Path(filename).exists():
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(f"File not found: {filename}")
        
        attendance_records = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    logger.warning(f"Skipping empty line {line_num}")
                    continue
                
                # Parse roll numbers from comma-separated values
                try:
                    roll_numbers = [int(roll.strip()) for roll in line.split(',')]
                    attendance_records.append(roll_numbers)
                except ValueError as e:
                    logger.warning(f"Invalid format in line {line_num}: {line}")
                    continue
        
        logger.info(f"Successfully read {len(attendance_records)} attendance records from {filename}")
        return attendance_records
    
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while reading attendance: {e}")
        raise


# ============================================================================
# FUNCTION: calculate_attendance()
# ============================================================================
def calculate_attendance(students, attendance_records):
    """
    Calculate attendance percentage for each student.
    
    Args:
        students (list): List of student dictionaries with Roll, Name, Email
        attendance_records (list): List of attendance records (each is a list of roll numbers)
        
    Returns:
        list: List of dictionaries with attendance data:
              Roll, Name, Email, Classes Attended, Total Classes, Attendance Percentage
    """
    try:
        total_classes = len(attendance_records)
        
        if total_classes == 0:
            logger.warning("No attendance records found. Total classes = 0")
        
        # Create a dictionary to track attendance for each roll number
        attendance_data = {}
        
        for student in students:
            roll = int(student['Roll'])
            attendance_data[roll] = {
                'Roll': student['Roll'],
                'Name': student['Name'],
                'Email': student['Email'],
                'Classes Attended': 0,
                'Total Classes': total_classes,
                'Attendance Percentage': 0.0
            }
        
        # Count attendance for each student
        for attendance_record in attendance_records:
            for roll in attendance_record:
                if roll in attendance_data:
                    attendance_data[roll]['Classes Attended'] += 1
        
        # Calculate attendance percentage
        for roll, data in attendance_data.items():
            if total_classes > 0:
                percentage = (data['Classes Attended'] / total_classes) * 100
                data['Attendance Percentage'] = round(percentage, 2)
            else:
                data['Attendance Percentage'] = 0.0
        
        result = list(attendance_data.values())
        logger.info(f"Calculated attendance for {len(result)} students")
        return result
    
    except Exception as e:
        logger.error(f"Error calculating attendance: {e}")
        raise


# ============================================================================
# FUNCTION: generate_report()
# ============================================================================
def generate_report(attendance_data, filename='attendance_report.csv'):
    """
    Generate attendance report CSV file.
    
    Args:
        attendance_data (list): List of dictionaries with attendance information
        filename (str): Output filename for the report
        
    Returns:
        str: Path to the generated report file
    """
    try:
        fieldnames = ['Roll', 'Name', 'Email', 'Classes Attended', 'Total Classes', 'Attendance Percentage']
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(attendance_data)
        
        logger.info(f"Report successfully generated: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise


# ============================================================================
# FUNCTION: create_html_email()
# ============================================================================
def create_html_email(student_data):
    """
    Create an HTML email body for the student's attendance report.
    
    Args:
        student_data (dict): Dictionary with student attendance information
        
    Returns:
        str: HTML formatted email body
    """
    try:
        name = student_data['Name']
        roll = student_data['Roll']
        classes_attended = student_data['Classes Attended']
        total_classes = student_data['Total Classes']
        attendance_pct = student_data['Attendance Percentage']
        
        # Determine color based on attendance threshold (75%)
        color = '#27ae60' if attendance_pct >= 75 else '#e74c3c'  # Green or Red
        status = '✓ Good' if attendance_pct >= 75 else '⚠ Below Target'
        
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background-color: #2c3e50;
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                    }}
                    .header p {{
                        margin: 10px 0 0 0;
                        font-size: 14px;
                        opacity: 0.9;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .greeting {{
                        font-size: 18px;
                        color: #2c3e50;
                        margin-bottom: 20px;
                    }}
                    .data-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    .data-table th {{
                        background-color: #ecf0f1;
                        padding: 12px;
                        text-align: left;
                        font-weight: 600;
                        color: #2c3e50;
                        border-bottom: 2px solid #bdc3c7;
                    }}
                    .data-table td {{
                        padding: 12px;
                        border-bottom: 1px solid #ecf0f1;
                        font-size: 15px;
                        color: #34495e;
                    }}
                    .data-table tr:last-child td {{
                        border-bottom: none;
                    }}
                    .attendance-box {{
                        background-color: {color};
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .attendance-box h2 {{
                        margin: 0 0 10px 0;
                        font-size: 28px;
                    }}
                    .attendance-box p {{
                        margin: 0;
                        font-size: 14px;
                        opacity: 0.9;
                    }}
                    .status {{
                        display: inline-block;
                        background-color: rgba(255, 255, 255, 0.2);
                        padding: 8px 16px;
                        border-radius: 20px;
                        font-size: 13px;
                        margin-top: 10px;
                    }}
                    .footer {{
                        background-color: #ecf0f1;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                        color: #7f8c8d;
                    }}
                    .footer p {{
                        margin: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 Attendance Report</h1>
                        <p>Your Personal Attendance Summary</p>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            Hello, <strong>{name}</strong> (Roll No. {roll})
                        </div>
                        
                        <p>Your attendance report for this term has been calculated. Please review your attendance summary below:</p>
                        
                        <table class="data-table">
                            <tr>
                                <th>Metric</th>
                                <th>Value</th>
                            </tr>
                            <tr>
                                <td>Classes Attended</td>
                                <td><strong>{classes_attended}</strong></td>
                            </tr>
                            <tr>
                                <td>Total Classes Conducted</td>
                                <td><strong>{total_classes}</strong></td>
                            </tr>
                        </table>
                        
                        <div class="attendance-box">
                            <h2>{attendance_pct}%</h2>
                            <p>Your Attendance Percentage</p>
                            <span class="status">{status}</span>
                        </div>
                        
                        <p style="color: #7f8c8d; font-size: 13px; margin-top: 20px;">
                            <strong>Note:</strong> An attendance percentage of 75% or above is considered good. 
                            If your attendance is below 75%, please consult with your instructor.
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Automated Attendance System</strong></p>
                        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>Please do not reply to this email. Contact your instructor for any queries.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html_body
    
    except Exception as e:
        logger.error(f"Error creating HTML email: {e}")
        raise


# ============================================================================
# FUNCTION: send_email()
# ============================================================================
def send_email(student_data, html_body, gmail_user, gmail_app_password):
    """
    Send attendance report email to a student using Gmail SMTP.
    
    Args:
        student_data (dict): Student information (Roll, Name, Email)
        html_body (str): HTML formatted email body
        gmail_user (str): Gmail account email address
        gmail_app_password (str): Gmail App Password (from environment variable)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Prepare email
        message = EmailMessage()
        message['Subject'] = f"📊 Your Attendance Report - {student_data['Name']}"
        message['From'] = gmail_user
        message['To'] = student_data['Email']
        
        # Set HTML content
        message.set_content('Your attendance report is attached.')
        message.add_alternative(html_body, subtype='html')
        
        # Create SSL context for secure connection
        context = ssl.create_default_context()
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(gmail_user, gmail_app_password)
            server.send_message(message)
        
        logger.info(f"Email sent successfully to {student_data['Name']} ({student_data['Email']})")
        return True
    
    except smtplib.SMTPAuthenticationError:
        logger.error(f"Gmail authentication failed for {student_data['Email']}. Check credentials.")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email to {student_data['Email']}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending email to {student_data['Email']}: {e}")
        return False


# ============================================================================
# FUNCTION: main()
# ============================================================================
def main():
    """
    Main execution function. Orchestrates the entire attendance workflow.
    """
    try:
        logger.info("=" * 80)
        logger.info("ATTENDANCE RECORDING APPLICATION STARTED")
        logger.info("=" * 80)
        
        # Step 1: Load environment variables for Gmail credentials
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_app_password:
            logger.error("Gmail credentials not found in environment variables.")
            logger.error("Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")
            print("\n❌ ERROR: Gmail credentials not configured!")
            print("Please follow the setup guide to configure environment variables.")
            return False
        
        logger.info(f"Gmail credentials loaded successfully for {gmail_user}")
        
        # Step 2: Load student data
        print("\n📖 Loading student data...")
        students = load_students('students.csv')
        print(f"✓ Loaded {len(students)} students")
        
        # Step 3: Read attendance records
        print("\n📋 Reading attendance records...")
        attendance_records = read_attendance('attendance.txt')
        print(f"✓ Found {len(attendance_records)} classes")
        
        # Step 4: Calculate attendance percentages
        print("\n🧮 Calculating attendance percentages...")
        attendance_data = calculate_attendance(students, attendance_records)
        print(f"✓ Attendance calculated for {len(attendance_data)} students")
        
        # Step 5: Generate report CSV
        print("\n📊 Generating attendance report...")
        report_file = generate_report(attendance_data, 'attendance_report.csv')
        print(f"✓ Report saved to {report_file}")
        
        # Step 6: Send emails
        print("\n📧 Sending attendance emails to students...")
        print("-" * 80)
        
        successful_emails = 0
        failed_emails = 0
        
        for idx, student in enumerate(attendance_data, 1):
            try:
                html_body = create_html_email(student)
                if send_email(student, html_body, gmail_user, gmail_app_password):
                    successful_emails += 1
                    print(f"[{idx}/{len(attendance_data)}] ✓ {student['Name']} ({student['Email']})")
                else:
                    failed_emails += 1
                    print(f"[{idx}/{len(attendance_data)}] ✗ {student['Name']} ({student['Email']}) - FAILED")
            except Exception as e:
                failed_emails += 1
                logger.error(f"Error processing student {student['Name']}: {e}")
                print(f"[{idx}/{len(attendance_data)}] ✗ {student['Name']} - ERROR")
        
        print("-" * 80)
        
        # Final summary
        logger.info("=" * 80)
        logger.info("ATTENDANCE RECORDING APPLICATION COMPLETED")
        logger.info("=" * 80)
        
        print("\n✅ PROCESS COMPLETED!")
        print(f"   Total Students: {len(attendance_data)}")
        print(f"   Emails Sent: {successful_emails}")
        print(f"   Emails Failed: {failed_emails}")
        print(f"   Report File: {report_file}")
        print(f"   Log File: attendance.log")
        
        return True
    
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"\n❌ File Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"\n❌ Error: {e}")
        return False


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
