from django.db import models
from django.contrib.auth.hashers import make_password
from shared.models import BaseModel
from simple_history.models import HistoricalRecords

# Create your models here.
class Branch(BaseModel):
     name=models.CharField(max_length=100,unique=True,null=True,blank=True)
     code = models.CharField(max_length=20,unique=True,)
     address = models.TextField(blank=True,)
     phone = models.CharField(max_length=20,blank=True,)
     email = models.EmailField(blank=True,)
     is_active = models.BooleanField(default=True,)
     is_delete = models.BooleanField(default=False,null=True)
     admin_email = models.EmailField(blank=True, null=True)
     admin_first_name = models.CharField(max_length=100, blank=True, null=True)
     admin_last_name = models.CharField(max_length=100, blank=True, null=True)
     admin_phone = models.CharField(max_length=20, blank=True, null=True)
     history = HistoricalRecords()
     class Meta:
             db_table = "branch"
             ordering = ["name"]
     
     def __str__(self):
             return self.name

     def save(self, *args, **kwargs):
             # self._state.adding is True only the FIRST time this row is saved
             # (i.e. it's a brand new branch, not an update to an existing one).
             is_new = self._state.adding
             super().save(*args, **kwargs)
             if is_new:
                     self.create_admin_account()

     def create_admin_account(self):
             if not self.admin_email or not self.admin_first_name:
                     return

             # Imported here (not at the top) to avoid circular-import issues,
             # since Users imports Branch.
             from superadmin.component.user.models import Users
             from superadmin.component.role.models import Role
             from superadmin.component.user.utils import generate_random_password, generate_password_reset_token
             from superadmin.component.user.tasks import send_branch_admin_credentials_email

             if Users.objects.filter(email__iexact=self.admin_email).exists():
                     return

             admin_role, _ = Role.objects.get_or_create(name='admin')
             raw_password = generate_random_password()

             admin_user = Users.objects.create(
                     email=self.admin_email,
                     first_name=self.admin_first_name,
                     last_name=self.admin_last_name or '',
                     phone=self.admin_phone,
                     role=admin_role,
                     branch=self,
                     password=make_password(raw_password),
             )

             token = generate_password_reset_token(admin_user.id)
             reset_link = f"http://127.0.0.1:8000/api/user/reset-password/{token}/"

             send_branch_admin_credentials_email.delay(
                     admin_user.email, admin_user.first_name, self.name, raw_password, reset_link
             )

     def branch_exists(branch_id):
      if not branch_id:
        return False
      return Branch.objects.filter(id=branch_id, is_delete=False).exists()
  

     def get_active_branch(branch_id):
       return Branch.objects.filter(id=branch_id, is_delete=False, is_active=True).first()     
#      def branch_has_dependent_data(branch_id):
   
#        try:
#            from pusthak_library_app.Branch.component.book.models import Book
#            if Book.objects.filter(branch_id=branch_id).exists():
#                return True
#        except ImportError:
#            pass
   
#        try:
#            from pusthak_library_app.Branch.component.member.models import Member
#            if Member.objects.filter(branch_id=branch_id).exists():
#                return True
#        except ImportError:
#            pass
   
#        return False