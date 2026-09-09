from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_password_reset_email(self, email, first_name, reset_link):
    subject = "Reset your Pusthak Library password"
    context = {"first_name": first_name or "there", "reset_link": reset_link, "expiry_hours": 24}
    html_content = render_to_string("emails/password_reset.html", context)
    text_content = strip_tags(html_content)
    try:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_branch_admin_credentials_email(self, email, first_name, branch_name, raw_password, reset_link):
    subject = f"Your profile has been created — {branch_name}"
    message = (
        f"Hi {first_name},\n\n"
        f"A profile has been created for you at the '{branch_name}' branch "
        f"of Pusthak Library.\n\n"
        f"Login email: {email}\n"
        f"Password: {raw_password}\n\n"
        f"Note: This is an auto-generated password. Please make sure to reset "
        f"your password after logging in.\n\n"
        f"Reset your password here: {reset_link}\n"
        f"Regards,\nPusthak Library Team"
    )
    try:
        send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                   recipient_list=[email], fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc)