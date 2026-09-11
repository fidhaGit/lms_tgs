from django.db import models
from shared.models import BaseModel
from simple_history.models import HistoricalRecords


class BookCopy(BaseModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ISSUED = "issued", "Issued"
        LOST = "lost", "Lost"
        DAMAGED = "damaged", "Damaged"
        RETIRED = "retired", "Retired"

    book = models.ForeignKey('book.Book', on_delete=models.PROTECT, related_name='copies')
    copy_code = models.CharField(max_length=50, unique=True, blank=True)   # auto-generated
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    condition_notes = models.CharField(max_length=255, blank=True)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        db_table = "book_copy"
        ordering = ["copy_code"]

    def save(self, *args, **kwargs):
        if not self.copy_code:
            self.copy_code = self.book.next_copy_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.copy_code} ({self.get_status_display()})"