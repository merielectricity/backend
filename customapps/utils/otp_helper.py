import random
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django_otp.oath import TOTP

def generate_otp(otp_secret):
    totp = TOTP(otp_secret.encode(),step=600)            
    return totp.token()

def send_otp(otp,data):
    if data.get("email") is not None:
        return send_otp_email(otp,data.get("email"))
    elif data.get("phone_number") is not None:
        return send_otp_sms(otp,data.get("phone_number"))

def verify_otp(otp_secret,otp):
    totp = TOTP(otp_secret.encode(),step=600)
    return totp.verify(int(otp))

def send_otp_sms(otp,phone_number):
    url = "https://www.fast2sms.com/dev/bulkV2"
    variables_values = otp
    numbers = phone_number
    # Construct payload with dynamic variables_values and numbers
    payload = f"variables_values={variables_values}&route=otp&numbers={numbers}"
    headers = {
        'authorization': "ex2aEhfJdDymXBjHv16LtYOKoG9zRA8kcrZqWUQ3FSIlngubwT1Izom3akxpcvbNwZhyUFC0AuGV2dE6",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response= requests.post(url, data=payload, headers=headers)
    if 'return":true' in response.text:
        return True
    else:
        return False



def send_otp_email(otp,to_email):    
    # Render the email template with the context variables
    template = get_template('emails/otp_email.html')
    subject = "OTP Verification For SolarVerse"
    context = {'otp_code': otp}
    email_body = template.render(context)
    
    # Create the email message
    email_message = EmailMultiAlternatives(
        subject=subject,
        body=email_body,
        from_email=settings.OSCAR_FROM_EMAIL,
        to=[to_email],
    )
    
    # Attach an HTML version of the email template
    html_email = template.render(context)
    email_message.attach_alternative(html_email, 'text/html')
    
    # Send the email
    try:
        email_message.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


    
