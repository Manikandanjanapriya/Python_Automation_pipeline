# email_bot.py

import smtplib, csv, os, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# ---- CONFIG ----------------------------------------
SENDER_EMAIL = 'muruganagp8697@gmail.com'
SENDER_PASSWORD = 'bhtt adkx tvhu bnpz'  # App password
SENDER_NAME = 'Janapriya M'

RECIPIENTS_CSV = 'recipients.csv'
LOG_FILE = 'email_log.csv'
ATTACHMENT_PATH = None
DELAY_SECONDS = 2

# ---- Build email -----------------------------------
def build_email(name, company):
    subject = f'Sales Report - {datetime.today().strftime("%B %Y")}'

    html = f"""
    <html>
    <body style="font-family:Arial;padding:20px;">
        <h2 style="color:#14b8a6;">Monthly Sales Report</h2>
        <p>Hi <b>{name}</b>,</p>
        <p>Please find this month's sales report for <b>{company}</b>.</p>
        <p><b>Highlights:</b> Revenue exceeded target 🎉</p>
        <p>Best regards,<br>{SENDER_NAME}</p>
    </body>
    </html>
    """

    plain = f"Hi {name},\nMonthly report for {company}.\nBest,\n{SENDER_NAME}"

    return subject, html, plain

# ---- Create message ---------------------------------
def create_message(to_email, name, company):
    subject, html, plain = build_email(name, company)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'{SENDER_NAME} <{SENDER_EMAIL}>'
    msg['To'] = to_email

    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # Attachment
    if ATTACHMENT_PATH and os.path.isfile(ATTACHMENT_PATH):
        with open(ATTACHMENT_PATH, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)

            fname = os.path.basename(ATTACHMENT_PATH)
            part.add_header('Content-Disposition', f'attachment; filename="{fname}"')
            msg.attach(part)

    return msg

# ---- Main -------------------------------------------
def run_email_bot():
    with open(RECIPIENTS_CSV, encoding='utf-8') as f:
        recipients = list(csv.DictReader(f))

    print(f'Email Bot | {len(recipients)} recipients')

    logs = []
    sent = failed = 0
    

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print('Connected to Gmail SMTP')

            for r in recipients:
                name = r.get('name', 'there')
                email = r.get('email', '').strip()
                company = r.get('company', 'Company')

                

                if not email:
                    print("Skipping empty email")
                    continue

                try:
                    msg = create_message(email, name, company)
                    server.sendmail(SENDER_EMAIL, email, msg.as_string())

                    print(f'Sent -> {name} <{email}>')
                    logs.append({'name': name, 'email': email, 'status': 'OK', 'error': ''})
                    sent += 1

                except Exception as e:
                    print(f'FAIL -> {email}: {e}')
                    logs.append({'name': name, 'email': email, 'status': 'FAIL', 'error': str(e)})
                    failed += 1

                time.sleep(DELAY_SECONDS)

    except smtplib.SMTPAuthenticationError:
        print('AUTH ERROR: Use Gmail App Password!')
        return

    # Save log
    with open(LOG_FILE, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['name', 'email', 'status', 'error'])
        w.writeheader()
        w.writerows(logs)

    print(f'\nSent: {sent} | Failed: {failed} | Log: {LOG_FILE}')

# ---- Run --------------------------------------------
if __name__ == '__main__':
    run_email_bot()