# Bulk Email Automation Tool

A Python script to send bulk personalized emails with optional attachments via Gmail SMTP.

---

## Features

- Send personalized emails to multiple recipients from a CSV,PDF file  
- Support for email attachments  
- Simple configuration through a `config.py` file  
- Uses Gmail SMTP for sending emails  

---

## Setup

1. **Create a `config.py` file** in your project directory with your Gmail credentials:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
