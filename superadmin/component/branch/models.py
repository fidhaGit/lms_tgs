from django.db import models
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
     history = HistoricalRecords()
     class Meta:
             db_table = "branch"
             ordering = ["name"]
     
     def __str__(self):
             return self.name