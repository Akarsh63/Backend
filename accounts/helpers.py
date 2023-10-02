from django.core.mail import send_mail
from random import randint
from datetime import datetime, timedelta
from .models import PasswordResetRequest  # Import your model

def generate_otp():
    return randint(100000, 999999)

def send_otp_email(email, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = 'fromdjango@gmail.com'  # Replace with your desired sender email
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def create_reset_request(email,otp):
   
    expiration_time = datetime.now() + timedelta(minutes=30)
    # PasswordResetRequest.objects.create(email=email, otp=otp, expiration_time=expiration_time)
