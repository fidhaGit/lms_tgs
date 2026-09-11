from rest_framework import serializers
from .models import Book
from superadmin.component.masterbook.models import MasterBook
from superadmin.component.branch.models import Branch


class BookSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    isbn = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at', 'is_delete', 'copy_sequence')
        read_only_fields = ('code', 'total_copies')

    def get_master_book(self, obj):
        return MasterBook.objects.using('default').filter(pk=obj.master_book_id).first()

    def get_branch(self, obj):
        return Branch.objects.using('default').filter(pk=obj.branch_id).first()

    def get_title(self, obj):
        master_book = self.get_master_book(obj)
        return master_book.title if master_book else None

    def get_author(self, obj):
        master_book = self.get_master_book(obj)
        return master_book.author if master_book else None

    def get_isbn(self, obj):
        master_book = self.get_master_book(obj)
        return master_book.isbn if master_book else None

    def get_category(self, obj):
        master_book = self.get_master_book(obj)
        return master_book.category if master_book else None

    def get_branch_name(self, obj):
        branch = self.get_branch(obj)
        return branch.name if branch else None

    def validate_master_book(self, value):
        if not MasterBook.objects.using('default').filter(pk=value.pk, is_delete=False).exists():
            raise serializers.ValidationError("This book does not exist in the master catalog.")
        return value

    def validate_branch(self, value):
        if not Branch.branch_exists(value.pk):
            raise serializers.ValidationError("This branch does not exist.")
        return value