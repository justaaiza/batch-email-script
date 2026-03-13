import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import path, makedirs
from datetime import datetime
import re

def sendemail(sender: str, recipient: str, cc_list: list, file_attachment_paths: list, subject: str, body: str, smtp_server: smtplib.SMTP_SSL, log_file_path: str) -> bool:
    '''
    Sends an email to the specified recipient with optional CC list and file attachments.
    '''
    try:
        # Ensure cc_list is a list
        cc_list = cc_list if cc_list else []

        # Create message
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Cc"] = ", ".join(cc_list)
        message["Subject"] = subject

        # Support both plain-text and HTML email clients.
        # The body file can include HTML tags (e.g., <b>, <strong>) and we preserve them in the HTML part.
        # The plain-text part strips HTML tags so the text stays readable in clients that don't render HTML.
        plain_text_body = re.sub(r"<[^>]+>", "", body)
        plain_part = MIMEText(plain_text_body, "plain")
        html_body = body.replace("\n", "<br>")
        html_part = MIMEText(html_body, "html")
        alternative = MIMEMultipart("alternative")
        alternative.attach(plain_part)
        alternative.attach(html_part)
        message.attach(alternative)

        # Attach files
        for file_path in file_attachment_paths:
            if path.exists(file_path):  # Check if file exists
                with open(file_path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={path.basename(file_path)}")
                    message.attach(part)
            else:
                print(f"Warning: File not found - {file_path}")

        # Send email
        smtp_server.sendmail(sender, [recipient] + cc_list, message.as_string())

        # Ensure log directory exists
        log_dir = path.dirname(log_file_path)
        if log_dir and not path.exists(log_dir):
            makedirs(log_dir)

        # Append to log file
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{recipient},success,{datetime.now()}\n")

        return True

    except Exception as e:
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{recipient},error,{datetime.now()},{e}\n")
        return False

def isvalidemail(email: str) -> bool:
    '''
    Validates an email address using a regular expression.
    '''
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None
