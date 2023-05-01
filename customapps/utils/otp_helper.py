import random
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django_otp.oath import TOTP
from django_otp.util import random_hex
from customapps.svuser.models import StaticDevice, StaticToken


def generate_otp():
    otp_secret = random_hex(20)
    totp = TOTP(otp_secret.encode())            
    return totp.token()

def send_otp(otp,email=None,phone_number=None):
        return send_otp_email(otp,email) or send_otp_sms(otp,phone_number)

def verify_otp(otp_secret,otp):
    totp = TOTP(otp_secret.encode(),step=600)
    return totp.verify(int(otp))

def send_otp_sms(otp,phone_number):
    if phone_number:
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
        return response.json().get('return') == True
    else:
        return False



def send_otp_email(otp,to_email):    
    if to_email:
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
            return False
    else: return False


    
def create_device_token(user=None,name=None, otp=None):
    if not (user or name):
        return None, None
    #  Creating a Device by user or by name 
    if user is not None:
        device, _ = StaticDevice.objects.get_or_create(user=user)
    else:
        device, _ = StaticDevice.objects.get_or_create(name=name)

    # if otp is not provided, generate and update table
    if not otp:
        otp = generate_otp()
        static_token, _ = StaticToken.objects.update_or_create(device=device,defaults={'token':otp})
    else:
         try:static_token= StaticToken.objects.get(device=device)
         except: static_token=None

    return device, static_token