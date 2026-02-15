import random
import string
from django.core.cache import cache
from django.conf import settings

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    # Setup for real email sending would go here (e.g., using send_mail)
    # For now, we mock it by printing to console/logs
    print(f"=======================================")
    print(f"Sending OTP to {email}: {otp}")
    print(f"=======================================")
    return True

def store_otp(email, otp):
    key = f"otp:{email}"
    # Expire in 10 minutes (600 seconds)
    cache.set(key, otp, timeout=600)

def verify_otp_value(email, input_otp):
    key = f"otp:{email}"
    stored_otp = cache.get(key)
    if stored_otp and stored_otp == input_otp:
        cache.delete(key)
        return True
    return False
