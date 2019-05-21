from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(send_from, subject, send_to, html):

    send_to = send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(html, 'html'))

    smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login('noreply.backpack@gmail.com', '5&K541KPVzf=Q,aOkoi21[vXV,qo')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()