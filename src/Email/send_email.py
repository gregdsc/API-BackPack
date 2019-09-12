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
    smtp = smtplib.SMTP(host='SSL0.OVH.NET', port=587)
    smtp.starttls()
    smtp.login('contact@pick-me.eu', 'testapipython')
    try:
        smtp.sendmail(send_from, send_to, msg.as_string())
    except:
        return 'Mail non accepté'
    finally:
        smtp.close()
