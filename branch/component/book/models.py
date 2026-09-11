from django.db import models
from django.db.models import F
from shared.models import BaseModel


class Book(BaseModel):
    master_book = models.ForeignKey('masterbook.MasterBook', on_delete=models.PROTECT,related_name='branch_books', db_constraint=False,)
    branch = models.ForeignKey('branch.Branch', on_delete=models.PROTECT,related_name='books', db_constraint=False,)
    code = models.CharField(max_length=50, unique=True, blank=True)   # auto-generated
    copy_sequence = models.IntegerField(default=0)                    # internal counter
    total_copies = models.IntegerField(default=0)
    shelf_category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "book"
        unique_together = ("master_book", "branch")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and not self.code:
            self.code = f"{self.branch.code}-{self.master_book_id}"
            super().save(update_fields=["code"])

    def next_copy_code(self):
        Book.objects.filter(pk=self.pk).update(copy_sequence=F('copy_sequence') + 1)
        self.refresh_from_db(fields=['copy_sequence'])
        return f"{self.code}-{self.copy_sequence:03d}"

    def __str__(self):
        return f"{self.branch.name} — {self.master_book.title}"