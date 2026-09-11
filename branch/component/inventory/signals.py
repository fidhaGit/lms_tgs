from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BookCopy


def _recalculate(book):
    book.total_copies = book.copies.filter(is_delete=False).exclude(
        status=BookCopy.Status.RETIRED
    ).count()
    book.save(update_fields=["total_copies"])


@receiver(post_save, sender=BookCopy)
def bookcopy_saved(sender, instance, **kwargs):
    _recalculate(instance.book)


@receiver(post_delete, sender=BookCopy)
def bookcopy_deleted(sender, instance, **kwargs):
    _recalculate(instance.book)