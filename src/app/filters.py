import django_filters
from app.models import Document


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = {
            "title": ["exact", "icontains"],
            "content": ["icontains"],
            "status": ["exact"],
            "author__username": ["exact", "icontains"],
            "created_at": ["exact", "gte", "lte"],
            "updated_at": ["exact", "gte", "lte"],
        }
