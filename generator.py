import secrets
import string

def generate_password(length=16, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))
