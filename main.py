import pandas as pd
import smtplib
from email.message import EmailMessage
from pathlib import Path
import ssl
import os
import tkinter as tk
from tkinter import messagebox

from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def read_template():
    with open("email_templates/email_body.txt", "r") as file:
        return file.read()

def send_email(name, to_email, report_path, email_body):
    msg = EmailMessage()
    msg['Subject'] = f"Your Report, {name}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(email_body.format(name=name))

    # Attach the report file
    with open(report_path, 'rb') as file:
        file_data = file.read()
        file_name = Path(report_path).name
        # Use 'application/octet-stream' to handle any file type safely
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Connect securely and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def send_bulk_emails():
    try:
        df = pd.read_csv("recipients.csv")
        email_body = read_template()
        base_dir = os.path.dirname(__file__)  # Directory where this script is located

        for index, row in df.iterrows():
            name = row['name']
            email = row['email']
            report_file = row['report_file'].strip()

            report_path = os.path.join(base_dir, report_file)
            print(f"Looking for report at: {report_path}")  # Debug print

            if os.path.exists(report_path):
                send_email(name, email, report_path, email_body)
                print(f"✅ Email sent to {name} ({email})")
            else:
                print(f"⚠️ Report not found: {report_path} for {name}")

        messagebox.showinfo("Success", "All emails have been sent!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def start_gui():
    window = tk.Tk()
    window.title("Email Automation Tool")
    window.geometry("300x150")

    label = tk.Label(window, text="Send Bulk Personalized Emails", font=("Arial", 12))
    label.pack(pady=20)

    send_button = tk.Button(window, text="Send Emails", command=send_bulk_emails, bg="green", fg="white", font=("Arial", 10))
    send_button.pack()

    window.mainloop()

if __name__ == "__main__":
    start_gui()
