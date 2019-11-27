from flask import current_app
import requests

def send_sms (message, to):
    payload = {'accessToken': current_app.config['SMS_KEY'], 'message': message, 'numero': to}
    r = requests.post("https://api.smsmode.com/http/1.6/sendSMS.do", data=payload)

    print(r.text)