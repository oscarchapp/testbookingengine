import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="buscar")

    class Meta:
        model = Room
        fields = []

    def filter_search(self, qs, name, value):
        if value:
            qs = qs.filter(name__icontains=value)
        return qs
