import secrets
import string
from django.core import signing


def generate_random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        if has_lower and has_upper and has_digit:
            return password

PASSWORD_RESET_SALT = "password-reset"
PASSWORD_RESET_MAX_AGE = 60 * 60 * 24  # token valid for 24 hours
def generate_password_reset_token(user_id):
    return signing.dumps({"user_id": user_id}, salt=PASSWORD_RESET_SALT)
def verify_password_reset_token(token):
    try:
        data = signing.loads(token, salt=PASSWORD_RESET_SALT, max_age=PASSWORD_RESET_MAX_AGE)
        return data.get("user_id")
    except signing.BadSignature:
        return None