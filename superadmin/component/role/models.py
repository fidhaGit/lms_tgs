from django.db import models
from shared.models import BaseModel

class Role(BaseModel):
    options = {
    "SUPER_ADMIN": "super_admin",
    "ADMIN": "admin",
    "STAFF": "staff",
    "MEMBER": "member",}
    name = models.CharField(max_length=20,choices=options,unique=True,)
    description = models.TextField(blank=True,)
    is_active = models.BooleanField(default=True,)
    class Meta:
        db_table = "roles"
        ordering = ["name"]

    def __str__(self):
        return self.name()