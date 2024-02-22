import subprocess
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os


def send_email(subject, message, from_addr, to_addr, smtp_server, port, login, password, attachment=None):
    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg.attach(MIMEText(message, 'plain'))
    try:
        # Create server object with SSL option
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(login, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print("Email successfully sent!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


# Run cv3.py and capture its output
result = subprocess.run(['python', 'cv3.py'], capture_output=True, text=True)
output = result.stdout

# Assume cv3.py saves the screenshot as 'screenshot.png'
screenshot_filename = 'screenshot.png'

# Get the current date and time
now = datetime.datetime.now()
formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

# Save the captured output to a file
with open('output.txt', 'w') as file:
    file.write(output)

screenshot_filename = 'screenshot.png'  # or the full path if not in the same directory
if not os.path.exists(screenshot_filename):
    print(f"Error: {screenshot_filename} does not exist.")
elif not os.access(screenshot_filename, os.R_OK):
    print(f"Error: {screenshot_filename} is not accessible.")
else:
    print(f"{screenshot_filename} is ready to be attached.")


# Example usage
load_dotenv('.env')
email_password = os.getenv('EMAIL_PASSWORD')
email_username = os.getenv('EMAIL_USERNAME')
subject = f"Connecting to BackOffice at {formatted_datetime}"
body = f"Please find below the output of the script and a screenshot attached.\n\nScript Output:\n{output}"
from_addr = "juan@liberatemarketing.com"
to_addr = "jduque0289@gmail.com"
smtp_server = "gcam1215.siteground.biz"
port = 465  # For SSL
login = email_username
password = email_password
attachments = ['output.txt', screenshot_filename]
send_email(subject, body, from_addr, to_addr, smtp_server, port, login, password, attachments)
