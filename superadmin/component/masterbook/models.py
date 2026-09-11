from django.db import models
from shared.models import BaseModel
from simple_history.models import HistoricalRecords


class MasterBook(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)   
    edition = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        db_table = "master_book"
        ordering = ["title"]

    def __str__(self):
        return self.title