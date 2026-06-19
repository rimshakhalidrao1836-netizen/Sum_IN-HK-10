import smtplib
import ssl
import csv
import json
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

HISTORY_FILE = "email_history.json"

def load_contacts(filepath):
    if not os.path.exists(filepath):
        print("Error: File not found")
        return []
    
    if filepath.endswith('.csv'):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    elif filepath.endswith('.json'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print("Error: Only CSV and JSON supported")
        return []

def load_template(filepath):
    if not os.path.exists(filepath):
        print("Error: Template file not found")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def personalize_message(template, contact):
    message = template
    for key, value in contact.items():
        placeholder = f"{{{key}}}"
        message = message.replace(placeholder, str(value))
    return message

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.lower()) is not None

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def send_bulk_emails(sender_email, password, contacts, subject_template, body_template):
    history = load_history()
    context = ssl.create_default_context()
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login(sender_email, password)
        print("Connected to SMTP server")
    except Exception as e:
        print(f"SMTP connection failed: {e}")
        return

    for contact in contacts:
        email = contact.get('email', '').strip().lower()
        
        if not is_valid_email(email):
            history.append({
                'email': email,
                'subject': subject_template,
                'status': 'Failed',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': 'Invalid email'
            })
            continue
        
        try:
            subject = personalize_message(subject_template, contact)
            body = personalize_message(body_template, contact)
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server.sendmail(sender_email, email, msg.as_string())
            
            history.append({
                'email': email,
                'subject': subject,
                'status': 'Sent',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': None
            })
            print(f"Sent to {email}")
            
        except Exception as e:
            history.append({
                'email': email,
                'subject': subject_template,
                'status': 'Failed',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': str(e)
            })
            print(f"Failed to send to {email}: {e}")
    
    server.quit()
    save_history(history)
    print(f"\nCompleted. Check {HISTORY_FILE} for details.")

def main_menu():
    contacts = []
    template = None
    subject_template = ""
    
    while True:
        print("\n===== Bulk Email Sender =====")
        print("1. Load Contacts")
        print("2. Load Template")
        print("3. Send Emails")
        print("4. View History")
        print("5. Exit")
        
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            filepath = input("Enter contacts file path (CSV/JSON): ").strip()
            contacts = load_contacts(filepath)
            print(f"Loaded {len(contacts)} contacts")
            
        elif choice == '2':
            filepath = input("Enter template file path: ").strip()
            template = load_template(filepath)
            subject_template = input("Enter email subject (use {placeholders}): ").strip()
            if template:
                print("Template loaded successfully")
                
        elif choice == '3':
            if not contacts or not template:
                print("Load contacts and template first")
                continue
            
            sender = input("Enter your email: ").strip()
            password = input("Enter app password: ").strip()
            
            confirm = input(f"Send emails to {len(contacts)} contacts? [y/n]: ").strip().lower()
            if confirm == 'y':
                send_bulk_emails(sender, password, contacts, subject_template, template)
                
        elif choice == '4':
            history = load_history()
            print(f"\nTotal emails: {len(history)}")
            for record in history[-10:]:
                print(f"[{record['status']}] {record['email']} - {record['timestamp']}")
                
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()