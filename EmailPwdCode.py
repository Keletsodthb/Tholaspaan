import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from math import ceil
from datetime import datetime
import secrets

def send_forgotpwd_email(self):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'TholaSpaan App Password Reset'
    msg['From'] = 'piecejobmzansi@gmail.com'
    msg['To'] = str(self.email.text)
    user_email = str(self.email.text)
    code = {secrets.token_urlsafe(16)}
    mask_chars = ceil(len(user_email) * 0.8)
    masked_email = f'{"*" * mask_chars}{user_email[-mask_chars:]}'
    html = f"""\
    <html>
    <body>
        <p>Good day,<br>
        Please use this code to reset the password for your TholaSpaan account.
        Here is your code: '{code}'
        If you don't recognize the Tholaspaan account '{masked_email}', you can click here to remove your email address from that account.
        Thanks,
        The TholaSpaan account team<br>
        </p>
    </body>
    </html>
    """
    part1 = MIMEText(html, "html")
    msg.attach(part1)

    text = msg.as_string()
    context = ssl.create_default_context()
    #with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        #smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        #smtp.sendmail(EMAIL_ADDRESS, test_recipients, text)

    return 