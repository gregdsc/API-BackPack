import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_mail(send_from, subject, send_to, html):
    send_to = send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(html, 'html'))

    protocol_mail_transfer = smtplib.SMTP(host='smtp.gmail.com', port=587)
    protocol_mail_transfer.starttls()
    protocol_mail_transfer.login('noreply.backpack@gmail.com', 'Wpn%:)z5"KP4-&6Av,XodGC-dW8V')  # Env
    protocol_mail_transfer.sendmail(send_from, send_to, msg.as_string())
    protocol_mail_transfer.close()
