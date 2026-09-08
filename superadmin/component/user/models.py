from django.db import models
from simple_history.models import HistoricalRecords
from shared.models import BaseModel
from superadmin.component.branch.models import Branch
from superadmin.component.role.models import Role
   
class Users(BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True,null=True,blank=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=128)
    role=models.ForeignKey(Role,on_delete=models.PROTECT,related_name="users",)
    branch = models.ForeignKey(Branch,on_delete=models.PROTECT, related_name="users",)
    is_active = models.BooleanField(default=True,null=True)
    is_delete = models.BooleanField(default=False,null=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
     return f"{self.first_name} {self.last_name}"
    
 
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
