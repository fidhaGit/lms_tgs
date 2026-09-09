from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import Branch


@receiver(post_save, sender=Branch)
def create_branch_admin(sender, instance, created, **kwargs):
    """
    Runs automatically every time a Branch is saved.
    `created` is True only the FIRST time it's saved (i.e. brand new branch).
    """
    if not created:
        return

    if not instance.admin_email or not instance.admin_first_name:
        # No admin details were given when the branch was created, so skip.
        return

    # Imported here (not at the top) to avoid circular-import issues,
    # since Users imports Branch.
    from superadmin.component.user.models import Users
    from superadmin.component.role.models import Role
    from superadmin.component.user.utils import generate_random_password
    from superadmin.component.user.tasks import send_branch_admin_credentials_email

    if Users.objects.filter(email__iexact=instance.admin_email).exists():
        return

    admin_role, _ = Role.objects.get_or_create(name='admin')
    raw_password = generate_random_password()

    admin_user = Users.objects.create(
        email=instance.admin_email,
        first_name=instance.admin_first_name,
        last_name=instance.admin_last_name or '',
        phone=instance.admin_phone,
        role=admin_role,
        branch=instance,
        password=make_password(raw_password),
    )

    send_branch_admin_credentials_email.delay(
        admin_user.email, admin_user.first_name, instance.name, raw_password
    )