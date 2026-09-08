from django.db import models
from shared.models import BaseModel
from simple_history.models import HistoricalRecords


class Role(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name