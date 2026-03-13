# imports
from modules.email_utils import sendemail, isvalidemail
from modules.smtp_utils import getSMTPServer
from os import path
from datetime import datetime
from time import sleep

#### Global Variables <set as per need before running main code> ####
# sender: The email address of the sender.
# password: The password or app-specific password for the sender's email account.
# attachment_file_paths: List of file paths to attach to emails.
sender = "" #enter your email
password = "" # create an App Password
attachment_file_paths = ["sample.docx"]

if __name__ == "__main__":
    '''
    Main script execution for sending emails to a list of recipients.

    Steps:
        1. Validate the sender email address.
        2. Check for the existence of required files (recipients, CC list, subject, body, log).
        3. Read and validate the subject and body content.
        4. Read and validate the CC list.
        5. Create an SMTP server object for sending emails.
        6. Loop through the recipient list and send emails.
        7. Log the status of each email (success, error, or invalid recipient).
        8. Close the SMTP server connection.
    '''
    # file paths:
    recipient_file_path = "./receipient_list.txt"
    cc_list_file_path = "./cc_list.txt"
    log_file_path = "./log.csv"
    subject_path: str = "./subject.txt"
    body_path: str = "./body.txt"

    # check if sender is valid
    if not isvalidemail(sender):
        print(">> Invalid sender email. Script ending...")
        while not isvalidemail(sender):
            sender = input("Enter valid sender email:")

    ### checking if files exist

    # check if recipient file exists
    if  not path.exists(recipient_file_path):
        print(">> Recipients file not found. Script ending...")
        exit()

    # check if log file exists
    if not path.exists(log_file_path):
        with open("log.csv", "w") as log:
            log.write("Recipient,Status,DateTime,Error\n")
    elif path.getsize(log_file_path) == 0:
        with open(log_file_path, "w") as log_file:
            log_file.write("Recipient,Status,DateTime,Error\n")

    # check if cc list file exists
    if not path.exists(cc_list_file_path):
        print("CC List file not found")
        with open("cc_list.txt", "w") as cc_list_file:
            cc_list_file.write("")

    # read and check subject and body
    try:
        with open("subject.txt", "r", encoding="utf-8") as subject_file:
            subject = subject_file.read()
        if not subject or subject == "":
            raise Exception("Subject file is empty")
        with open("body.txt", "r", encoding="utf-8") as body_file:
            body = body_file.read()
        if not body or body == "":
            raise Exception("Body file is empty")
    except Exception as e:
        print(">> Subject or Body file not found. Script ending...")
        print(f"    Error: {e}")
        exit()

    # reading cc list
    cc_list: list = []
    with open(cc_list_file_path, "r") as cc_list_file:
        cc_list = cc_list_file.read().split("\n")
        cc_list = [ email for email in cc_list if isvalidemail(email) ]

    # print on terminal
    print(">> CC List:")
    for email in cc_list:
        print(f"    {email}")

    # creating server
    try:
        server = getSMTPServer(sender, password)
    except Exception as e:
        print(f"Error: {e}")
        print(">> Error in creating server:", e, "- Script ending...")
        exit()

    # main emailer loop
    with open(recipient_file_path, "r") as recipient_file:
        i = 1
        for recipient in recipient_file:
            recipient = recipient.strip()
            if isvalidemail(recipient):
                print(f"{i}. Sending email to {recipient}...")
                sendemail(  sender,
                            recipient,
                            cc_list,
                            attachment_file_paths,
                            subject,
                            body,
                            server,
                            log_file_path )
                i += 1
                # sleep for 5 seconds
                sleep(5)
            else:
                # log in the log.csv file [new row entry: recipient email, "invalid", datetime]
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"{recipient},invalid,{datetime.now()}\n")

    # close server
    print(">> Script ended. Closing server...")
    server.quit()