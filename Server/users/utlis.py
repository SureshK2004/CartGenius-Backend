import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings

def generateOtp():
    otp = ''.join([str(random.randint(1, 9)) for _ in range(6)])
    return otp

def send_code_to_user(email):
    subject = "One-Time Passcode for Email Verification"
    otp_code = generateOtp()
    print(f"Generated OTP for {email}: {otp_code}")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print(f"User with email {email} not found.")
        return

    # Store or update OTP
    OneTimePassword.objects.update_or_create(
        user=user,
        defaults={'code': otp_code}
    )

    current_site = "myAuth.com"
    email_body = f"""
        <p>Hi <strong>{user.email}</strong>,</p>
        <p>Thanks for signing up on <strong>{current_site}</strong>.</p>
        <p>Please verify your email using this one-time passcode:</p>
        <h2 style="color:#2d3748;">🔐 {otp_code}</h2>
        <p>Have a nice day!</p>
    """

    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    email.content_subtype = 'html'  # To support HTML

    try:
        email.send()
        print(f"OTP email sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")


def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    email.content_subtype = 'html'

    try:
        email.send()
        print("Normal email sent successfully.")
    except Exception as e:
        print(f"Failed to send normal email: {e}")








