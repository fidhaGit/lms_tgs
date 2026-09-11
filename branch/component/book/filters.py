import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='master_book__title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='master_book__author', lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='master_book__category', lookup_expr='iexact')
    branch = django_filters.NumberFilter(field_name='branch_id')
    available = django_filters.BooleanFilter(method='filter_available')

    def filter_available(self, queryset, name, value):
        return queryset.filter(total_copies__gt=0) if value else queryset.filter(total_copies=0)

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'branch', 'available']